from playwright.sync_api import Page
from pages.base_page import BasePage
from locators.naver_locators import NaverLocators
from utils.logger import get_logger

logger = get_logger('naver_search_result_page')


class NaverSearchResultPage(BasePage):
    """네이버 검색 결과 페이지 객체

    https://search.naver.com/search.naver 에 대한 동작을 캡슐화한다.
    Locator는 NaverLocators.SearchResultPage 에서 참조한다.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Locator 참조 (단일 파일 naver_locators.py 에서 관리)
        self._locators = NaverLocators.SearchResultPage

    def wait_for_results(self, timeout: int = 10000) -> None:
        """검색 결과 컨테이너가 표시될 때까지 대기한다"""
        logger.info('검색 결과 로딩 대기')
        self.page.wait_for_selector(
            self._locators.RESULT_CONTAINER,
            timeout=timeout
        )

    def is_on_search_result_page(self) -> bool:
        """현재 페이지가 검색 결과 페이지인지 확인한다"""
        return 'search.naver.com' in self.current_url()

    def get_result_count(self) -> int:
        """검색 결과 제목 항목의 수를 반환한다"""
        elements = self.page.query_selector_all(self._locators.RESULT_TITLES)
        count = len(elements)
        logger.info(f'검색 결과 수: {count}')
        return count

    def click_first_result(self) -> None:
        """첫 번째 검색 결과 링크를 클릭한다

        target="_blank" 링크이므로 새 탭이 열린다.
        새 탭을 캡처하여 self.page를 교체한다.
        """
        logger.info('첫 번째 검색 결과 클릭')
        first_link = self.page.locator(self._locators.FIRST_RESULT_LINK).first
        with self.page.context.expect_page() as new_page_info:
            first_link.click()
        new_page = new_page_info.value
        new_page.wait_for_load_state('domcontentloaded')
        # 새 탭으로 page 교체하여 이후 URL 검증이 새 탭 기준으로 동작
        self.page = new_page

    def search_again(self, keyword: str) -> None:
        """결과 페이지에서 새로운 키워드로 재검색한다"""
        logger.info(f'재검색: "{keyword}"')
        self.page.fill(self._locators.SEARCH_INPUT, keyword)
        self.page.click(self._locators.SEARCH_BUTTON)
        self.page.wait_for_load_state('domcontentloaded')
