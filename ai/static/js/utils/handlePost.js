export const handlePost = async (url, data) => {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("요청에 실패했습니다.");
  }

  return response.json();
};

export const handleClick = async (processing_tag, callback) => {
  try {
    processing_tag.innerHTML =
      '<img src="/static/images/progress.gif" style="width: 3%; margin-top: 10px;">';
    await callback();
  } catch (error) {
    console.error("Error:", error);
    alert("Error:" + error);
  } finally {
    processing_tag.innerHTML = "";
  }
};
