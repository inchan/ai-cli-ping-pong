"""CLI Configuration

CLI별 명령어 템플릿 및 설정 관리
"""

from typing import TypedDict


class CLIConfig(TypedDict):
    """CLI 설정 타입"""
    command: str
    timeout: int
    extra_args: list[str]
    env_vars: dict[str, str]  # 환경 변수
    supports_skip_git_check: bool  # --skip-git-repo-check 플래그 지원 여부
    skip_git_check_position: str  # 플래그 위치: "before_extra_args" 또는 "after_extra_args"
    supported_args: list[str]  # 지원하는 CLI 인자 목록


# CLI별 설정
CLI_CONFIGS: dict[str, CLIConfig] = {
    "claude": {
        "command": "claude",
        "extra_args": [],
        "timeout": 60,
        "env_vars": {},
        "supports_skip_git_check": False,
        "skip_git_check_position": "before_extra_args",
        "supported_args": [
            "--system-prompt",
            "--append-system-prompt",
            "--print",
            "--model",
            "--debug",
            "--tools",
            "--allowed-tools",
            "--disallowed-tools",
            "--mcp-config",
            "--settings",
            "--permission-mode",
            "--continue",
            "--resume",
            "--output-format",
        ],
    },
    "gemini": {
        "command": "gemini",
        "extra_args": [],
        "timeout": 60,
        "env_vars": {},
        "supports_skip_git_check": False,
        "skip_git_check_position": "before_extra_args",
        "supported_args": [
            "--model",
            "--approval-mode",
            "--allowed-mcp-server-names",
            "--allowed-tools",
            "--extensions",
            "--output-format",
            "--debug",
            "--sandbox",
            "--yolo",
            "--include-directories",
            "--list-extensions",
            "--resume",
            "--list-sessions",
            "--delete-session",
        ],
    },
    "codex": {
        "command": "codex",
        "extra_args": ["exec", "-"],
        "timeout": 60,
        "env_vars": {},
        "supports_skip_git_check": True,
        "skip_git_check_position": "after_extra_args",  # codex exec --skip-git-repo-check -
        "supported_args": [
            "--skip-git-repo-check",
            "--model",
            "--sandbox",
            "--config",
            "--enable",
            "--disable",
            "--json",
            "--output-schema",
            "--color",
            "--image",
            "--profile",
            "--full-auto",
            "--cd",
            "--add-dir",
            "--output-last-message",
        ],
    },
    "qwen": {
        "command": "qwen",
        "extra_args": [],
        "timeout": 60,
        "env_vars": {
            "OPENAI_BASE_URL": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            "OPENAI_MODEL": "qwen3-coder-plus",
        },
        "supports_skip_git_check": False,
        "skip_git_check_position": "before_extra_args",
        "supported_args": [
            "--model",
            "--approval-mode",
            "--allowed-mcp-server-names",
            "--allowed-tools",
            "--extensions",
            "--output-format",
            "--debug",
            "--sandbox",
            "--yolo",
            "--include-directories",
            "--openai-api-key",
            "--openai-base-url",
            "--tavily-api-key",
            "--google-api-key",
            "--google-search-engine-id",
            "--web-search-default",
        ],
    },
}
