# language: ko
기능: 네이버 오픈 API 블로그 검색
  네이버 오픈 API를 통해 블로그 검색이 정상 동작한다
  (NAVER_CLIENT_ID 및 NAVER_CLIENT_SECRET .env 설정 필요)

  @api
  시나리오: 블로그 검색 API 호출 시 정상 응답을 받는다
    조건 유효한 네이버 오픈 API 인증 정보가 설정되어 있다
    만약 "playwright" 키워드로 블로그 검색 API를 호출한다
    그러면 응답 상태 코드는 200 이다
    그리고 응답 본문에 "items" 필드가 존재한다
    그리고 응답 본문의 "items" 목록이 비어있지 않다

  @api
  시나리오 개요: 다양한 키워드로 블로그 검색 API를 호출할 수 있다
    조건 유효한 네이버 오픈 API 인증 정보가 설정되어 있다
    만약 "<키워드>" 키워드로 블로그 검색 API를 호출한다
    그러면 응답 상태 코드는 200 이다

    예:
      | 키워드      |
      | python      |
      | selenium    |
      | playwright  |
