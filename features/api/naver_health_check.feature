# language: ko
기능: 네이버 메인 헬스체크
  네이버 메인 페이지가 정상적으로 응답하는지 확인한다

  @api @smoke
  시나리오: 네이버 메인 페이지가 정상 응답한다
    만약 "https://www.naver.com" 에 GET 요청을 보낸다
    그러면 응답 상태 코드는 200 이다
    그리고 Content-Type 헤더에 "text/html" 이 포함된다
