import allure
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from pages.naver_main_page import NaverMainPage
from pages.naver_search_result_page import NaverSearchResultPage

# 이 파일에서 처리할 feature 파일 연결
scenarios('ui/naver_first_result.feature')


# ─────────────────────────────────────────
# Given (사전 조건)
# ─────────────────────────────────────────

@allure.step('사용자가 네이버 메인 페이지에 접속한다')
@given('사용자가 네이버 메인 페이지에 접속한다', target_fixture='opened_main_page')
def step_open_main_page(naver_main_page: NaverMainPage):
    """네이버 메인 페이지 접속"""
    naver_main_page.open()
    assert naver_main_page.is_loaded()
    return naver_main_page


@allure.step('사용자가 "{keyword}" 키워드로 검색한다')
@given(parsers.parse('사용자가 "{keyword}" 키워드로 검색한다'))
def step_given_search(naver_main_page: NaverMainPage, keyword: str):
    """배경: 특정 키워드로 검색이 완료된 상태"""
    naver_main_page.open()
    naver_main_page.search(keyword)


# ─────────────────────────────────────────
# When (실행 액션)
# ─────────────────────────────────────────

@allure.step('사용자가 "{keyword}" 키워드로 검색한다 (When)')
@when(parsers.parse('사용자가 "{keyword}" 키워드로 검색한다'))
def step_when_search(naver_main_page: NaverMainPage, keyword: str):
    """검색 실행"""
    naver_main_page.search(keyword)


@allure.step('사용자가 첫 번째 검색 결과를 클릭한다')
@when('사용자가 첫 번째 검색 결과를 클릭한다')
def step_click_first_result(naver_search_result_page: NaverSearchResultPage):
    """검색 결과에서 첫 번째 항목을 클릭한다"""
    naver_search_result_page.click_first_result()


# ─────────────────────────────────────────
# Then (결과 검증)
# ─────────────────────────────────────────

@allure.step('검색 결과 페이지가 표시된다')
@then('검색 결과 페이지가 표시된다')
def step_assert_on_result_page(naver_search_result_page: NaverSearchResultPage):
    """검색 결과 페이지 표시 확인"""
    naver_search_result_page.wait_for_results()
    assert naver_search_result_page.is_on_search_result_page(), \
        f'검색 결과 페이지가 아닙니다. 현재 URL: {naver_search_result_page.current_url()}'


@allure.step('URL이 "naver.com" 도메인이 아닌 페이지로 이동한다')
@then('URL이 "naver.com" 도메인이 아닌 페이지로 이동한다')
def step_assert_navigated_away(naver_search_result_page: NaverSearchResultPage):
    """클릭 후 네이버가 아닌 외부 페이지로 이동했는지 확인한다"""
    current = naver_search_result_page.current_url()
    assert 'naver.com' not in current, \
        f'외부 페이지로 이동하지 않았습니다. 현재 URL: {current}'
