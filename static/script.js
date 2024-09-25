async function fetchSVG() {
  const word = document.getElementById("wordInput").value;
  if (!word) {
    alert("请输入一个词语！");
    return;
  }
  document.getElementById("loading").style.display = "block";
  const response = await fetch("/explain", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ word: word }),
  });
  if (!response.ok) {
    document.getElementById("loading").style.display = "none";
    // 尝试 json 序列化响应体，以获取错误信息
    try {
      const errorData = await response.json();
      alert(`${errorData.error}`);
    } catch (e) {
      alert("请求失败，稍后再试。");
    }
  }
  const data = await response.json();
  document.getElementById("loading").style.display = "none";
  document.getElementById("svgContainer").innerHTML = data.svg;
}
