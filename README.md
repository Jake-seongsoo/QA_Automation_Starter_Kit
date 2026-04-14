# QA 테스트 자동화 스타터 키트

Playwright + Python + pytest-bdd 를 사용한 UI/API 테스트 자동화 프레임워크입니다.
POM(Page Object Model) 구조와 Locator 중앙 관리 패턴을 적용하였으며,
네이버(naver.com)를 예제로 포함합니다.

---

## 기술 스택

| 도구 | 용도 |
|---|---|
| [Playwright](https://playwright.dev/python/) | 브라우저 자동화 |
| [pytest-bdd](https://pytest-bdd.readthedocs.io/) | BDD (Gherkin/Cucumber 문법) |
| [pytest-playwright](https://playwright.dev/python/docs/test-runners) | Playwright pytest 연동 |
| [Allure](https://allurereport.org/) | 테스트 리포트 |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 환경변수 관리 |

---

## 프로젝트 구조

```
QA_Automation_Starter_kit/
├── conftest.py                        # 전역 pytest fixture
├── pytest.ini                         # pytest 설정
├── requirements.txt                   # 패키지 의존성
├── .env.example                       # 환경변수 템플릿
│
├── config/
│   └── settings.py                    # 환경 설정 (base_url, timeout 등)
│
├── locators/
│   └── naver_locators.py              # ★ Locator 중앙 관리 파일 (단일 파일)
│
├── pages/                             # Page Object Model
│   ├── base_page.py
│   ├── naver_main_page.py
│   └── naver_search_result_page.py
│
├── api_clients/                       # API 클라이언트
│   ├── base_api_client.py
│   └── naver_api_client.py
│
├── features/                          # Gherkin .feature 파일
│   ├── ui/
│   │   ├── naver_search.feature
│   │   └── naver_first_result.feature
│   └── api/
│       ├── naver_health_check.feature
│       └── naver_open_api.feature
│
├── tests/                             # pytest-bdd step 정의
│   ├── ui/
│   │   ├── test_naver_search_steps.py
│   │   └── test_naver_first_result_steps.py
│   ├── api/
│   │   ├── test_naver_health_check_steps.py
│   │   └── test_naver_open_api_steps.py
│   └── unit/
│       ├── test_naver_locators.py
│       └── test_naver_api_client.py
│
└── reports/
    └── allure-results/                # 테스트 결과 저장 경로
```

---

## 설치 방법

### 1. Python 가상환경 생성 (권장)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. Playwright 브라우저 설치

```bash
playwright install chromium
```

### 4. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 값을 입력합니다:

```dotenv
# 네이버 오픈 API 인증 정보 (오픈 API 시나리오 실행 시 필요)
# https://developers.naver.com/apps/#/register 에서 발급
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
```

> 오픈 API 인증 정보가 없어도 UI 테스트와 헬스체크 API 테스트는 정상 실행됩니다.

---

## 실행 방법

### 전체 테스트 실행

```bash
pytest
```

### 마커로 필터링

```bash
# UI 테스트만 실행
pytest -m ui

# API 테스트만 실행
pytest -m api

# 스모크 테스트만 실행 (빠른 기본 검증)
pytest -m smoke
```

### 특정 파일/디렉터리 실행

```bash
# UI 테스트 디렉터리
pytest tests/ui/

# API 헬스체크만
pytest tests/api/test_naver_health_check_steps.py

# Unit 테스트만
pytest tests/unit/
```

### 브라우저 창 표시 (--headed)

```bash
pytest tests/ui/ --headed
```

### Allure 리포트 생성 및 조회

```bash
# 테스트 실행 (결과는 reports/allure-results/ 에 저장됨)
pytest

# 리포트 서버 시작 (브라우저가 자동으로 열림)
allure serve reports/allure-results
```

> Allure CLI 가 없는 경우: [Allure 설치 가이드](https://allurereport.org/docs/install/)

---

## 핵심 패턴 가이드

### Locator 추가하는 법

모든 선택자는 `locators/naver_locators.py` **한 곳에서만** 관리합니다.

```python
# locators/naver_locators.py
class NaverLocators:
    class MainPage:
        SEARCH_INPUT = '#query'      # 기존
        NEW_BUTTON = '#new-btn'      # 추가 ← 이 파일만 수정
```

페이지 객체에서는 이 파일을 import 하여 참조합니다:

```python
# pages/naver_main_page.py
from locators.naver_locators import NaverLocators

class NaverMainPage(BasePage):
    def click_new_button(self):
        self.page.click(NaverLocators.MainPage.NEW_BUTTON)  # locator 참조
```

### 새 Page Object 추가하는 법

1. `locators/naver_locators.py` 에 nested class 추가

```python
class NaverLocators:
    class NewsPage:              # 새 페이지 locator 추가
        HEADLINE = '.news_headline'
```

2. `pages/` 아래 새 파일 생성

```python
# pages/naver_news_page.py
from pages.base_page import BasePage
from locators.naver_locators import NaverLocators

class NaverNewsPage(BasePage):
    def get_headline(self) -> str:
        return self.page.inner_text(NaverLocators.NewsPage.HEADLINE)
```

3. `conftest.py` 에 fixture 추가

```python
@pytest.fixture
def naver_news_page(page) -> NaverNewsPage:
    return NaverNewsPage(page)
```

### 새 BDD 시나리오 추가하는 법

1. `features/ui/` 또는 `features/api/` 에 `.feature` 파일 작성
2. `tests/ui/` 또는 `tests/api/` 에 step 정의 파일(`test_*_steps.py`) 작성
3. 파일 상단에 `scenarios('ui/new_feature.feature')` 호출

---

## 환경변수 전체 목록

| 변수명 | 기본값 | 설명 |
|---|---|---|
| `BASE_URL` | `https://www.naver.com` | UI 테스트 기준 URL |
| `HEADLESS` | `true` | 브라우저 헤드리스 모드 |
| `TIMEOUT` | `10000` | 대기 타임아웃 (ms) |
| `NAVER_CLIENT_ID` | (없음) | 네이버 오픈 API 클라이언트 ID |
| `NAVER_CLIENT_SECRET` | (없음) | 네이버 오픈 API 클라이언트 시크릿 |

---

## 주의사항

- **Selector 깨짐**: 네이버 DOM은 수시로 변경됩니다. Selector가 맞지 않으면 `locators/naver_locators.py` 만 수정하세요.
- **오픈 API**: `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET` 미설정 시 오픈 API 시나리오는 자동으로 **skip** 처리됩니다.
- **Python 버전**: 3.10 이상을 권장합니다 (`str | None` 타입힌트 사용).
