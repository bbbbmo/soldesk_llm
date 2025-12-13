const send = document.getElementById("send");
const result_animation_tag = document.getElementById("result_animation");

send.addEventListener("click", function () {
  // 처리중 animation
  result_animation_tag.innerHTML =
    '<img src="/static/images/progress.gif" style="width: 15%; margin-top: 0px;">';
});
