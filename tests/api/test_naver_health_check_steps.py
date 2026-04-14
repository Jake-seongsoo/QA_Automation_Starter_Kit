import allure
import pytest
from pytest_bdd import scenarios, when, then, parsers
from playwright.sync_api import APIResponse

from api_clients.naver_api_client import NaverApiClient

# 이 파일에서 처리할 feature 파일 연결
scenarios('api/naver_health_check.feature')


# ─────────────────────────────────────────
# When (실행 액션)
# ─────────────────────────────────────────

@allure.step('"{url}" 에 GET 요청을 보낸다')
@when(parsers.parse('"{url}" 에 GET 요청을 보낸다'), target_fixture='api_response')
def step_get_request(naver_api_client: NaverApiClient, url: str) -> APIResponse:
    """지정한 URL에 GET 요청을 전송하고 응답을 반환한다"""
    return naver_api_client.health_check()


# ─────────────────────────────────────────
# Then (결과 검증)
# ─────────────────────────────────────────

@allure.step('응답 상태 코드는 {status_code:d} 이다')
@then(parsers.parse('응답 상태 코드는 {status_code:d} 이다'))
def step_assert_status_code(api_response: APIResponse, status_code: int):
    """HTTP 응답 상태 코드를 검증한다"""
    assert api_response.status == status_code, \
        f'기대 상태 코드: {status_code}, 실제: {api_response.status}'


@allure.step('Content-Type 헤더에 "{content_type}" 이 포함된다')
@then(parsers.parse('Content-Type 헤더에 "{content_type}" 이 포함된다'))
def step_assert_content_type(api_response: APIResponse, content_type: str):
    """Content-Type 응답 헤더에 지정한 값이 포함되어 있는지 검증한다"""
    actual = api_response.headers.get('content-type', '')
    assert content_type in actual, \
        f'Content-Type 헤더에 "{content_type}" 이 없습니다. 실제 값: {actual}'
