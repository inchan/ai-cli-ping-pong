# AI CLI Ping-Pong MCP Server

MCP (Model Context Protocol) 서버로 로컬에 설치된 AI CLI 도구들과 **파일 기반**으로 통신합니다.

## ✨ Features

- ✅ **list_available_clis**: 설치된 AI CLI 도구 목록 조회
- ✅ **send_message**: AI CLI에 메시지 보내고 응답 받기
- ✅ **skip_git_repo_check**: Codex CLI Git 저장소 체크 스킵 (선택)
- ✅ **환경 변수 지원**: Qwen 등 API 키가 필요한 CLI 지원
- ✅ **로깅 시스템**: 디버깅 및 모니터링 용이
- ✅ **파일 기반 통신**: Stateless 세션으로 안전한 실행
- ✅ **MCP 서버 통합**: MCP SDK 1.22.0 설치 완료

## 📋 Supported CLIs

| CLI | Command | 환경 변수 | 특이사항 | 상태 |
|-----|---------|----------|---------|------|
| Claude Code | `claude` | - | - | ✅ 지원 |
| Gemini CLI | `gemini` | - | - | ✅ 지원 |
| OpenAI Codex | `codex` | - | skip_git_check 지원 | ✅ 지원 |
| Qwen Code | `qwen` | OPENAI_API_KEY 등 | 환경 변수 필요 | ✅ 지원 |

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- Node.js (for MCP Inspector)

### Setup

```bash
# 1. Python 3.12 설치 (권장)
brew install python@3.12

# 2. 가상 환경 생성
python3.12 -m venv venv
source venv/bin/activate

# 3. 패키지 설치 (개발 모드)
pip install -e .

# 4. 개발 의존성 설치 (선택)
pip install -e ".[dev]"
```

### Verify Installation

```bash
# MCP SDK 설치 확인
pip show mcp

# 서버 import 테스트
python -c "from ai_cli_mcp.server import app; print('Server:', app.name)"
```

## 🧪 Development

### Running the MCP Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run server directly (for debugging)
python -m ai_cli_mcp.server

# Run with MCP Inspector (for testing)
npx @modelcontextprotocol/inspector ./venv/bin/python -m ai_cli_mcp.server
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=src/ai_cli_mcp --cov-report=term-missing

# Run specific test file
pytest tests/test_config.py -v

# Run MCP validation tests
pytest tests/mcp-validation/ -v
```

## 📊 Test Coverage & Validation

**MCP 검증 완료** ✅
- ✅ **63개 테스트 통과** (100% 통과율)
- ✅ **전체 커버리지: 86.5%** (목표 80% 초과)
- ✅ **Hit Rate: 100%** (목표 95% 초과)
- ✅ **Success Rate: 100%** (목표 99% 초과)
- ✅ **프로덕션 준비 완료**

**파일별 커버리지:**
- ✅ `__init__.py`: 100%
- ✅ `config.py`: 100%
- ✅ `logger.py`: 91.7%
- ✅ `server.py`: 88.1%
- ✅ `file_handler.py`: 85.7%
- ✅ `cli_manager.py`: 81.4%

**테스트 분류:**
- 프로토콜 테스트 (Phase 1): 17개
- 기능 테스트 (Phase 2): 28개
- E2E 테스트 (Phase 3): 18개

## Architecture

```
MCP Client (Claude Code)
    ↓ stdio (JSON-RPC)
MCP Server (ai_cli_mcp)
    ↓ File-based I/O
AI CLI (claude, gemini, codex, qwen)
```

## 📚 Documentation

### Development Artifacts

Development artifacts (plans, reports, analysis) are stored locally in the `.artifacts/` directory to keep the repository clean.

- **`.artifacts/reports/`**: Final validation reports and summaries.
- **`.artifacts/plans/`**: Test and validation plans.
- **`.artifacts/analysis/`**: Code quality reviews and coverage analysis.

### Validation Reports

**프로덕션 배포 승인**: ✅ APPROVED

자세한 검증 과정 및 결과는 `tests/mcp-validation/` 디렉토리 참조:

- **`VALIDATION_REPORT.md`** - 최종 검증 보고서 (권장 읽기)
- `PROJECT_STATUS.md` - 전체 프로젝트 진행 상황
- `MCP_VALIDATION_PLAN.md` - 검증 계획 (5 phases)
- `PHASE0_SUCCESS_REPORT.md` - MCP SDK 설치 과정
- `PHASE1_COMPLETION_REPORT.md` - 서버 활성화 과정
- `PHASE3_COMPLETION_REPORT.md` - 행동 테스트 완료
- `MANUAL_TESTING_CHECKLIST.md` - MCP Inspector 수동 테스트 가이드
- `validation_metrics.json` - 메트릭 데이터

## Usage

### As MCP Server

**Claude Code 설정** (`.claude/settings.local.json`):
```json
{
  "mcpServers": {
    "ai-cli-mcp": {
      "command": "/Users/chans/workspace/pilot/ai-cli-ping-pong/venv/bin/python",
      "args": ["-m", "ai_cli_mcp.server"]
    }
  }
}
```

**Claude Desktop 설정** (`~/.config/claude/mcp_servers.json`):
```json
{
  "ai-cli-mcp": {
    "command": "/Users/chans/workspace/pilot/ai-cli-ping-pong/venv/bin/python",
    "args": ["-m", "ai_cli_mcp.server"],
    "cwd": "/Users/chans/workspace/pilot/ai-cli-ping-pong"
  }
}
```

### Tools

#### list_available_clis

설치된 CLI 도구 목록을 반환합니다.

```json
{
  "name": "list_available_clis"
}
```

Response:
```json
{
  "clis": [
    {
      "name": "claude",
      "command": "claude",
      "version": "1.0.0",
      "installed": true
    }
  ]
}
```

#### send_message

CLI에 메시지를 보내고 응답을 받습니다.

**기본 사용법**:
```json
{
  "name": "send_message",
  "arguments": {
    "cli_name": "claude",
    "message": "Write a hello world function"
  }
}
```

**Codex with skip_git_check**:
```json
{
  "name": "send_message",
  "arguments": {
    "cli_name": "codex",
    "message": "Write a hello world function",
    "skip_git_repo_check": true
  }
}
```

Response:
```json
{
  "response": "def hello():\n    print('Hello, World!')"
}
```

## License

MIT
