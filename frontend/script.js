function uploadImage() {
  let input = document.getElementById("imageInput");
  if (input.files.length === 0) {
    alert("Please upload an image");
    return;
  }

  let file = input.files[0];
  let img = new Image();
  let canvas = document.getElementById("canvas");
  let ctx = canvas.getContext("2d");

  img.onload = function () {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
  };

  img.src = URL.createObjectURL(file);

  let formData = new FormData();
  formData.append("image", file);

  fetch("http://127.0.0.1:5000/detect", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    let output = "";

    data.forEach(d => {
      let [x1, y1, x2, y2] = d.box;
      let label = d.label.toLowerCase();
      let color = "red";

      if (label.includes("helmet")) color = "green";
      else if (label.includes("vest")) color = "blue";
      else if (label.includes("boot")) color = "orange";
      else if (label.includes("person")) color = "purple";
      else if (label.includes("mask")) color = "red";
      else if (label.includes("glove")) color = "cyan";
      else if (label.includes("glass")) color = "yellow";
      else if (label.includes("ear")) color = "pink";

      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

      ctx.fillStyle = color;
      ctx.font = "16px Arial";
      ctx.fillText(
        `${d.label} (${d.confidence})`,
        x1,
        y1 > 20 ? y1 - 5 : y1 + 20
      );

      output += `✔ ${d.label} - ${d.confidence}\n`;
    });

    document.getElementById("result").innerText =
      output || "No PPE detected";
  })
  .catch(() => {
    document.getElementById("result").innerText =
      "Error connecting to backend";
  });
}
