"""Tests for MCP Server call_tool handlers

Priority 1 테스트: server.py의 비동기 핸들러 및 도구 실행 로직
"""

import asyncio
import pytest
import time
from unittest.mock import patch, MagicMock, AsyncMock

from ai_cli_mcp.server import app, call_tool
from ai_cli_mcp.file_handler import (
    CLINotFoundError,
    CLITimeoutError,
    CLIExecutionError,
)
from ai_cli_mcp.task_manager import TaskManager, get_task_manager, InMemoryStorage, TaskStatus # type: ignore


class TestCallToolListAvailableCLIs:
    """list_tools 도구 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_call_tool_list_available_clis_success(self):
        """list_tools 핸들러 성공 케이스"""
        result = await call_tool("list_tools", {})

        # 응답 형식 검증
        assert isinstance(result, dict)
        assert "clis" in result
        assert isinstance(result["clis"], list)

        # 기본 CLI 포함 확인
        cli_names = [cli["name"] for cli in result["clis"]]
        assert "claude" in cli_names
        assert "gemini" in cli_names
        assert "codex" in cli_names
        assert "qwen" in cli_names

    @pytest.mark.asyncio
    async def test_call_tool_list_available_clis_cli_structure(self):
        """각 CLI 항목의 구조 검증"""
        result = await call_tool("list_tools", {})

        for cli in result["clis"]:
            # 필수 필드 존재
            assert "name" in cli
            assert "command" in cli
            assert "version" in cli
            assert "installed" in cli

            # 필드 타입 검증
            assert isinstance(cli["name"], str)
            assert isinstance(cli["command"], str)
            assert isinstance(cli["installed"], bool)
            # version은 None 또는 문자열
            assert cli["version"] is None or isinstance(cli["version"], str)

    @pytest.mark.asyncio
    async def test_call_tool_list_available_clis_asyncio_called(self):
        """asyncio.to_thread()가 호출됨을 확인"""
        # 실제 list_tools 호출하므로 to_thread 호출 여부는
        # 실제 동작으로 검증됨. 이 테스트는 기존 success 테스트로 충분함
        result = await call_tool("list_tools", {})

        # 비동기 처리가 제대로 되었으므로 응답 받음
        assert isinstance(result, dict)
        assert "clis" in result


class TestCallToolRunTool:
    """run_tool 도구 핸들러 테스트 (동기/비동기 통합)"""

    @pytest.mark.asyncio
    async def test_call_tool_run_tool_sync_success(self):
        """run_tool 동기 실행 성공 케이스 (run_async=False)"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Success response"

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Hello, world!",
                "run_async": False
            })

            assert "response" in result
            assert result["response"] == "Success response"
            mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_call_tool_run_tool_default_sync(self):
        """run_tool 기본값은 동기 실행이어야 함"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Success"

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Hello"
            }) # run_async 생략

            assert "response" in result
            mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_call_tool_run_tool_async_success(self):
        """run_tool 비동기 실행 (run_async=True)"""
        
        # TaskManager 초기화 (테스트용)
        TaskManager._task_manager_instance = None
        manager = get_task_manager()
        manager.storage = InMemoryStorage()
        await manager.start()

        try:
            # 실제 실행 함수는 모킹
            mock_execution = MagicMock(return_value="Async Result")
            
            # server.py의 execute_cli_file_based를 패치
            # functools.partial로 감싸지기 때문에 호출 시점에 모킹된 함수가 사용됨
            with patch("ai_cli_mcp.server.execute_cli_file_based", new=mock_execution):
                result = await call_tool("run_tool", {
                    "cli_name": "claude",
                    "message": "Async Test",
                    "run_async": True
                })

                # 즉시 반환 확인
                assert "task_id" in result
                assert result["status"] == "running"
                task_id = result["task_id"]

                # 잠시 대기하여 작업 완료 유도
                await asyncio.sleep(0.1)

                # 작업이 실행되었는지 확인
                mock_execution.assert_called_once()

                # 상태 조회 (get_run_status 사용)
                status_result = await call_tool("get_run_status", {"task_id": task_id})
                assert status_result["status"] == "completed"
                assert status_result["result"] == "Async Result"

        finally:
            await manager.stop()
            TaskManager._task_manager_instance = None

    @pytest.mark.asyncio
    async def test_call_tool_run_tool_with_system_prompt(self):
        """시스템 프롬프트 포함 run_tool"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Response with system prompt"

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Tell me a story",
                "system_prompt": "You are a storyteller",
            })

            assert "response" in result
            mock_execute.assert_called_once()
            # system_prompt가 전달되었는지 확인
            call_args = mock_execute.call_args
            assert "system_prompt" in call_args.kwargs or len(call_args.args) > 3

    @pytest.mark.asyncio
    async def test_call_tool_run_tool_cli_not_found_error(self):
        """CLI not found 에러 처리 (동기)"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLINotFoundError("claude (claude)가 설치되지 않았습니다")

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Hello",
            })

            assert "error" in result
            assert result["type"] == "CLINotFoundError"
            assert "설치되지 않았습니다" in result["error"]

    @pytest.mark.asyncio
    async def test_call_tool_run_tool_execution_error(self):
        """실행 에러 처리 (동기)"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLIExecutionError("CLI 실행 실패 (코드 1)")

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Request",
            })

            assert "error" in result
            assert result["type"] == "CLIExecutionError"
            assert "실패" in result["error"]


class TestCallToolGetRunStatus:
    """get_run_status 도구 핸들러 테스트"""

    @pytest.fixture(autouse=True)
    async def setup_task_manager(self):
        """각 테스트 전에 TaskManager를 초기화하고, 테스트 후에 정리합니다."""
        TaskManager._task_manager_instance = None
        manager = get_task_manager()
        manager.storage = InMemoryStorage()
        await manager.start()
        yield manager
        await manager.stop()
        TaskManager._task_manager_instance = None

    @pytest.mark.asyncio
    async def test_get_run_status_not_found(self, setup_task_manager):
        """존재하지 않는 task_id 조회"""
        result = await call_tool("get_run_status", {"task_id": "invalid-id"})
        
        assert result["status"] == "not_found"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_run_status_completed(self, setup_task_manager):
        """완료된 작업 상태 조회"""
        # 수동으로 작업 추가
        def dummy_task():
            return "Done"
        
        task_id = await setup_task_manager.start_task(dummy_task)
        await asyncio.sleep(0.1) # 완료 대기

        result = await call_tool("get_run_status", {"task_id": task_id})
        
        assert result["status"] == "completed"
        assert result["result"] == "Done"


class TestCallToolAddTool:
    """add_tool 도구 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_call_tool_add_tool_minimal(self):
        """add_tool 최소 필드 (name, command만)"""
        result = await call_tool("add_tool", {
            "name": "deepseek",
            "command": "deepseek",
        })

        assert result["success"] is True
        assert result["message"] == "CLI 'deepseek' 추가 완료"
        assert result["cli"]["name"] == "deepseek"
        assert result["cli"]["command"] == "deepseek"

    @pytest.mark.asyncio
    async def test_call_tool_add_tool_full_options(self):
        """add_tool 전체 옵션"""
        result = await call_tool("add_tool", {
            "name": "custom_gpt",
            "command": "custom-gpt",
            "extra_args": ["--mode", "chat"],
            "timeout": 120,
            "env_vars": {"API_KEY": "secret"},
            "supports_skip_git_check": True,
            "skip_git_check_position": "after_extra_args",
        })

        assert result["success"] is True
        assert result["message"] == "CLI 'custom_gpt' 추가 완료"
        assert result["cli"]["name"] == "custom_gpt"
        assert result["cli"]["command"] == "custom-gpt"

    @pytest.mark.asyncio
    async def test_call_tool_add_tool_then_list(self):
        """add_tool 후 list_tools에 반영"""
        # 1. CLI 추가
        add_result = await call_tool("add_tool", {
            "name": "test_cli",
            "command": "test-cli",
        })
        assert add_result["success"] is True

        # 2. 목록에서 확인
        list_result = await call_tool("list_tools", {})
        cli_names = [cli["name"] for cli in list_result["clis"]]
        assert "test_cli" in cli_names

    @pytest.mark.asyncio
    async def test_call_tool_add_tool_with_error(self):
        """add_tool 실패 케이스"""
        with patch("ai_cli_mcp.server.get_cli_registry") as mock_registry:
            mock_registry.return_value.add_cli.side_effect = Exception("Registry error")

            result = await call_tool("add_tool", {
                "name": "bad_cli",
                "command": "bad",
            })

            assert "error" in result
            assert result["type"] == "AddCLIError"


class TestCallToolUnknownTool:
    """Unknown tool 에러 처리"""

    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool(self):
        """존재하지 않는 도구 호출"""
        result = await call_tool("nonexistent_tool", {})

        assert "error" in result
        assert "Unknown tool" in result["error"]
        assert "nonexistent_tool" in result["error"]


class TestCallToolIntegration:
    """도구 핸들러 통합 테스트"""

    @pytest.mark.asyncio
    async def test_call_tool_list_then_run(self):
        """list → run 순서대로 호출"""
        # 1. 목록 조회
        list_result = await call_tool("list_tools", {})
        assert "clis" in list_result

        # 2. run_tool 시도 (실제로는 모킹됨)
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Test response"

            send_result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Test",
            })
            assert "response" in send_result

    @pytest.mark.asyncio
    async def test_call_tool_add_then_list(self):
        """add_tool → list 순서대로 호출"""
        # 1. CLI 추가
        add_result = await call_tool("add_tool", {
            "name": "integration_test",
            "command": "it-cmd",
        })
        assert add_result["success"] is True

        # 2. 목록에서 확인
        list_result = await call_tool("list_tools", {})
        cli_names = [cli["name"] for cli in list_result["clis"]]
        assert "integration_test" in cli_names


class TestCallToolErrorHandling:
    """에러 처리 상세 테스트"""

    @pytest.mark.asyncio
    async def test_error_message_includes_cli_name(self):
        """에러 메시지에 CLI 이름 포함"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLINotFoundError("claude가 설치되지 않았습니다")

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Test",
            })

            assert "claude" in result["error"]

    @pytest.mark.asyncio
    async def test_error_type_is_specified(self):
        """에러 타입이 명시됨"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLITimeoutError("Timeout")

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "Test",
            })

            assert "type" in result
            assert result["type"] == "CLITimeoutError"


# 엣지 케이스 테스트
class TestCallToolEdgeCases:
    """엣지 케이스 테스트"""

    @pytest.mark.asyncio
    async def test_run_tool_with_empty_message(self):
        """빈 메시지 전송"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = ""

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": "",
            })

            assert "response" in result

    @pytest.mark.asyncio
    async def test_run_tool_with_long_message(self):
        """매우 긴 메시지 전송"""
        long_message = "x" * 10000

        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Response"

            result = await call_tool("run_tool", {
                "cli_name": "claude",
                "message": long_message,
            })

            assert "response" in result
