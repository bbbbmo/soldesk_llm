import { handleClick, handlePost } from "./utils/handlePost.js";

const send = document.getElementById("send");
const processing_tag = document.getElementById("processing");

const onClickSendBtn = async () => {
  let tags = document.querySelectorAll("[name='recommend']");
  let values = []; // 전체 이미지의 값, 서버로 전달
  let pick_count = 0; // 선택한 이미지 카운터,5개까지만
  for (let i = 0; i < tags.length; i++) {
    // 25번 순환
    let tag = tags[i]; // 태그 추출
    let pick = tag.getAttribute("data-value"); // 0 (기본값), 1(선택시)
    values.push(pick); // 태그의 기본값인 0과 이미지 선택시 1로 변경된 값이 할당됨.

    if (pick == 1) {
      // 선택한 이미지이면 카운터 증가
      pick_count = pick_count + 1;
    }
  }

  if (pick_count == 5) {
    // 이미지가 5개 선택되면 다음으로 자동 진행
    let movie = values.join(","); // 배열의 값을 ','로 연결,[1,0,1]=>"1,0,1"
    console.log("-> movie: " + movie);
    const data = await handlePost("/movie", { movie: movie });

    document.querySelector("#result").innerHTML = "<h3>" + data.res + "</h3>";
    document.querySelector("#processing").innerHTML = "";
  } else if (pick_count > 5) {
    // 이미지가 5개 이상 선택되면 메시지 출력
    document.getElementById("processing").innerHTML =
      "<br>이미지 선택은 5개만 가능합니다.<br>";
  } else {
    document.getElementById("processing").innerHTML =
      "<br>이미지 선택이 부족합니다.<br>";
  }
};

send.addEventListener(
  "click",
  async () => await handleClick(processing_tag, onClickSendBtn)
);
