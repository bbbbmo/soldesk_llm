let msg = document.getElementById("msg");

send.addEventListener("click", function () {
  // 선택한 파일 데이터 저장 ★

  // 태그 id가 'file'인 태그의 파일 갯수

  if (cnt == 0) {
    msg.innerHTML = '<span style="color: red">파일 선택이 안되었습니다.</span>';
    return; // 실행 종료
  }

  // 파일이 있으면 파일 객체를 FormData 클래스의 객체에 저장

  // form 객체에 file이란 이름으로 파일 객체 저장 ★

  msg.innerHTML =
    '<img src="/static/images/progress.gif" style="width: 15%; margin-top: 0px;">';
  //비동기 통신(업로드)
  //응답처리한것을 다시 받는다.
});
