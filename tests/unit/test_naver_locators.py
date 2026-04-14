"""
NaverLocators 클래스 구조 단위 테스트

Locator 중앙 관리 파일(naver_locators.py)이 올바른 구조를 유지하는지 검증한다.
DOM 변경으로 locator를 수정할 때 누락 없이 업데이트되었는지 회귀 체크에 활용한다.
"""
import pytest
from locators.naver_locators import NaverLocators


class TestNaverLocatorsStructure:
    """NaverLocators 클래스 구조 검증"""

    def test_main_page_locators_exist(self):
        """MainPage nested class 와 필수 locator 존재 여부를 확인한다"""
        assert hasattr(NaverLocators, 'MainPage'), 'MainPage nested class 가 없습니다'
        assert hasattr(NaverLocators.MainPage, 'SEARCH_INPUT'), 'SEARCH_INPUT locator 가 없습니다'
        assert hasattr(NaverLocators.MainPage, 'SEARCH_BUTTON'), 'SEARCH_BUTTON locator 가 없습니다'

    def test_search_result_page_locators_exist(self):
        """SearchResultPage nested class 와 필수 locator 존재 여부를 확인한다"""
        assert hasattr(NaverLocators, 'SearchResultPage'), 'SearchResultPage nested class 가 없습니다'
        assert hasattr(NaverLocators.SearchResultPage, 'RESULT_CONTAINER'), \
            'RESULT_CONTAINER locator 가 없습니다'
        assert hasattr(NaverLocators.SearchResultPage, 'FIRST_RESULT_LINK'), \
            'FIRST_RESULT_LINK locator 가 없습니다'

    def test_locator_values_are_strings(self):
        """모든 locator 값이 문자열 타입인지 확인한다"""
        for attr_name in vars(NaverLocators.MainPage):
            if not attr_name.startswith('_'):
                value = getattr(NaverLocators.MainPage, attr_name)
                assert isinstance(value, str), \
                    f'MainPage.{attr_name} 값이 문자열이 아닙니다: {type(value)}'

        for attr_name in vars(NaverLocators.SearchResultPage):
            if not attr_name.startswith('_'):
                value = getattr(NaverLocators.SearchResultPage, attr_name)
                assert isinstance(value, str), \
                    f'SearchResultPage.{attr_name} 값이 문자열이 아닙니다: {type(value)}'

    def test_locator_values_are_not_empty(self):
        """모든 locator 값이 빈 문자열이 아닌지 확인한다"""
        for attr_name in vars(NaverLocators.MainPage):
            if not attr_name.startswith('_'):
                value = getattr(NaverLocators.MainPage, attr_name)
                assert value.strip(), f'MainPage.{attr_name} 값이 비어 있습니다'

        for attr_name in vars(NaverLocators.SearchResultPage):
            if not attr_name.startswith('_'):
                value = getattr(NaverLocators.SearchResultPage, attr_name)
                assert value.strip(), f'SearchResultPage.{attr_name} 값이 비어 있습니다'

    def test_search_input_selector_format(self):
        """검색 입력창 locator가 CSS ID 선택자 형식인지 확인한다"""
        selector = NaverLocators.MainPage.SEARCH_INPUT
        assert selector.startswith('#'), \
            f'SEARCH_INPUT 은 CSS ID 선택자(#) 여야 합니다. 실제: {selector}'
