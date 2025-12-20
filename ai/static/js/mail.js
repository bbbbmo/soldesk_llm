import { handleClick, handlePost } from "./utils/handlePost";

const send = document.getElementById("send");
const processing_tag = document.getElementById("processing");

const postMail = async () =>
  await handlePost("/mail", {
    subject: document.querySelector("#subject").value,
    recipient_email: document.querySelector("#recipient_email").value,
    message: document.querySelector("#message").value,
  });

send.addEventListener(
  "click",
  handleClick(processing_tag, async () => {
    await postMail();
  })
);
