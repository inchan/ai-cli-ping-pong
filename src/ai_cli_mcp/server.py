"""MCP Server

AI CLI Ping-Pong MCP 서버 진입점
"""

import asyncio
import sys
from dataclasses import asdict
from typing import Any, Dict

# MCP SDK import
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .cli_manager import list_available_clis
from .cli_registry import get_cli_registry
from .file_handler import execute_cli_file_based, CLINotFoundError, CLIExecutionError, CLITimeoutError
from .logger import get_logger

logger = get_logger(__name__)


# MCP Server 인스턴스 생성
app = Server("ai-cli-mcp")


@app.list_tools()
async def list_tools():
    """도구 목록 반환"""
    from mcp.types import Tool

    return [
        Tool(
            name="list_available_clis",
            description="설치된 AI CLI 목록 조회",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="send_message",
            description="AI CLI에 메시지 전송 (파일 기반, 시스템 프롬프트 및 args 지원)",
            inputSchema={
                "type": "object",
                "properties": {
                    "cli_name": {
                        "type": "string",
                        "description": "CLI 이름 (claude, gemini, codex, qwen 또는 커스텀 CLI)"
                    },
                    "message": {
                        "type": "string",
                        "description": "전송할 프롬프트"
                    },
                    "system_prompt": {
                        "type": "string",
                        "description": "시스템 프롬프트 (세션별, 선택사항). Claude는 --append-system-prompt, 나머지는 YAML 형식으로 처리됨"
                    },
                    "skip_git_repo_check": {
                        "type": "boolean",
                        "description": "Git 저장소 체크 건너뛰기 (Codex만 지원, 기본값: true)"
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "추가 CLI 인자 (선택사항). 각 CLI가 지원하는 옵션만 전달되며, 지원하지 않는 옵션은 로그에 기록되고 무시됨"
                    }
                },
                "required": ["cli_name", "message"]
            }
        ),
        Tool(
            name="add_cli",
            description="동적으로 새로운 AI CLI 추가 (런타임)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "CLI 이름 (필수, 예: deepseek)"
                    },
                    "command": {
                        "type": "string",
                        "description": "실행 명령어 (필수, 예: deepseek)"
                    },
                    "extra_args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "추가 인자 (선택, 기본값: [])"
                    },
                    "timeout": {
                        "type": "number",
                        "description": "타임아웃 초 (선택, 기본값: 60)"
                    },
                    "env_vars": {
                        "type": "object",
                        "description": "환경 변수 (선택, 기본값: {})"
                    },
                    "supports_skip_git_check": {
                        "type": "boolean",
                        "description": "Git 체크 스킵 지원 (선택, 기본값: false)"
                    },
                    "skip_git_check_position": {
                        "type": "string",
                        "enum": ["before_extra_args", "after_extra_args"],
                        "description": "플래그 위치 (선택, 기본값: before_extra_args)"
                    },
                    "supported_args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "지원하는 CLI 인자 목록 (선택, 기본값: [])"
                    }
                },
                "required": ["name", "command"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]):
    """도구 실행 (비동기 처리 개선)"""
    if name == "list_available_clis":
        # 비동기로 실행하여 블로킹 방지
        clis = await asyncio.to_thread(list_available_clis)
        return {"clis": [asdict(cli) for cli in clis]}

    elif name == "send_message":
        cli_name = arguments["cli_name"]
        message = arguments["message"]
        system_prompt = arguments.get("system_prompt", None)
        skip_git_repo_check = arguments.get("skip_git_repo_check", True)
        args = arguments.get("args", [])

        try:
            # 비동기로 실행하여 블로킹 방지
            response = await asyncio.to_thread(
                execute_cli_file_based, cli_name, message, skip_git_repo_check, system_prompt, args
            )
            return {"response": response}
        except CLINotFoundError as e:
            logger.error(f"CLI not found: {e}")
            return {"error": str(e), "type": "CLINotFoundError"}
        except CLITimeoutError as e:
            logger.error(f"CLI timeout: {e}")
            return {"error": str(e), "type": "CLITimeoutError"}
        except CLIExecutionError as e:
            logger.error(f"CLI execution error: {e}")
            return {"error": str(e), "type": "CLIExecutionError"}

    elif name == "add_cli":
        # 필수 필드
        cli_name = arguments["name"]
        command = arguments["command"]

        # 선택 필드 (기본값 자동 적용)
        extra_args = arguments.get("extra_args")
        timeout = arguments.get("timeout")
        env_vars = arguments.get("env_vars")
        supports_skip_git_check = arguments.get("supports_skip_git_check")
        skip_git_check_position = arguments.get("skip_git_check_position")
        supported_args = arguments.get("supported_args")

        try:
            registry = get_cli_registry()
            registry.add_cli(
                name=cli_name,
                command=command,
                extra_args=extra_args,
                timeout=timeout,
                env_vars=env_vars,
                supports_skip_git_check=supports_skip_git_check,
                skip_git_check_position=skip_git_check_position,
                supported_args=supported_args,
            )
            logger.info(f"CLI '{cli_name}' 추가 성공")
            return {
                "success": True,
                "message": f"CLI '{cli_name}' 추가 완료",
                "cli": {
                    "name": cli_name,
                    "command": command
                }
            }
        except Exception as e:
            logger.error(f"CLI 추가 실패: {e}")
            return {"error": str(e), "type": "AddCLIError"}

    else:
        logger.warning(f"Unknown tool: {name}")
        return {"error": f"Unknown tool: {name}"}


def main():
    """메인 함수"""
    logger.info("AI CLI Ping-Pong MCP Server starting...")
    logger.info("MCP SDK version: 1.22.0")
    logger.info("Server name: ai-cli-mcp")
    logger.info("Available tools: list_available_clis, send_message, add_cli")

    # stdio 서버 시작
    from mcp.server.stdio import stdio_server

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    asyncio.run(run())


if __name__ == "__main__":
    main()
