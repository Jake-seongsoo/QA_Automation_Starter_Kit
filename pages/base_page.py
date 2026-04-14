import allure
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger('base_page')


class BasePage:
    """모든 페이지 객체의 기반 클래스

    공통 동작(페이지 이동, 로딩 대기, 스크린샷)을 제공한다.
    모든 페이지 클래스는 이 클래스를 상속받는다.
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        """지정한 URL로 이동한다"""
        logger.info(f'페이지 이동: {url}')
        self.page.goto(url)

    def wait_for_load(self) -> None:
        """페이지 로딩이 완료될 때까지 대기한다"""
        self.page.wait_for_load_state('domcontentloaded')

    def title(self) -> str:
        """현재 페이지의 제목을 반환한다"""
        return self.page.title()

    def current_url(self) -> str:
        """현재 페이지의 URL을 반환한다"""
        return self.page.url

    def screenshot(self, name: str) -> bytes:
        """스크린샷을 캡처하고 Allure 리포트에 첨부한다"""
        data = self.page.screenshot()
        allure.attach(
            data,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f'스크린샷 캡처: {name}')
        return data

    def wait_for_selector(self, selector: str, timeout: int = 10000) -> None:
        """지정한 선택자가 나타날 때까지 대기한다"""
        self.page.wait_for_selector(selector, timeout=timeout)
