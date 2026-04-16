---
description: 'BDD 보일러플레이트 자동 생성: feature + steps + page object + locators (UI) 또는 api client (API)'
allowed-tools:
  [
    'Read',
    'Write',
    'Edit',
    'Glob',
    'Grep',
  ]
---

# /bdd-scaffold

`$ARGUMENTS` 를 파싱하여 BDD 테스트 스캐폴드 파일 일체를 자동 생성한다.

## 사용법

```
/bdd-scaffold {feature_name} {ui|api}
```

예시:
- `/bdd-scaffold naver_login ui`
- `/bdd-scaffold product_search api`

---

## 실행 절차

### STEP 0. 인수 파싱 및 유효성 검사

`$ARGUMENTS` 를 공백으로 분리한다.
- `feature_name` = 첫 번째 인수 (snake_case 필수, 예: `naver_login`)
- `type` = 두 번째 인수 (`ui` 또는 `api` 중 하나)

**유효성 실패 조건:**
- 인수가 2개 미만인 경우
- `type` 이 `ui` 또는 `api` 가 아닌 경우
- `feature_name` 에 한글이나 공백이 포함된 경우

유효성 실패 시 올바른 사용법을 안내하고 즉시 중단한다.

**이름 변환 규칙 (이후 단계에서 사용):**
- `class_name` = feature_name을 PascalCase로 변환
  - `naver_login` → `NaverLogin`
  - `product_search` → `ProductSearch`
  - 규칙: `_` 로 단어 분리 → 각 단어 첫 글자 대문자 → 합치기
- `fixture_name` = feature_name 그대로 (snake_case)
  - 예: `naver_login`

---

### STEP 1. 기존 파일 중복 확인

생성할 파일이 이미 존재하는지 Glob으로 확인한다.

**UI 타입 확인 대상:**
- `features/ui/{feature_name}.feature`
- `tests/ui/test_{feature_name}_steps.py`
- `pages/{feature_name}_page.py`
- `locators/{feature_name}_locators.py`

**API 타입 확인 대상:**
- `features/api/{feature_name}.feature`
- `tests/api/test_{feature_name}_steps.py`
- `api_clients/{feature_name}_client.py`

이미 존재하는 파일이 있으면 해당 파일 목록을 사용자에게 알리고, 덮어쓸지 여부를 확인한 후 진행한다.

---

### STEP 2. 파일 생성

`type` 에 따라 아래 해당 섹션의 파일을 생성한다.

---

## UI 타입 생성 파일

### 2-UI-A. `features/ui/{feature_name}.feature`

```gherkin
# language: ko
기능: {feature_name} (기능 설명을 여기에 작성하세요)
  {feature_name} 에 대한 사용자 시나리오를 정의한다

  배경:
    조건 사용자가 {feature_name} 페이지에 접속한다

  @ui @smoke
  시나리오: 기본 동작이 정상적으로 수행된다
    만약 사용자가 기본 액션을 수행한다
    그러면 예상 결과가 표시된다

  @ui
  시나리오 개요: 다양한 입력값으로 동작을 확인한다
    만약 사용자가 "<입력값>" 으로 액션을 수행한다
    그러면 결과가 표시된다

    예:
      | 입력값   |
      | 값1      |
      | 값2      |
```

### 2-UI-B. `locators/{feature_name}_locators.py`

```python
"""
{feature_name} 페이지 Locator 관리 파일

{class_name} 관련 모든 CSS 선택자를 이 파일에서 관리한다.
DOM 변경 시 이 파일만 수정하면 전체 테스트에 반영된다.

사용 방법:
    from locators.{feature_name}_locators import {class_name}Locators
"""


class {class_name}Locators:
    """{class_name} 페이지 Locator 모음"""

    # TODO: 실제 CSS 선택자로 교체하세요
    # 예시 선택자 — 실제 DOM 구조에 맞게 수정 필요
    CONTAINER = '.container'
    PRIMARY_BUTTON = 'button[type="submit"]'
    INPUT_FIELD = 'input[name="input"]'
    RESULT_MESSAGE = '.result-message'
```

### 2-UI-C. `pages/{feature_name}_page.py`

```python
from playwright.sync_api import Page
from pages.base_page import BasePage
from locators.{feature_name}_locators import {class_name}Locators
from utils.logger import get_logger

logger = get_logger('{feature_name}_page')


class {class_name}Page(BasePage):
    """{class_name} 페이지 객체

    {class_name} 관련 동작을 캡슐화한다.
    Locator 는 {class_name}Locators 에서 참조한다.
    """

    URL = 'https://example.com/{feature_name}'  # TODO: 실제 URL로 교체하세요

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._locators = {class_name}Locators

    def open(self) -> None:
        """{class_name} 페이지를 열고 로딩을 대기한다"""
        logger.info('{class_name} 페이지 접속')
        self.goto(self.URL)
        self.wait_for_load()

    def is_loaded(self) -> bool:
        """페이지가 정상적으로 로딩되었는지 확인한다"""
        # TODO: 페이지 로딩 확인 로직을 구현하세요
        return self.page.is_visible(self._locators.CONTAINER)

    def perform_action(self, input_value: str) -> None:
        """기본 액션을 수행한다

        Args:
            input_value: 입력 값
        """
        logger.info(f'액션 수행: "{input_value}"')
        # TODO: 실제 동작 로직을 구현하세요
        self.page.fill(self._locators.INPUT_FIELD, input_value)
        self.page.click(self._locators.PRIMARY_BUTTON)
        self.page.wait_for_load_state('domcontentloaded')

    def get_result_message(self) -> str:
        """결과 메시지 텍스트를 반환한다"""
        return self.page.inner_text(self._locators.RESULT_MESSAGE)
```

### 2-UI-D. `tests/ui/test_{feature_name}_steps.py`

```python
import allure
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from pages.{feature_name}_page import {class_name}Page

# 이 파일에서 처리할 feature 파일 연결
scenarios('ui/{feature_name}.feature')


# ─────────────────────────────────────────
# Given (사전 조건)
# ─────────────────────────────────────────

@allure.step('사용자가 {feature_name} 페이지에 접속한다')
@given('사용자가 {feature_name} 페이지에 접속한다')
def step_open_page({fixture_name}_page: {class_name}Page):
    """{class_name} 페이지를 열고 로딩을 확인한다"""
    {fixture_name}_page.open()
    assert {fixture_name}_page.is_loaded(), '{class_name} 페이지가 정상 로딩되지 않았습니다'


# ─────────────────────────────────────────
# When (실행 액션)
# ─────────────────────────────────────────

@allure.step('사용자가 기본 액션을 수행한다')
@when('사용자가 기본 액션을 수행한다')
def step_perform_action({fixture_name}_page: {class_name}Page):
    """기본 액션을 수행한다"""
    # TODO: 실제 액션 호출로 교체하세요
    {fixture_name}_page.perform_action('기본값')


@allure.step('사용자가 "{input_value}" 으로 액션을 수행한다')
@when(parsers.parse('사용자가 "{input_value}" 으로 액션을 수행한다'))
def step_perform_action_with_value({fixture_name}_page: {class_name}Page, input_value: str):
    """입력값으로 액션을 수행한다"""
    {fixture_name}_page.perform_action(input_value)


# ─────────────────────────────────────────
# Then (결과 검증)
# ─────────────────────────────────────────

@allure.step('예상 결과가 표시된다')
@then('예상 결과가 표시된다')
def step_assert_result({fixture_name}_page: {class_name}Page):
    """예상 결과가 화면에 표시되는지 확인한다"""
    # TODO: 실제 검증 로직으로 교체하세요
    result = {fixture_name}_page.get_result_message()
    assert result, '결과 메시지가 표시되지 않았습니다'


@allure.step('결과가 표시된다')
@then('결과가 표시된다')
def step_assert_any_result({fixture_name}_page: {class_name}Page):
    """어떤 형태로든 결과가 표시되는지 확인한다"""
    # TODO: 실제 검증 로직으로 교체하세요
    assert {fixture_name}_page.is_loaded(), '결과 페이지가 로딩되지 않았습니다'
```

### 2-UI-E. `conftest.py` 수정

`conftest.py` 를 Read 로 읽은 뒤, 아래 두 블록을 파일 끝에 추가한다 (Edit 사용):

**import 블록** (파일 상단 import 영역에 추가):
```python
from pages.{feature_name}_page import {class_name}Page
```

**fixture 블록** (파일 끝 `# Page Object Fixture` 섹션에 추가):
```python

@pytest.fixture(scope='function')
def {fixture_name}_page(page) -> {class_name}Page:
    """{class_name}Page 인스턴스를 제공하는 fixture"""
    return {class_name}Page(page)
```

---

## API 타입 생성 파일

### 2-API-A. `features/api/{feature_name}.feature`

```gherkin
# language: ko
기능: {feature_name} API (기능 설명을 여기에 작성하세요)
  {feature_name} API 의 정상 동작을 검증한다

  @api @smoke
  시나리오: API 가 정상 응답한다
    만약 "{feature_name}" 엔드포인트에 GET 요청을 보낸다
    그러면 응답 상태 코드는 200 이다

  @api
  시나리오: API 가 올바른 데이터를 반환한다
    만약 "{feature_name}" 엔드포인트에 GET 요청을 보낸다
    그러면 응답 상태 코드는 200 이다
    그리고 응답 본문에 필수 필드가 포함된다
```

### 2-API-B. `api_clients/{feature_name}_client.py`

```python
from playwright.sync_api import APIRequestContext, APIResponse
from api_clients.base_api_client import BaseApiClient
from config.settings import Settings
from utils.logger import get_logger

logger = get_logger('{feature_name}_client')


class {class_name}Client(BaseApiClient):
    """{class_name} API 클라이언트

    {class_name} 관련 API 엔드포인트를 캡슐화한다.
    BaseApiClient 를 상속받아 공통 요청/로깅 로직을 재사용한다.
    """

    # TODO: 실제 Base URL 로 교체하세요
    BASE_URL = 'https://api.example.com'

    def __init__(self, request_context: APIRequestContext, settings: Settings) -> None:
        super().__init__(request_context, self.BASE_URL)
        self._settings = settings

    def get_{feature_name}(self) -> APIResponse:
        """{feature_name} 기본 엔드포인트에 GET 요청을 전송한다

        Returns:
            APIResponse 객체
        """
        logger.info('{feature_name} API 요청')
        # TODO: 실제 엔드포인트 경로로 교체하세요
        return self.get('/{feature_name}')

    def get_{feature_name}_by_id(self, resource_id: str) -> APIResponse:
        """ID 로 특정 {feature_name} 리소스를 조회한다

        Args:
            resource_id: 조회할 리소스 ID

        Returns:
            APIResponse 객체
        """
        logger.info(f'{feature_name} 리소스 조회: {resource_id}')
        return self.get(f'/{feature_name}/{resource_id}')
```

### 2-API-C. `tests/api/test_{feature_name}_steps.py`

```python
import allure
import pytest
from pytest_bdd import scenarios, when, then, parsers
from playwright.sync_api import APIResponse

from api_clients.{feature_name}_client import {class_name}Client

# 이 파일에서 처리할 feature 파일 연결
scenarios('api/{feature_name}.feature')


# ─────────────────────────────────────────
# When (실행 액션)
# ─────────────────────────────────────────

@allure.step('"{endpoint}" 엔드포인트에 GET 요청을 보낸다')
@when(parsers.parse('"{endpoint}" 엔드포인트에 GET 요청을 보낸다'), target_fixture='api_response')
def step_get_request({fixture_name}_client: {class_name}Client, endpoint: str) -> APIResponse:
    """{feature_name} API 에 GET 요청을 전송하고 응답을 반환한다"""
    return {fixture_name}_client.get_{feature_name}()


# ─────────────────────────────────────────
# Then (결과 검증)
# ─────────────────────────────────────────

@allure.step('응답 상태 코드는 {status_code:d} 이다')
@then(parsers.parse('응답 상태 코드는 {status_code:d} 이다'))
def step_assert_status_code(api_response: APIResponse, status_code: int):
    """HTTP 응답 상태 코드를 검증한다"""
    assert api_response.status == status_code, \
        f'기대 상태 코드: {status_code}, 실제: {api_response.status}'


@allure.step('응답 본문에 필수 필드가 포함된다')
@then('응답 본문에 필수 필드가 포함된다')
def step_assert_required_fields(api_response: APIResponse):
    """응답 JSON 에 필수 필드가 포함되어 있는지 검증한다"""
    # TODO: 실제 필수 필드 목록으로 교체하세요
    body = api_response.json()
    required_fields = []  # 예: ['id', 'name', 'status']
    for field in required_fields:
        assert field in body, f'응답 본문에 필수 필드 "{field}" 가 없습니다'
```

### 2-API-D. `conftest.py` 수정

`conftest.py` 를 Read 로 읽은 뒤, 아래 블록을 추가한다 (Edit 사용):

**import 블록** (파일 상단 import 영역에 추가):
```python
from api_clients.{feature_name}_client import {class_name}Client
```

**fixture 블록** (파일 끝 `# API Client Fixture` 섹션에 추가):
```python

@pytest.fixture(scope='function')
def {fixture_name}_client(api_request_context: APIRequestContext, settings: Settings) -> {class_name}Client:
    """{class_name}Client 인스턴스를 제공하는 fixture"""
    return {class_name}Client(api_request_context, settings)
```

---

### STEP 3. 생성 결과 요약 출력

모든 파일 생성 완료 후 아래 형식으로 결과를 출력한다:

```
✅ BDD 스캐폴드 생성 완료: {feature_name} ({type})

생성된 파일:
  📄 features/{type}/{feature_name}.feature
  🐍 tests/{type}/test_{feature_name}_steps.py
  [UI인 경우]
  🏗️  pages/{feature_name}_page.py
  📍 locators/{feature_name}_locators.py
  [API인 경우]
  🌐 api_clients/{feature_name}_client.py
  🔧 conftest.py (fixture 추가)

다음 단계:
  1. feature 파일에서 한국어 시나리오를 실제 비즈니스 요구사항에 맞게 수정하세요
  [UI인 경우]
  2. locators/{feature_name}_locators.py 에서 실제 CSS 선택자로 교체하세요
  3. pages/{feature_name}_page.py 에서 URL 및 동작 메서드를 구현하세요
  [API인 경우]
  2. api_clients/{feature_name}_client.py 에서 BASE_URL 및 엔드포인트를 설정하세요
  4. pytest -m {type} 으로 테스트를 실행하여 스텝 연결을 확인하세요
```
