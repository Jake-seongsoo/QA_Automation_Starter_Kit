import allure
import pytest
from playwright.sync_api import Playwright, APIRequestContext

from config.settings import Settings
from pages.naver_main_page import NaverMainPage
from pages.naver_search_result_page import NaverSearchResultPage
from api_clients.naver_api_client import NaverApiClient
from utils.logger import get_logger

logger = get_logger('conftest')


# ─────────────────────────────────────────
# 기본 설정 Fixture
# ─────────────────────────────────────────

@pytest.fixture(scope='session')
def settings() -> Settings:
    """테스트 전 세션에서 공유하는 환경 설정 인스턴스"""
    return Settings()


# ─────────────────────────────────────────
# Playwright 브라우저 옵션 오버라이드
# ─────────────────────────────────────────

@pytest.fixture(scope='session')
def browser_context_args(browser_context_args, settings):
    """브라우저 컨텍스트 기본 옵션을 설정한다 (viewport, timeout 등)"""
    return {
        **browser_context_args,
        'viewport': {'width': 1280, 'height': 720},
        'locale': 'ko-KR',
    }


# ─────────────────────────────────────────
# API RequestContext Fixture
# ─────────────────────────────────────────

@pytest.fixture(scope='function')
def api_request_context(playwright: Playwright, settings: Settings) -> APIRequestContext:
    """Playwright APIRequestContext 인스턴스를 생성하고 테스트 후 정리한다"""
    context = playwright.request.new_context(
        base_url=settings.openapi_url,
        extra_http_headers={
            'Accept': 'application/json',
        }
    )
    yield context
    context.dispose()


# ─────────────────────────────────────────
# Page Object Fixture
# ─────────────────────────────────────────

@pytest.fixture(scope='function')
def naver_main_page(page) -> NaverMainPage:
    """NaverMainPage 인스턴스를 제공하는 fixture"""
    return NaverMainPage(page)


@pytest.fixture(scope='function')
def naver_search_result_page(page) -> NaverSearchResultPage:
    """NaverSearchResultPage 인스턴스를 제공하는 fixture"""
    return NaverSearchResultPage(page)


# ─────────────────────────────────────────
# API Client Fixture
# ─────────────────────────────────────────

@pytest.fixture(scope='function')
def naver_api_client(api_request_context: APIRequestContext, settings: Settings) -> NaverApiClient:
    """NaverApiClient 인스턴스를 제공하는 fixture"""
    return NaverApiClient(api_request_context, settings)


# ─────────────────────────────────────────
# pytest-bdd 훅: 실패 시 스크린샷 첨부
# ─────────────────────────────────────────

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 실패 시 스크린샷을 캡처하여 Allure 리포트에 첨부한다"""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        # 'page' fixture가 있는 테스트(UI 테스트)에서만 스크린샷 시도
        page = item.funcargs.get('page')
        if page:
            try:
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name=f'실패 스크린샷 - {item.name}',
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info(f'실패 스크린샷 첨부: {item.name}')
            except Exception as e:
                logger.warning(f'스크린샷 캡처 실패: {e}')
