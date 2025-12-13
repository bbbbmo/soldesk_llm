// click 이벤트 설정
send.addEventListener("click", () => {
  //form data  가져오기, 메일제목, 받는 이메일 주소, 메일내용
  let recipient_email =
    //처리중 이미지 보여주기
    (document.getElementById("processing").innerHTML =
      '<img src="/static/images/progress.gif" style="width: 3%; margin-top: 10px;">');

  // 서버와 비동기 통신 (폼데이터 전달 => 결과 받아서 처리)
}); //클릭 이벤트 설정 end
