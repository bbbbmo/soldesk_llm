const send = document.getElementById("send");
const processing_tag = document.getElementById("processing");

const postMail = async (subject, recipient_email, message) => {
  const response = await fetch("/mail", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ subject, recipient_email, message }),
  });

  if (!response.ok) {
    throw new Error("요청에 실패했습니다.");
  }

  return response.json();
};

send.addEventListener("click", async () => {
  try {
    processing_tag.innerHTML =
      '<img src="/static/images/progress.gif" style="width: 3%; margin-top: 10px;">';

    const subject = document.querySelector("#subject").value;
    const recipient_email = document.querySelector("#recipient_email").value;
    const message = document.querySelector("#message").value;

    await postMail(subject, recipient_email, message);
  } catch (error) {
    console.error("Error:", error);
    alert("Error:" + error);
  } finally {
    processing_tag.innerHTML = "";
  }
});
