import allure
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from pages.naver_main_page import NaverMainPage
from pages.naver_search_result_page import NaverSearchResultPage

# 이 파일에서 처리할 feature 파일 연결
scenarios('ui/naver_search.feature')


# ─────────────────────────────────────────
# Given (사전 조건)
# ─────────────────────────────────────────

@allure.step('사용자가 네이버 메인 페이지에 접속한다')
@given('사용자가 네이버 메인 페이지에 접속한다')
def step_open_naver_main(naver_main_page: NaverMainPage):
    """네이버 메인 페이지를 열고 로딩을 확인한다"""
    naver_main_page.open()
    assert naver_main_page.is_loaded(), '네이버 메인 페이지가 정상 로딩되지 않았습니다'


# ─────────────────────────────────────────
# When (실행 액션)
# ─────────────────────────────────────────

@allure.step('사용자가 "{keyword}" 키워드로 검색한다')
@when(parsers.parse('사용자가 "{keyword}" 키워드로 검색한다'))
def step_search_keyword(naver_main_page: NaverMainPage, keyword: str):
    """검색창에 키워드를 입력하고 검색을 실행한다"""
    naver_main_page.search(keyword)


# ─────────────────────────────────────────
# Then (결과 검증)
# ─────────────────────────────────────────

@allure.step('검색 결과 페이지가 표시된다')
@then('검색 결과 페이지가 표시된다')
def step_assert_search_result_page(naver_search_result_page: NaverSearchResultPage):
    """검색 결과 페이지로 이동했는지 확인한다"""
    naver_search_result_page.wait_for_results()
    assert naver_search_result_page.is_on_search_result_page(), \
        f'검색 결과 페이지가 아닙니다. 현재 URL: {naver_search_result_page.current_url()}'


@allure.step('검색 결과가 1개 이상 존재한다')
@then('검색 결과가 1개 이상 존재한다')
def step_assert_result_count(naver_search_result_page: NaverSearchResultPage):
    """검색 결과가 적어도 1개 이상 표시되는지 확인한다"""
    count = naver_search_result_page.get_result_count()
    assert count >= 1, f'검색 결과가 없습니다. 결과 수: {count}'
