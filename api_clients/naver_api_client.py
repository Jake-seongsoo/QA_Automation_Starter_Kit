import pytest
from playwright.sync_api import APIRequestContext, APIResponse
from api_clients.base_api_client import BaseApiClient
from config.settings import Settings
from utils.logger import get_logger

logger = get_logger('naver_api_client')

# 네이버 오픈 API 엔드포인트
BLOG_SEARCH_PATH = '/v1/search/blog.json'
NAVER_MAIN_URL = 'https://www.naver.com'


class NaverApiClient(BaseApiClient):
    """네이버 API 전용 클라이언트

    Playwright APIRequestContext를 사용하여
    네이버 오픈 API 및 헬스체크 요청을 처리한다.
    """

    def __init__(
        self,
        request_context: APIRequestContext,
        settings: Settings
    ) -> None:
        super().__init__(request_context, settings.openapi_url)
        self._settings = settings

    def _get_auth_headers(self) -> dict:
        """네이버 오픈 API 인증 헤더를 반환한다

        인증 정보가 없으면 테스트를 건너뛴다 (pytest.skip).
        """
        if not self._settings.has_naver_api_credentials:
            pytest.skip(
                '네이버 오픈 API 인증 정보(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET)가 '
                '.env 파일에 설정되지 않았습니다. 테스트를 건너뜁니다.'
            )
        return {
            'X-Naver-Client-Id': self._settings.naver_client_id,
            'X-Naver-Client-Secret': self._settings.naver_client_secret,
        }

    def search_blog(self, query: str, display: int = 10) -> APIResponse:
        """네이버 블로그 검색 API를 호출한다

        Args:
            query: 검색 키워드
            display: 반환할 결과 수 (기본값: 10)

        Returns:
            APIResponse 객체 (JSON 응답 포함)

        Raises:
            pytest.skip: 인증 정보 미설정 시
        """
        logger.info(f'블로그 검색 API 호출: query="{query}"')
        headers = self._get_auth_headers()
        return self.get(
            BLOG_SEARCH_PATH,
            headers=headers,
            params={'query': query, 'display': display}
        )

    def health_check(self) -> APIResponse:
        """네이버 메인 페이지 헬스체크 요청을 보낸다

        별도 인증 없이 naver.com 에 GET 요청을 보내 HTTP 상태를 확인한다.

        Returns:
            APIResponse 객체
        """
        logger.info('네이버 메인 헬스체크 요청')
        # base_url 대신 직접 절대 URL 사용 (오픈 API URL과 다름)
        response = self._context.get(NAVER_MAIN_URL)
        logger.info(f'헬스체크 응답 상태: {response.status}')
        return response
