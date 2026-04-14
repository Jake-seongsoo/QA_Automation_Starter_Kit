from playwright.sync_api import Page
from pages.base_page import BasePage
from locators.naver_locators import NaverLocators
from utils.logger import get_logger

logger = get_logger('naver_main_page')


class NaverMainPage(BasePage):
    """네이버 메인 페이지 객체

    https://www.naver.com 에 대한 동작을 캡슐화한다.
    Locator는 NaverLocators.MainPage 에서 참조한다.
    """

    URL = 'https://www.naver.com'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Locator 참조 (단일 파일 naver_locators.py 에서 관리)
        self._locators = NaverLocators.MainPage

    def open(self) -> None:
        """네이버 메인 페이지를 열고 로딩을 대기한다"""
        logger.info('네이버 메인 페이지 접속')
        self.goto(self.URL)
        self.wait_for_load()

    def is_loaded(self) -> bool:
        """메인 페이지가 정상적으로 로딩되었는지 확인한다"""
        return 'NAVER' in self.title().upper()

    def search(self, keyword: str) -> None:
        """검색창에 키워드를 입력하고 검색을 실행한다

        Args:
            keyword: 검색할 키워드 문자열
        """
        logger.info(f'검색 키워드 입력: "{keyword}"')
        # 검색창 클릭 후 입력
        self.page.click(self._locators.SEARCH_INPUT)
        self.page.fill(self._locators.SEARCH_INPUT, keyword)

        # 검색 버튼 클릭
        logger.info('검색 버튼 클릭')
        self.page.click(self._locators.SEARCH_BUTTON)

        # 결과 페이지 로딩 대기
        self.page.wait_for_load_state('domcontentloaded')
