---
description: '커밋 전 코드 품질/안전성 사전 검증: 불필요한 import 자동 제거, unit 테스트, 디버그 코드 검출, 시크릿 검출'
allowed-tools:
  [
    'Read',
    'Edit',
    'Grep',
    'Glob',
    'Bash(git status:*)',
    'Bash(git diff:*)',
    'Bash(python -m pytest:*)',
    'Bash(pytest:*)',
  ]
---

# /deploy-check

커밋 전 코드 품질과 안전성을 사전 검증한다. 자동 수정 가능한 항목은 즉시 수정하고, 수동 판단이 필요한 항목은 리포트로 알린다.

## 사용법

```
/deploy-check
```

`/commit` 실행 전에 항상 먼저 실행한다:
1. `/deploy-check` — 품질/안전성 검증 및 자동 수정
2. `/commit` — 커밋 메시지 생성 및 커밋

---

## 실행 절차

### STEP 0. 변경 대상 Python 파일 수집

아래 명령으로 변경된/스테이지된 파일 목록을 확인한다:

```bash
git status --short
git diff --name-only HEAD
git diff --name-only --cached
```

두 결과를 합쳐서 `.py` 확장자 파일만 추린다.

**대상 파일이 없으면** 다음 메시지를 출력하고 STEP 1~3을 건너뛰어 STEP 4~5 전체 파일 대상 검사로 이동한다:
```
ℹ️  변경된 Python 파일 없음. 전체 파일 대상으로 보안 검사만 진행합니다.
```

---

### STEP 1. 불필요한 import 자동 제거

STEP 0에서 수집한 각 Python 파일에 대해 순서대로 처리한다.

**분석 규칙:**

각 파일을 `Read` 로 읽은 뒤 아래 기준으로 미사용 import를 판별한다:

1. `import X` 형태: `X`, `X.`, `X(` 가 import 선언 이후 본문에 등장하지 않으면 미사용
2. `from X import Y` 형태: `Y`, `Y(`, `Y.` 가 import 선언 이후 본문에 등장하지 않으면 미사용
3. `from X import Y as Z` 형태: `Z`, `Z(`, `Z.` 가 등장하지 않으면 미사용

**제거하지 않는 예외 (side-effect / re-export import):**
- `__all__` 에 포함된 심볼
- `# noqa` 주석이 달린 라인
- `conftest.py` 내부의 pytest fixture용 import (`pytest`, `Playwright`, `APIRequestContext` 등)
- `__init__.py` 파일 전체 (re-export 가능성)
- `TYPE_CHECKING` 블록 내부 import
- 알려진 side-effect 모듈: `allure`, `pytest`, `typing_extensions`

미사용 import 발견 시 `Edit` 로 해당 라인만 제거한다. 제거 후 파일명과 제거한 심볼 이름을 누적 기록한다.

---

### STEP 2. pytest 수집 검증

```bash
python -m pytest tests/ --co -q 2>&1
```

**목적:** 수정된 파일에 import 에러, syntax 에러, BDD step 미구현 이슈가 없는지 사전 확인.

- 수집 성공 시: ✅ 기록
- 수집 실패 시: ❌ 기록 + 에러 출력의 첫 10줄을 리포트에 포함

---

### STEP 3. Unit 테스트 실행

```bash
python -m pytest tests/unit/ -v 2>&1
```

- 모두 통과 시: ✅ passed 수 기록
- 실패 발생 시: ❌ 기록 + 실패한 테스트 이름과 `AssertionError` 첫 줄만 추출하여 리포트에 포함
- **Unit 테스트가 한 건이라도 실패하면 최종 판정을 ❌ 차단으로 설정한다**

---

### STEP 4. 디버그 코드 검출 (리포트만, 자동 제거 안 함)

`Grep` 으로 아래 패턴을 프로젝트 전체 `.py` 파일에서 검색한다:

| 패턴 | 이유 |
|------|------|
| `^\s*print\(` | logger 대신 사용된 임시 출력 |
| `breakpoint\(\)` | 디버거 진입점 잔존 |
| `pdb\.set_trace\(\)` | 디버거 진입점 잔존 |
| `^\s*import pdb` | pdb 모듈 임포트 잔존 |

**예외:** `utils/logger.py` 파일은 검색 대상에서 제외한다.

검출 항목마다 `파일경로:라인번호` 형태로 리포트에 기록한다. **파일은 수정하지 않는다.**

---

### STEP 5. 시크릿 / .env 검출 (리포트만, 자동 제거 안 함)

#### 5-A. .env 스테이징 확인

`git status --short` 결과에 `.env` 파일이 포함되어 있으면 즉시 **차단 경고**:
```
🚫 차단: .env 파일이 스테이징되어 있습니다!
   git restore --staged .env  명령으로 제거 후 다시 시도하세요.
```

#### 5-B. 하드코딩된 시크릿 패턴 검색

아래 패턴으로 `.py` 및 `.feature` 파일 전체를 검색한다. `.env.example` 은 제외한다.

| 패턴 | 설명 |
|------|------|
| `NAVER_CLIENT_SECRET\s*=\s*['"][^'"]{4,}['"]` | 네이버 API 시크릿 하드코딩 |
| `NAVER_CLIENT_ID\s*=\s*['"][^'"]{4,}['"]` | 네이버 클라이언트 ID 하드코딩 |
| `api[_-]?key\s*=\s*['"][a-zA-Z0-9]{16,}['"]` | 일반 API 키 패턴 |

단, 값이 `your_`, `<`, `example`, `test_`, `dummy` 로 시작하는 placeholder 는 오탐으로 무시한다.

검출 시: `파일경로:라인번호` 기록 + 최종 판정을 ⚠️ 경고로 설정한다.

---

### STEP 6. 최종 리포트 출력

모든 STEP 완료 후 아래 형식으로 결과를 출력한다:

```
🔍 Deploy Check 결과
══════════════════════════════════════

✅ 자동 수정 완료
  - 불필요한 import 제거: N개 파일, 총 M라인 제거
    (수정 없으면: 변경된 파일에서 미사용 import 없음)

══════════════════════════════════════
검증 결과

  pytest 수집    : ✅ OK  /  ❌ FAIL
  Unit 테스트    : ✅ N passed  /  ❌ M failed
  디버그 코드    : ✅ 없음  /  ⚠️  N건 발견
                   (발견 시 파일:라인 목록)
  시크릿 검출    : ✅ 없음  /  🚫 .env 스테이징됨  /  ⚠️  N건 발견

══════════════════════════════════════
🚀 커밋 가능 여부

  ✅ 안전          — 모든 검증 통과, /commit 으로 진행하세요
  ⚠️  경고 확인 필요 — 디버그 코드 또는 시크릿 의심 항목 존재, 직접 확인 후 커밋
  ❌ 차단          — unit 테스트 실패 또는 .env 스테이징됨, 반드시 수정 후 재실행
```

**판정 기준:**
- ❌ 차단: unit 테스트 실패 1건 이상 **또는** .env 스테이징됨
- ⚠️ 경고: 디버그 코드 또는 시크릿 패턴 1건 이상 검출 (차단 조건 없을 때)
- ✅ 안전: 위 조건 모두 해당 없음
