const send = document.getElementById("send");
const result_animation_tag = document.getElementById("result_animation");

const postTranslator = async (sentence, language, age) => {
  const response = await fetch("/translator", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ sentence, language, age }),
  });

  if (!response.ok) {
    throw new Error("요청에 실패했습니다.");
  }

  return response.json();
};

send.addEventListener("click", async () => {
  try {
    result_animation_tag.innerHTML =
      '<img src="/static/images/progress.gif" style="width: 15%; margin-top: 0px;">';

    const sentence = document.getElementById("sentence").value;
    const language = document.getElementById("language").value;
    const age = document.getElementById("age").value;

    const response = await postTranslator(sentence, language, age);

    const translatedText = response.res.replace(/\\n/g, "\n");
    document.getElementById("result").value = translatedText;
  } catch (error) {
    console.error("Error:", error);
    alert("Error:" + error);
  } finally {
    result_animation_tag.innerHTML = "";
  }
});
