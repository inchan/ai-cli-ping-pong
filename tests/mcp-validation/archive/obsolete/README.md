# 대체되거나 중복된 문서

이 문서들은 다른 문서로 요약되거나 대체되었습니다.

## 보관된 문서 및 대체 관계

| 원본 문서 | 크기 | 대체된 문서 | 사유 |
|----------|------|------------|------|
| PHASE0_INSTALLATION_REPORT.md | 8.9KB | PHASE0_SUCCESS_REPORT.md | 실패 분석 → 성공 보고서로 대체 |
| SELF_CRITICAL_REVIEW.md | 15.9KB | REVIEW_SUMMARY.md | 상세 리뷰 → 요약 보고서로 정리 |
| SESSION_SUMMARY.md | 12.1KB | PROJECT_STATUS.md | 세션별 요약 → 전체 진행 상황에 통합 |
| NEW_SESSION_GUIDE.md | 9.3KB | - | 새 세션 가이드 (필요성 낮음) |

## 각 문서의 보존 사유

### PHASE0_INSTALLATION_REPORT.md
- **내용**: MCP SDK 설치 실패 분석 및 문제 해결 과정
- **대체**: PHASE0_SUCCESS_REPORT.md (최종 성공 과정만 기록)
- **보존 이유**: 실패 과정에서 얻은 교훈 (Python 버전 호환성 등)

### SELF_CRITICAL_REVIEW.md
- **내용**: 코드베이스 전체에 대한 상세한 자기비판 리뷰
- **대체**: REVIEW_SUMMARY.md (핵심 개선사항만 요약)
- **보존 이유**: 전체 분석 과정 및 상세한 문제점 기록

### SESSION_SUMMARY.md
- **내용**: 작업 세션별 상세 요약
- **대체**: PROJECT_STATUS.md (전체 진행 상황에 통합)
- **보존 이유**: 세션별 의사결정 과정 추적

### NEW_SESSION_GUIDE.md
- **내용**: 새로운 작업 세션 시작 시 참조 가이드
- **대체**: 없음 (실제 사용 빈도 낮음)
- **보존 이유**: 향후 유사 프로젝트 시작 시 참조 가능

## 사용 지침

이 문서들은 **참조용으로만 보관**됩니다.

### 읽어야 할 경우
- ❌ 일반적인 프로젝트 이해 목적 (대체 문서 참조)
- ✅ 실패 과정 및 교훈 학습
- ✅ 상세한 리뷰 분석 과정 추적
- ✅ 과거 의사결정 근거 확인

### 읽지 않아도 되는 경우
- 프로젝트 전체 개요 파악 → `README.md` 참조
- 검증 결과 확인 → `VALIDATION_REPORT.md` 참조
- 진행 상황 확인 → `PROJECT_STATUS.md` 참조
- 리뷰 결과 확인 → `REVIEW_SUMMARY.md` 참조

---

**아카이브 일자**: 2025-11-30
**아카이브 사유**: 중복 제거 및 문서 구조 최적화
