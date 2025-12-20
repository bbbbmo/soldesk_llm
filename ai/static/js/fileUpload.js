import { handleClick, handlePost } from "./utils/handlePost.js";

const send = document.getElementById("send");
const msg = document.getElementById("msg");
const processing_tag = document.getElementById("processing");

const onClickSendBtn = async () => {
  const formData = new FormData();

  const cnt = document.getElementById("file").files.length;
  const files = document.getElementById("file").files;

  if (cnt == 0) {
    msg.innerHTML = '<span style="color: red">파일 선택이 안되었습니다.</span>';
    return; // 실행 종료
  }

  for (let i = 0; i < cnt; i++) {
    formData.append("file", files[i]);
  }

  await fetch("/fileupload", {
    method: "POST",
    body: formData,
  });
};

send.addEventListener(
  "click",
  async () => await handleClick(processing_tag, onClickSendBtn)
);
