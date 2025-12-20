const send = document.getElementById("send");
const clear = document.getElementById("clear");
const result_animation_tag = document.getElementById("result_animation");
const article_tag = document.getElementById("article");
const result_tag = document.getElementById("result");

const postSummary = async (article) => {
  const response = await fetch("/summary", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ article }),
  });

  if (!response.ok) {
    throw new Error("요청에 실패했습니다.");
  }

  return response.json();
};

send.addEventListener("click", async () => {
  try {
    result_animation_tag.innerHTML =
      '<img src="/static/images/progress.gif" style="width:5%;margin-top:0px;">';
    result_animation_tag.style.display = "block";

    const response = await postSummary(article_tag.value);

    result_tag.value = response.res;
    result_tag.style.display = "block";
  } catch (error) {
    console.error("Error:", error);
    alert("Error:" + error);
  } finally {
    result_animation_tag.innerHTML = "";
  }
});

clear.addEventListener("click", function () {
  article_tag.value = "";
  article_tag.focus();
});
