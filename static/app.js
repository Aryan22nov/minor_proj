function upload() {
  const fileInput = document.getElementById("imageInput");
  const resultDiv = document.getElementById("result");
  const predictButton = document.getElementById("predictButton");

  if (!fileInput.files.length) {
    resultDiv.textContent = "Please select an image first.";
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("image", file);

  predictButton.disabled = true;
  resultDiv.textContent = "Predicting…";

  fetch("/predict", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        resultDiv.textContent = `Error: ${data.error}`;
        return;
      }

      resultDiv.innerHTML = `
        <strong>Prediction:</strong> ${data.disease}<br />
        <strong>Confidence:</strong> ${(data.confidence * 100).toFixed(1)}%<br />
        <strong>Scores:</strong> ${Object.entries(data.scores)
          .map(([k, v]) => `${k}: ${(v * 100).toFixed(1)}%`)
          .join(" · ")}
      `;
    })
    .catch((err) => {
      resultDiv.textContent = `Request failed: ${err.message}`;
    })
    .finally(() => {
      predictButton.disabled = false;
    });
}
