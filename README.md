# AI CLI Ping-Pong MCP Server

MCP (Model Context Protocol) 서버로 로컬에 설치된 AI CLI 도구들과 **파일 기반**으로 통신합니다.

## ✨ Features

- ✅ **비동기 작업 실행**: `start_send_message`와 `get_task_status`를 통해 긴 작업을 백그라운드에서 처리
- ✅ **영속적 작업 저장소**: SQLite를 사용하여 서버가 재시작되어도 작업 상태 유지 (선택 사항)
- ✅ **다양한 CLI 지원**: Claude, Gemini, Codex, Qwen 등 주요 AI 코딩 CLI 도구 지원
- ✅ **동적 CLI 추가**: `add_cli`를 통해 런타임에 새로운 CLI 동적으로 추가
- ✅ **안전한 파일 기반 통신**: Stateless 세션을 통해 안전한 CLI 실행 보장
- ✅ **상세 로깅 시스템**: 디버깅 및 모니터링 용이
- ✅ **MCP 서버 통합**: MCP SDK 1.22.0과 완벽 호환

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

자세한 내용은 다음 문서를 참조하세요:
- [**비동기 작업 실행 아키텍처 (Asynchronous Task Execution Architecture)**](./docs/ASYNC_TASK_ARCHITECTURE.md)

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

## ⚙️ Configuration

### 저장소 유형 (Storage Type)
`TaskManager`가 작업 상태를 저장하는 방식을 설정할 수 있습니다.

- **`memory` (기본값)**: 작업을 인-메모리에 저장합니다. 서버 재시작 시 모든 작업 내역이 사라집니다.
- **`sqlite`**: 작업을 SQLite 데이터베이스 파일(`.data/tasks.db`)에 영속적으로 저장합니다. 서버가 재시작되어도 작업 내역이 유지됩니다.

**설정 방법**:
`MCP_STORAGE_TYPE` 환경 변수를 사용하여 저장소 유형을 지정합니다.

```bash
# SQLite 저장소를 사용하려면 서버 실행 전 환경 변수를 설정합니다.
export MCP_STORAGE_TYPE=sqlite
python -m ai_cli_mcp.server
```

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

### Available Tools (MCP)

#### `list_available_clis`

서버에 설정된 CLI 도구 목록과 설치 상태를 반환합니다.

```json
{
  "name": "list_available_clis"
}
```

#### `send_message`

AI CLI에 메시지를 보내고 응답이 올 때까지 대기하는 **동기(Synchronous)** 방식입니다. 간단하고 빠른 작업에 적합합니다.

```json
{
  "name": "send_message",
  "arguments": {
    "cli_name": "claude",
    "message": "Write a hello world function"
  }
}
```

#### `start_send_message`

긴 작업에 권장되는 **비동기(Asynchronous)** 방식입니다. 작업을 백그라운드에서 시작하고 즉시 `task_id`를 반환합니다.

```json
{
  "name": "start_send_message",
  "arguments": {
    "cli_name": "claude",
    "message": "Write a python script that analyzes a large CSV file."
  }
}
```

#### `get_task_status`

`start_send_message`로 시작된 비동기 작업의 상태를 조회합니다. 작업이 완료될 때까지 주기적으로 호출(polling)해야 합니다.

```json
{
  "name": "get_task_status",
  "arguments": {
    "task_id": "<your-task-id>"
  }
}
```

#### `add_cli`
런타임에 새로운 AI CLI 설정을 동적으로 추가합니다.

```json
{
  "name": "add_cli",
  "arguments": {
    "name": "my-custom-cli",
    "command": "my-cli-command"
  }
}
```

## License

MIT
