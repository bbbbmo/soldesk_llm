const send = document.getElementById("send");
const result_animation_tag = document.getElementById("result_animation");

const postTranslator = async () =>
  await handlePost("/translator", {
    sentence: sentence.value,
    language: language.value,
    age: age.value,
  });

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
