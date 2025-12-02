"""Pytest 설정 파일

전역 fixture 및 테스트 설정
"""

import os
import pytest
from ai_cli_mcp.cli_registry import CLIRegistry


@pytest.fixture(autouse=True)
def reset_cli_registry():
    """각 테스트 전후로 CLI Registry 초기화

    싱글톤 패턴으로 인한 테스트 간 상태 공유를 방지합니다.
    autouse=True로 모든 테스트에 자동 적용됩니다.
    """
    # 테스트 전: Registry 완전 초기화
    instance = CLIRegistry._instance
    if instance is not None:
        if hasattr(instance, "_initialized"):
            delattr(instance, "_initialized")
        if hasattr(instance, "_runtime_clis"):
            instance._runtime_clis = {}

    CLIRegistry._instance = None

    # 환경 변수 정리
    if "CUSTOM_CLI_CONFIG" in os.environ:
        del os.environ["CUSTOM_CLI_CONFIG"]

    yield

    # 테스트 후: 정리
    instance = CLIRegistry._instance
    if instance is not None:
        if hasattr(instance, "_initialized"):
            delattr(instance, "_initialized")
        if hasattr(instance, "_runtime_clis"):
            instance._runtime_clis = {}

    CLIRegistry._instance = None

    if "CUSTOM_CLI_CONFIG" in os.environ:
        del os.environ["CUSTOM_CLI_CONFIG"]
