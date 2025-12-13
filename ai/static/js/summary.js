send.addEventListener("click", () => {
  //article 뉴스를 가져와서

  //console.log('article:'+article)
  //처리중 이미지 보여준다.
  animation_tag.innerHTML =
    '<img src="/static/images/progress.gif" style="width:5%;margin-top:0px;">';
  animation_tag.style.display = "block";
  //flask서버에 article 전달(비동기:fetch())
});
clear.addEventListener("click", function () {
  article_tag.value = "";
  article_tag.focus();
});
