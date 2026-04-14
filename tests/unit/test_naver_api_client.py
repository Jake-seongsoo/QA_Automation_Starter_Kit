"""
NaverApiClient 단위 테스트

실제 네트워크 요청 없이 NaverApiClient 의 동작을 검증한다.
monkeypatch 를 사용해 APIRequestContext 를 mock 처리한다.
"""
import pytest
from unittest.mock import MagicMock, patch

from api_clients.naver_api_client import NaverApiClient
from config.settings import Settings


@pytest.fixture
def mock_settings_with_credentials():
    """인증 정보가 있는 Settings mock"""
    settings = MagicMock(spec=Settings)
    settings.openapi_url = 'https://openapi.naver.com'
    settings.naver_client_id = 'test_client_id'
    settings.naver_client_secret = 'test_client_secret'
    settings.has_naver_api_credentials = True
    return settings


@pytest.fixture
def mock_settings_without_credentials():
    """인증 정보가 없는 Settings mock"""
    settings = MagicMock(spec=Settings)
    settings.openapi_url = 'https://openapi.naver.com'
    settings.naver_client_id = None
    settings.naver_client_secret = None
    settings.has_naver_api_credentials = False
    return settings


@pytest.fixture
def mock_request_context():
    """Playwright APIRequestContext mock"""
    return MagicMock()


class TestNaverApiClientInit:
    """NaverApiClient 초기화 테스트"""

    def test_client_initializes_with_settings(
        self, mock_request_context, mock_settings_with_credentials
    ):
        """Settings를 받아 클라이언트가 정상 생성되는지 확인한다"""
        client = NaverApiClient(mock_request_context, mock_settings_with_credentials)
        assert client is not None

    def test_base_url_is_set_from_settings(
        self, mock_request_context, mock_settings_with_credentials
    ):
        """base_url 이 settings.openapi_url 에서 올바르게 설정되는지 확인한다"""
        client = NaverApiClient(mock_request_context, mock_settings_with_credentials)
        assert client._base_url == 'https://openapi.naver.com'


class TestNaverApiClientSearchBlog:
    """search_blog 메서드 테스트"""

    def test_search_blog_sends_get_request(
        self, mock_request_context, mock_settings_with_credentials
    ):
        """search_blog 호출 시 GET 요청이 전송되는지 확인한다"""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_request_context.get.return_value = mock_response

        client = NaverApiClient(mock_request_context, mock_settings_with_credentials)
        response = client.search_blog('playwright')

        # GET 요청이 1회 호출되었는지 확인
        mock_request_context.get.assert_called_once()

    def test_search_blog_includes_auth_headers(
        self, mock_request_context, mock_settings_with_credentials
    ):
        """인증 헤더(X-Naver-Client-Id, X-Naver-Client-Secret)가 포함되는지 확인한다"""
        mock_response = MagicMock()
        mock_request_context.get.return_value = mock_response

        client = NaverApiClient(mock_request_context, mock_settings_with_credentials)
        client.search_blog('playwright')

        call_kwargs = mock_request_context.get.call_args.kwargs
        headers = call_kwargs.get('headers', {})
        assert 'X-Naver-Client-Id' in headers, 'X-Naver-Client-Id 헤더가 없습니다'
        assert 'X-Naver-Client-Secret' in headers, 'X-Naver-Client-Secret 헤더가 없습니다'

    def test_search_blog_skips_when_no_credentials(
        self, mock_request_context, mock_settings_without_credentials
    ):
        """인증 정보가 없으면 pytest.skip 이 호출되는지 확인한다"""
        client = NaverApiClient(mock_request_context, mock_settings_without_credentials)

        with pytest.raises(pytest.skip.Exception):
            client.search_blog('playwright')


class TestNaverApiClientHealthCheck:
    """health_check 메서드 테스트"""

    def test_health_check_sends_get_to_naver_main(
        self, mock_request_context, mock_settings_with_credentials
    ):
        """health_check 가 naver.com 으로 GET 요청을 보내는지 확인한다"""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_request_context.get.return_value = mock_response

        client = NaverApiClient(mock_request_context, mock_settings_with_credentials)
        response = client.health_check()

        # GET 요청 URL 확인
        call_args = mock_request_context.get.call_args
        url = call_args.args[0] if call_args.args else call_args.kwargs.get('url', '')
        assert 'naver.com' in url, f'naver.com URL 로 요청하지 않았습니다. 실제: {url}'

    def test_health_check_returns_response(
        self, mock_request_context, mock_settings_with_credentials
    ):
        """health_check 가 APIResponse 를 반환하는지 확인한다"""
        mock_response = MagicMock()
        mock_response.status = 200
        mock_request_context.get.return_value = mock_response

        client = NaverApiClient(mock_request_context, mock_settings_with_credentials)
        result = client.health_check()

        assert result is not None
        assert result.status == 200
