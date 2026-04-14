"""
네이버 페이지 Locator 중앙 관리 파일

모든 CSS 선택자, XPath, 텍스트 기반 선택자를 이 파일 한 곳에서 관리한다.
페이지 DOM이 변경될 경우 이 파일만 수정하면 전체 테스트에 반영된다.

사용 방법:
    from locators.naver_locators import NaverLocators

    # 메인 페이지 검색 입력창
    NaverLocators.MainPage.SEARCH_INPUT

    # 검색 결과 첫 번째 링크
    NaverLocators.SearchResultPage.FIRST_RESULT_LINK
"""


class NaverLocators:
    """네이버 전체 페이지 Locator 모음"""

    class MainPage:
        """네이버 메인 페이지 (https://www.naver.com)"""

        # 검색 입력창
        SEARCH_INPUT = '#query'

        # 검색 버튼
        SEARCH_BUTTON = 'button.btn_search'

        # 네이버 로고
        LOGO = '.logo_today'

        # 로그인 버튼
        LOGIN_BUTTON = '.link_login'

    class SearchResultPage:
        """네이버 검색 결과 페이지 (https://search.naver.com/search.naver)"""

        # 검색 결과 전체 컨테이너
        RESULT_CONTAINER = '#main_pack'

        # 웹 검색 결과 목록 첫 번째 항목 링크
        FIRST_RESULT_LINK = '.spw_fsolid._fsolid_body a[data-heatmap-target=".link"]'

        # 검색 결과 제목 목록
        RESULT_TITLES = '.spw_fsolid._fsolid_body a[data-heatmap-target=".link"]'

        # 통합검색 탭
        ALL_TAB = '#lnb a[data-tab="all"]'

        # 검색창 (결과 페이지 내)
        SEARCH_INPUT = '#query'

        # 검색 버튼 (결과 페이지 내)
        SEARCH_BUTTON = 'button.bt_search'

        # 검색 결과 수 영역 (지식iN, 블로그 등 섹션)
        SECTION_TITLES = '.source_tit'
