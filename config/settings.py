import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# .env 파일 로드 (없으면 무시)
load_dotenv()


@dataclass
class Settings:
    """테스트 실행 환경 설정"""

    # 기본 URL
    base_url: str = field(
        default_factory=lambda: os.getenv('BASE_URL', 'https://www.naver.com')
    )

    # 네이버 오픈 API URL
    openapi_url: str = 'https://openapi.naver.com'

    # 브라우저 타임아웃 (밀리초)
    timeout: int = field(
        default_factory=lambda: int(os.getenv('TIMEOUT', '10000'))
    )

    # 헤드리스 모드
    headless: bool = field(
        default_factory=lambda: os.getenv('HEADLESS', 'true').lower() == 'true'
    )

    # 네이버 오픈 API 인증 정보
    naver_client_id: str | None = field(
        default_factory=lambda: os.getenv('NAVER_CLIENT_ID')
    )
    naver_client_secret: str | None = field(
        default_factory=lambda: os.getenv('NAVER_CLIENT_SECRET')
    )

    @property
    def has_naver_api_credentials(self) -> bool:
        """네이버 오픈 API 인증 정보 존재 여부"""
        return bool(self.naver_client_id and self.naver_client_secret)
