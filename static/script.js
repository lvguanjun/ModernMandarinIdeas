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
    alert("网络错误，请稍后再试！");
    return;
  }
  const data = await response.json();
  document.getElementById("loading").style.display = "none";
  document.getElementById("svgContainer").innerHTML = data.svg;
}
