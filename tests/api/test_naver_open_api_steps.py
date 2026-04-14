import allure
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import APIResponse

from api_clients.naver_api_client import NaverApiClient
from config.settings import Settings

# 이 파일에서 처리할 feature 파일 연결
scenarios('api/naver_open_api.feature')


# ─────────────────────────────────────────
# Given (사전 조건)
# ─────────────────────────────────────────

@allure.step('유효한 네이버 오픈 API 인증 정보가 설정되어 있다')
@given('유효한 네이버 오픈 API 인증 정보가 설정되어 있다')
def step_check_credentials(settings: Settings):
    """인증 정보가 없으면 테스트를 건너뛴다

    .env 에 NAVER_CLIENT_ID, NAVER_CLIENT_SECRET 가 설정되어 있어야 한다.
    """
    if not settings.has_naver_api_credentials:
        pytest.skip(
            '네이버 오픈 API 인증 정보가 설정되어 있지 않습니다. '
            '.env 파일에 NAVER_CLIENT_ID, NAVER_CLIENT_SECRET 를 설정하세요.'
        )


# ─────────────────────────────────────────
# When (실행 액션)
# ─────────────────────────────────────────

@allure.step('"{keyword}" 키워드로 블로그 검색 API를 호출한다')
@when(parsers.parse('"{keyword}" 키워드로 블로그 검색 API를 호출한다'), target_fixture='api_response')
def step_call_blog_search(naver_api_client: NaverApiClient, keyword: str) -> APIResponse:
    """네이버 블로그 검색 API를 호출하고 응답을 반환한다"""
    return naver_api_client.search_blog(query=keyword)


# ─────────────────────────────────────────
# Then (결과 검증)
# ─────────────────────────────────────────

@allure.step('응답 상태 코드는 {status_code:d} 이다')
@then(parsers.parse('응답 상태 코드는 {status_code:d} 이다'))
def step_assert_status_code(api_response: APIResponse, status_code: int):
    """HTTP 응답 상태 코드를 검증한다"""
    assert api_response.status == status_code, \
        f'기대 상태 코드: {status_code}, 실제: {api_response.status}'


@allure.step('응답 본문에 "items" 필드가 존재한다')
@then('응답 본문에 "items" 필드가 존재한다')
def step_assert_items_field(api_response: APIResponse):
    """응답 JSON 에 items 키가 존재하는지 확인한다"""
    body = api_response.json()
    assert 'items' in body, f'"items" 필드가 없습니다. 응답 키: {list(body.keys())}'


@allure.step('응답 본문의 "items" 목록이 비어있지 않다')
@then('응답 본문의 "items" 목록이 비어있지 않다')
def step_assert_items_not_empty(api_response: APIResponse):
    """items 배열이 최소 1개 이상의 항목을 포함하는지 확인한다"""
    body = api_response.json()
    items = body.get('items', [])
    assert len(items) > 0, '검색 결과(items)가 비어있습니다'
