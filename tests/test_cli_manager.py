"""Tests for cli_manager module"""

import pytest
from ai_cli_mcp.cli_manager import (
    CLIInfo,
    list_available_clis,
    get_cli_version,
    is_cli_installed,
)


class TestCLIInfo:
    """Test CLIInfo dataclass"""

    def test_cli_info_creation(self):
        """CLIInfo 데이터클래스 생성 테스트"""
        cli_info = CLIInfo(
            name="test",
            command="test-cli",
            version="1.0.0",
            installed=True
        )
        assert cli_info.name == "test"
        assert cli_info.command == "test-cli"
        assert cli_info.version == "1.0.0"
        assert cli_info.installed is True

    def test_cli_info_with_none_version(self):
        """버전 정보가 없는 경우"""
        cli_info = CLIInfo(
            name="test",
            command="test-cli",
            version=None,
            installed=False
        )
        assert cli_info.version is None
        assert cli_info.installed is False


class TestIsCliInstalled:
    """Test is_cli_installed function"""

    def test_installed_cli(self):
        """설치된 CLI 감지 (python3는 반드시 설치되어 있음)"""
        assert is_cli_installed("python3") is True

    def test_uninstalled_cli(self):
        """미설치 CLI 감지"""
        assert is_cli_installed("nonexistent-cli-12345") is False


class TestGetCliVersion:
    """Test get_cli_version function"""

    def test_get_version_success(self):
        """버전 정보 조회 성공 (python3 --version)"""
        version = get_cli_version("python3")
        assert version is not None
        assert "Python" in version or "3." in version

    def test_get_version_failure(self):
        """버전 정보 조회 실패"""
        version = get_cli_version("nonexistent-cli-12345")
        assert version is None


class TestListAvailableClis:
    """Test list_available_clis function"""

    def test_returns_list(self):
        """list 타입 반환"""
        clis = list_available_clis()
        assert isinstance(clis, list)

    def test_returns_cli_info_objects(self):
        """CLIInfo 객체들의 리스트 반환"""
        clis = list_available_clis()
        assert len(clis) == 4  # claude, gemini, codex, qwen

        for cli in clis:
            assert isinstance(cli, CLIInfo)
            assert hasattr(cli, "name")
            assert hasattr(cli, "command")
            assert hasattr(cli, "version")
            assert hasattr(cli, "installed")

    def test_includes_all_configured_clis(self):
        """config에 정의된 모든 CLI 포함"""
        clis = list_available_clis()
        cli_names = {cli.name for cli in clis}

        expected_names = {"claude", "gemini", "codex", "qwen"}
        assert cli_names == expected_names

    def test_installed_status_accuracy(self):
        """설치 상태가 정확해야 함"""
        clis = list_available_clis()

        for cli in clis:
            # CLI가 실제로 설치되어 있는지 다시 확인
            actual_installed = is_cli_installed(cli.command)
            assert cli.installed == actual_installed, \
                f"{cli.name}의 installed 상태가 잘못되었습니다"

    def test_version_for_installed_clis(self):
        """설치된 CLI는 버전 정보를 가져야 함 (또는 None)"""
        clis = list_available_clis()

        for cli in clis:
            if cli.installed:
                # 버전이 있거나 None (일부 CLI는 --version을 지원하지 않을 수 있음)
                assert cli.version is None or isinstance(cli.version, str)

    def test_uninstalled_cli_has_none_version(self):
        """미설치 CLI는 version이 None이어야 함"""
        clis = list_available_clis()

        for cli in clis:
            if not cli.installed:
                assert cli.version is None
