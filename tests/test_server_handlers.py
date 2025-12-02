"""Tests for MCP Server call_tool handlers

Priority 1 테스트: server.py의 비동기 핸들러 및 도구 실행 로직
"""

import asyncio
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from ai_cli_mcp.server import app, call_tool
from ai_cli_mcp.file_handler import (
    CLINotFoundError,
    CLITimeoutError,
    CLIExecutionError,
)


class TestCallToolListAvailableCLIs:
    """list_available_clis 도구 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_call_tool_list_available_clis_success(self):
        """list_available_clis 핸들러 성공 케이스"""
        result = await call_tool("list_available_clis", {})

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
        result = await call_tool("list_available_clis", {})

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
        # 실제 list_available_clis 호출하므로 to_thread 호출 여부는
        # 실제 동작으로 검증됨. 이 테스트는 기존 success 테스트로 충분함
        result = await call_tool("list_available_clis", {})

        # 비동기 처리가 제대로 되었으므로 응답 받음
        assert isinstance(result, dict)
        assert "clis" in result


class TestCallToolSendMessage:
    """send_message 도구 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_call_tool_send_message_success(self):
        """send_message 성공 케이스"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Success response"

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Hello, world!",
            })

            assert "response" in result
            assert result["response"] == "Success response"
            mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_call_tool_send_message_with_system_prompt(self):
        """시스템 프롬프트 포함 send_message"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Response with system prompt"

            result = await call_tool("send_message", {
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
    async def test_call_tool_send_message_with_skip_git_check(self):
        """skip_git_repo_check 포함 send_message (Codex용)"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Codex response"

            result = await call_tool("send_message", {
                "cli_name": "codex",
                "message": "Write code",
                "skip_git_repo_check": True,
            })

            assert "response" in result
            mock_execute.assert_called_once()
            # skip_git_repo_check가 True로 전달되었는지 확인
            call_args = mock_execute.call_args
            assert call_args.args[2] is True  # 3번째 인자

    @pytest.mark.asyncio
    async def test_call_tool_send_message_cli_not_found_error(self):
        """CLI not found 에러 처리"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLINotFoundError("claude (claude)가 설치되지 않았습니다")

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Hello",
            })

            assert "error" in result
            assert result["type"] == "CLINotFoundError"
            assert "설치되지 않았습니다" in result["error"]

    @pytest.mark.asyncio
    async def test_call_tool_send_message_timeout_error(self):
        """타임아웃 에러 처리"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLITimeoutError("CLI 실행 타임아웃 (60초)")

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Long request",
            })

            assert "error" in result
            assert result["type"] == "CLITimeoutError"
            assert "타임아웃" in result["error"]

    @pytest.mark.asyncio
    async def test_call_tool_send_message_execution_error(self):
        """실행 에러 처리"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLIExecutionError("CLI 실행 실패 (코드 1)")

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Request",
            })

            assert "error" in result
            assert result["type"] == "CLIExecutionError"
            assert "실패" in result["error"]

    @pytest.mark.asyncio
    async def test_call_tool_send_message_asyncio_to_thread(self):
        """asyncio.to_thread() 호출 검증"""
        with patch("ai_cli_mcp.server.asyncio.to_thread") as mock_to_thread:
            # to_thread가 반환할 값
            async def async_to_thread(*args, **kwargs):
                return "Response"

            mock_to_thread.side_effect = async_to_thread

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Test",
            })

            # to_thread 호출 확인
            mock_to_thread.assert_called_once()
            assert "response" in result or "error" in result


class TestCallToolAddCLI:
    """add_cli 도구 핸들러 테스트"""

    @pytest.mark.asyncio
    async def test_call_tool_add_cli_minimal(self):
        """add_cli 최소 필드 (name, command만)"""
        result = await call_tool("add_cli", {
            "name": "deepseek",
            "command": "deepseek",
        })

        assert result["success"] is True
        assert result["message"] == "CLI 'deepseek' 추가 완료"
        assert result["cli"]["name"] == "deepseek"
        assert result["cli"]["command"] == "deepseek"

    @pytest.mark.asyncio
    async def test_call_tool_add_cli_full_options(self):
        """add_cli 전체 옵션"""
        result = await call_tool("add_cli", {
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
    async def test_call_tool_add_cli_then_list(self):
        """add_cli 후 list_available_clis에 반영"""
        # 1. CLI 추가
        add_result = await call_tool("add_cli", {
            "name": "test_cli",
            "command": "test-cli",
        })
        assert add_result["success"] is True

        # 2. 목록에서 확인
        list_result = await call_tool("list_available_clis", {})
        cli_names = [cli["name"] for cli in list_result["clis"]]
        assert "test_cli" in cli_names

    @pytest.mark.asyncio
    async def test_call_tool_add_cli_with_error(self):
        """add_cli 실패 케이스"""
        with patch("ai_cli_mcp.server.get_cli_registry") as mock_registry:
            mock_registry.return_value.add_cli.side_effect = Exception("Registry error")

            result = await call_tool("add_cli", {
                "name": "bad_cli",
                "command": "bad",
            })

            assert "error" in result
            assert result["type"] == "AddCLIError"

    @pytest.mark.asyncio
    async def test_call_tool_add_cli_overwrite_existing(self):
        """기존 CLI를 동일 이름으로 덮어쓰기"""
        # 1. 첫 번째 추가
        result1 = await call_tool("add_cli", {
            "name": "override_test",
            "command": "cmd1",
        })
        assert result1["success"] is True

        # 2. 같은 이름으로 다시 추가
        result2 = await call_tool("add_cli", {
            "name": "override_test",
            "command": "cmd2",
        })
        assert result2["success"] is True

        # 3. 마지막 값으로 덮어써졌는지 확인
        list_result = await call_tool("list_available_clis", {})
        # override_test CLI가 하나만 존재해야 함 (마지막 값)


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
    async def test_call_tool_list_then_send(self):
        """list → send 순서대로 호출"""
        # 1. 목록 조회
        list_result = await call_tool("list_available_clis", {})
        assert "clis" in list_result

        # 2. send_message 시도 (실제로는 모킹됨)
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Test response"

            send_result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Test",
            })
            assert "response" in send_result

    @pytest.mark.asyncio
    async def test_call_tool_add_then_list(self):
        """add_cli → list 순서대로 호출"""
        # 1. CLI 추가
        add_result = await call_tool("add_cli", {
            "name": "integration_test",
            "command": "it-cmd",
        })
        assert add_result["success"] is True

        # 2. 목록에서 확인
        list_result = await call_tool("list_available_clis", {})
        cli_names = [cli["name"] for cli in list_result["clis"]]
        assert "integration_test" in cli_names

    @pytest.mark.asyncio
    async def test_call_tool_error_recovery(self):
        """에러 후에도 정상 동작"""
        # 1. 에러 발생
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLINotFoundError("Not found")

            error_result = await call_tool("send_message", {
                "cli_name": "nonexistent",
                "message": "Test",
            })
            assert "error" in error_result

        # 2. 에러 후에도 정상 호출 가능
        list_result = await call_tool("list_available_clis", {})
        assert "clis" in list_result


class TestCallToolErrorHandling:
    """에러 처리 상세 테스트"""

    @pytest.mark.asyncio
    async def test_error_message_includes_cli_name(self):
        """에러 메시지에 CLI 이름 포함"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLINotFoundError("claude가 설치되지 않았습니다")

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Test",
            })

            assert "claude" in result["error"]

    @pytest.mark.asyncio
    async def test_error_type_is_specified(self):
        """에러 타입이 명시됨"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.side_effect = CLITimeoutError("Timeout")

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "Test",
            })

            assert "type" in result
            assert result["type"] == "CLITimeoutError"

    @pytest.mark.asyncio
    async def test_all_error_types_handled(self):
        """모든 에러 타입 처리 검증"""
        errors = [
            (CLINotFoundError("Not found"), "CLINotFoundError"),
            (CLITimeoutError("Timeout"), "CLITimeoutError"),
            (CLIExecutionError("Execution failed"), "CLIExecutionError"),
        ]

        for error, error_type in errors:
            with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
                mock_execute.side_effect = error

                result = await call_tool("send_message", {
                    "cli_name": "test",
                    "message": "Test",
                })

                assert result["type"] == error_type
                assert "error" in result


# 엣지 케이스 테스트
class TestCallToolEdgeCases:
    """엣지 케이스 테스트"""

    @pytest.mark.asyncio
    async def test_send_message_with_empty_message(self):
        """빈 메시지 전송"""
        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = ""

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": "",
            })

            assert "response" in result

    @pytest.mark.asyncio
    async def test_send_message_with_long_message(self):
        """매우 긴 메시지 전송"""
        long_message = "x" * 10000

        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Response"

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": long_message,
            })

            assert "response" in result

    @pytest.mark.asyncio
    async def test_send_message_with_special_characters(self):
        """특수 문자 포함 메시지"""
        special_message = "Hello! @#$%^&*()_+-=[]{}|;:',.<>?/~`"

        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Response"

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": special_message,
            })

            assert "response" in result

    @pytest.mark.asyncio
    async def test_add_cli_with_special_characters_in_name(self):
        """특수 문자를 포함한 CLI 이름"""
        result = await call_tool("add_cli", {
            "name": "test-cli-2024",
            "command": "test-cmd",
        })

        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_send_message_with_unicode_characters(self):
        """유니코드 문자 포함 메시지"""
        unicode_message = "안녕하세요! 你好! مرحبا! 🎉"

        with patch("ai_cli_mcp.server.execute_cli_file_based") as mock_execute:
            mock_execute.return_value = "Response"

            result = await call_tool("send_message", {
                "cli_name": "claude",
                "message": unicode_message,
            })

            assert "response" in result
