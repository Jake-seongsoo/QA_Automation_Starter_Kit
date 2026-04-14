import logging
import sys


def get_logger(name: str = 'qa_automation') -> logging.Logger:
    """한국어 포맷의 로거를 반환한다"""
    logger = logging.getLogger(name)

    # 이미 핸들러가 설정되어 있으면 재사용
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 콘솔 핸들러
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # 한국어 친화 포맷
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# 기본 로거 인스턴스
logger = get_logger()
