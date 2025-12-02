# AI CLI Reference

> **Last Updated:** 2025-11-30
> **Purpose:** 지원되는 AI CLI 도구들의 명령어, 설치 방법, 사용법 레퍼런스

---

## Supported CLI Tools

| CLI | Command | NPM Package | Default Model | Status |
|-----|---------|-------------|---------------|--------|
| Claude Code | `claude` | `@anthropic-ai/claude-code` | Sonnet 4.5 | ✅ Active |
| Gemini CLI | `gemini` | `@google/gemini-cli` | Gemini 2.5 Pro | ✅ Active |
| Codex CLI | `codex` | `@openai/codex` | GPT-5-Codex | ✅ Active |
| Qwen Code | `qwen` | `@qwen-code/qwen-code` | Qwen3-Coder-480B | ✅ Active |

---

## 1. Claude Code CLI

### Overview
Claude Code는 터미널에서 동작하는 agentic 코딩 도구로, 코드 읽기, 수정, 실행을 로컬에서 수행합니다.

### Installation
```bash
npm install -g @anthropic-ai/claude-code
```

### Prerequisites
- Node.js 18 이상

### Available Models
- Sonnet 4.5 (기본)
- Opus 4.5
- Haiku 4.5

### File-Based Usage (추정)
```bash
# Input 파일에 프롬프트 작성
echo "Write a hello world function" > input.txt

# Claude 실행 (헤드리스 모드)
claude --headless --input input.txt --output output.txt

# Output 파일에서 결과 읽기
cat output.txt
```

### References
- [Official GitHub](https://github.com/anthropics/claude-code)
- [Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## 2. Gemini CLI

### Overview
Google의 오픈소스 AI 에이전트로, Gemini를 터미널에서 직접 사용할 수 있습니다.

### Installation
```bash
npm install -g @google/gemini-cli
```

### Prerequisites
- Google AI Studio API 키 또는 Vertex AI 키

### Available Models
- Gemini 2.5 Pro (기본, 1M context window)
- Gemini 3 Pro (Ultra 구독자용)

### File-Based Usage (추정)
```bash
# Input 파일에 프롬프트 작성
echo "Write a hello world function" > input.txt

# Gemini 실행
gemini --headless --input input.txt --output output.txt

# Output 파일에서 결과 읽기
cat output.txt
```

### References
- [Official GitHub](https://github.com/google-gemini/gemini-cli)
- [Documentation](https://developers.google.com/gemini-code-assist/docs/gemini-cli)
- [Blog Announcement](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)

---

## 3. OpenAI Codex CLI

### Overview
OpenAI의 경량 코딩 에이전트로, 최신 reasoning 모델을 터미널에서 사용할 수 있습니다.

### Installation
```bash
# npm 사용
npm i -g @openai/codex

# 또는 Homebrew (macOS)
brew install --cask codex
```

### Prerequisites
- ChatGPT Plus, Pro, Business, Edu, 또는 Enterprise 플랜

### Available Models
- GPT-5-Codex (기본)
- GPT-5

### File-Based Usage (추정)
```bash
# Input 파일에 프롬프트 작성
echo "Write a hello world function" > input.txt

# Codex 실행
codex --headless --input input.txt --output output.txt

# Output 파일에서 결과 읽기
cat output.txt
```

### References
- [Official GitHub](https://github.com/openai/codex)
- [Documentation](https://developers.openai.com/codex/cli/)
- [Getting Started Guide](https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started)

---

## 4. Qwen Code CLI

### Overview
Alibaba의 오픈소스 AI 코딩 도구로, Qwen3-Coder 모델을 사용합니다.

### Installation
```bash
npm install -g @qwen-code/qwen-code
```

### Prerequisites
- 환경 변수 설정 필요:
  - `OPENAI_API_KEY`: DashScope API 키
  - `OPENAI_BASE_URL`: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  - `OPENAI_MODEL`: qwen3-coder-plus

### Available Models
- Qwen3-Coder-480B-A35B-Instruct (기본, 256K-1M context)

### File-Based Usage (추정)
```bash
# 환경 변수 설정
export OPENAI_API_KEY="your-api-key"
export OPENAI_BASE_URL="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
export OPENAI_MODEL="qwen3-coder-plus"

# Input 파일에 프롬프트 작성
echo "Write a hello world function" > input.txt

# Qwen 실행
qwen --headless --input input.txt --output output.txt

# Output 파일에서 결과 읽기
cat output.txt
```

### References
- [Official Blog Post](https://qwenlm.github.io/blog/qwen3-coder/)
- [Community GitHub](https://github.com/dinoanderson/qwen_cli_coder)
- [Tutorial](https://www.datacamp.com/tutorial/qwen-code)

---

## Notes

### ⚠️ Important - MCP 서버 사용자 필독

본 문서의 **"File-Based Usage"** 섹션은 각 CLI의 실제 명령어를 **추정**한 것입니다.

**실제 MCP 서버 구현 방식**:

본 AI CLI Ping-Pong MCP 서버는 파일 옵션 (--input/--output)을 사용하지 않고,
**stdin/stdout 파이프 방식**을 사용합니다:

```bash
cat input.txt | cli [args] > output.txt
```

**사용자는 CLI의 명령어 옵션을 직접 알 필요가 없습니다.**
MCP 도구(`send_message`)를 통해 자동으로 처리됩니다.

**이 문서에서 정확한 정보**:
- ✅ CLI별 설치 가이드
- ✅ 지원 모델 정보
- ✅ 환경 변수 설정 (Qwen 등)

**추정 정보 (참고용)**:
- ⚠️ File-Based Usage 섹션 (실제 MCP 서버에서 사용하지 않음)

### MCP 서버를 통한 실제 사용법

본 MCP 서버를 사용할 때는 다음과 같이 MCP 도구를 호출합니다:

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

**CLI별 특이사항**:

- **Codex**: `skip_git_repo_check` 파라미터 지원
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

- **Qwen**: 환경 변수 필요 (MCP 서버 설정에서 자동 처리)
  - `OPENAI_BASE_URL`: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  - `OPENAI_MODEL`: qwen3-coder-plus

자세한 통합 방법은 [`INTEGRATION_GUIDE.md`](./INTEGRATION_GUIDE.md)를 참조하세요.

---

## Update History

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-30 | 1.0.0 | 초기 레퍼런스 작성 (웹 검색 기반) |
