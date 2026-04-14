from playwright.sync_api import APIRequestContext, APIResponse
from utils.logger import get_logger

logger = get_logger('base_api_client')


class BaseApiClient:
    """Playwright APIRequestContext 기반 공통 API 클라이언트

    모든 API 클라이언트는 이 클래스를 상속받아 사용한다.
    공통 헤더 설정, 응답 로깅, 에러 처리를 제공한다.
    """

    def __init__(self, request_context: APIRequestContext, base_url: str) -> None:
        self._context = request_context
        self._base_url = base_url.rstrip('/')

    def _build_url(self, path: str) -> str:
        """base_url과 path를 합쳐 전체 URL을 구성한다"""
        return f'{self._base_url}/{path.lstrip("/")}'

    def get(self, path: str, **kwargs) -> APIResponse:
        """GET 요청을 전송하고 응답을 반환한다

        Args:
            path: 엔드포인트 경로 (예: '/v1/search/blog.json')
            **kwargs: Playwright fetch() 추가 파라미터 (headers, params 등)

        Returns:
            APIResponse 객체
        """
        url = self._build_url(path)
        logger.info(f'GET 요청: {url}')
        response = self._context.get(url, **kwargs)
        logger.info(f'응답 상태: {response.status}')
        return response

    def post(self, path: str, **kwargs) -> APIResponse:
        """POST 요청을 전송하고 응답을 반환한다

        Args:
            path: 엔드포인트 경로
            **kwargs: Playwright fetch() 추가 파라미터 (headers, data 등)

        Returns:
            APIResponse 객체
        """
        url = self._build_url(path)
        logger.info(f'POST 요청: {url}')
        response = self._context.post(url, **kwargs)
        logger.info(f'응답 상태: {response.status}')
        return response
