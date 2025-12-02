# CLI Reference Update Template

> **Purpose:** CLI 정보 업데이트 시 사용할 표준 양식

---

## Update Checklist

레퍼런스를 업데이트할 때 다음 항목들을 확인하세요:

- [ ] CLI 명령어 변경 사항 확인
- [ ] NPM 패키지 이름 변경 확인
- [ ] 기본 모델 변경 확인
- [ ] 새로운 설치 방법 추가 확인
- [ ] 파일 기반 사용법 실제 테스트
- [ ] 공식 문서 링크 업데이트
- [ ] Update History에 변경 사항 기록

---

## Update Form

### 1. Basic Information

```yaml
CLI_NAME: "Example CLI"
COMMAND: "example"
NPM_PACKAGE: "@org/example-cli"
VERSION: "1.0.0"
STATUS: "Active" # Active, Deprecated, Beta
LAST_VERIFIED: "2025-11-30"
```

### 2. Installation

```yaml
INSTALLATION_METHOD:
  npm: "npm install -g @org/example-cli"
  homebrew: "brew install example-cli"
  other: "pip install example-cli"

PREREQUISITES:
  - "Node.js 18+"
  - "API Key from example.com"
```

### 3. Models

```yaml
DEFAULT_MODEL: "example-model-v1"

AVAILABLE_MODELS:
  - name: "example-model-v1"
    context_window: "128K"
    status: "Stable"
  - name: "example-model-v2"
    context_window: "1M"
    status: "Beta"
```

### 4. File-Based Usage

```yaml
FILE_BASED_SUPPORT: true # true, false, unknown

# If true, provide tested commands
INPUT_COMMAND: "example --input input.txt --output output.txt"

# Command structure
COMMAND_STRUCTURE:
  input_flag: "--input"
  output_flag: "--output"
  headless_flag: "--headless"
  model_flag: "--model"

# Test results
TEST_STATUS: "Verified" # Verified, Estimated, Untested
TEST_DATE: "2025-11-30"
TEST_NOTES: "Successfully tested with v1.0.0"
```

### 5. Environment Variables

```yaml
REQUIRED_ENV_VARS:
  - name: "EXAMPLE_API_KEY"
    description: "API key from example.com"
    required: true
  - name: "EXAMPLE_BASE_URL"
    description: "Base URL for API"
    required: false
    default: "https://api.example.com"
```

### 6. References

```yaml
REFERENCES:
  github: "https://github.com/org/example-cli"
  documentation: "https://docs.example.com"
  blog: "https://blog.example.com/announcement"
  tutorial: "https://tutorial.example.com"
```

### 7. Known Issues

```yaml
KNOWN_ISSUES:
  - issue: "File input not working on Windows"
    severity: "High"
    workaround: "Use WSL"
    status: "Open"
    reported: "2025-11-30"
```

---

## Update Process

### Step 1: Information Gathering
1. CLI 공식 문서 확인
2. GitHub repository 확인
3. 최신 릴리스 노트 확인
4. Community discussions 확인

### Step 2: Testing
1. CLI 설치 테스트
```bash
# 설치
npm install -g @org/example-cli

# 버전 확인
example --version

# 헬프 확인
example --help
```

2. 파일 기반 사용법 테스트
```bash
# 테스트 입력 파일 작성
echo "Test prompt" > test_input.txt

# CLI 실행
example --headless --input test_input.txt --output test_output.txt

# 결과 확인
cat test_output.txt
```

3. 결과 기록
- 성공 여부
- 오류 메시지 (있다면)
- 실행 시간
- 출력 품질

### Step 3: Documentation Update
1. `CLI_REFERENCE.md` 파일 열기
2. 해당 CLI 섹션 찾기
3. 변경 사항 반영
4. Update History 업데이트

### Step 4: Verification
1. 변경 사항 리뷰
2. 링크 유효성 확인
3. 코드 예제 검증
4. 문서 포맷 확인

---

## Example Update Entry

### Update History Format

```markdown
| Date | Version | Changes |
|------|---------|---------|
| 2025-11-30 | 1.1.0 | Claude Code: 파일 입출력 옵션 검증 완료 |
| 2025-11-30 | 1.0.0 | 초기 레퍼런스 작성 (웹 검색 기반) |
```

### Detailed Change Log Format

```markdown
## [1.1.0] - 2025-11-30

### Added
- Claude Code 파일 기반 사용법 검증
- 환경 변수 설정 예제

### Changed
- Default model: Sonnet 4.0 → Sonnet 4.5
- NPM package: `@anthropic/claude` → `@anthropic-ai/claude-code`

### Fixed
- Windows에서 파일 경로 이슈 해결 방법 추가

### Deprecated
- `--legacy-mode` 옵션 deprecated

### Removed
- Haiku 3.5 모델 지원 종료
```

---

## Automation Ideas

### Future Enhancements
1. **자동 버전 체크 스크립트**
```python
# check_versions.py
import subprocess
import json

CLIS = ['claude', 'gemini', 'codex', 'qwen']

for cli in CLIS:
    try:
        version = subprocess.check_output([cli, '--version'])
        print(f"{cli}: {version.decode().strip()}")
    except Exception as e:
        print(f"{cli}: Not installed or error - {e}")
```

2. **자동 테스트 스크립트**
```python
# test_cli.py
def test_file_based_io(cli_command):
    # 1. Create test input
    with open('test_input.txt', 'w') as f:
        f.write("Write a hello world function")

    # 2. Run CLI
    result = subprocess.run([cli_command, '--input', 'test_input.txt', '--output', 'test_output.txt'])

    # 3. Check output
    if os.path.exists('test_output.txt'):
        with open('test_output.txt', 'r') as f:
            output = f.read()
            return True, output
    return False, None
```

3. **문서 자동 생성 스크립트**
```python
# generate_reference.py
# YAML 데이터를 읽어서 Markdown 생성
```

---

## Notes

- 모든 변경 사항은 git으로 버전 관리
- Breaking changes는 메이저 버전 업데이트
- 테스트 결과는 별도 로그 파일로 보관
- Community feedback을 적극 반영
