const searchBtn = document.querySelector("#search-btn");
const cityInput = document.querySelector("#city-input");
const resultDiv = document.querySelector("#weather-result");

searchBtn.addEventListener("click", async () => {
  const city = cityInput.value;
  if (!city) return;

  resultDiv.innerHTML = "<p>Loading...</p>";

  try {
    // This is the bridge to your Python FastAPI server!
    const response = await fetch(`http://127.0.0.1:8000/?city=${city}`);
    const data = await response.json();

    if (data.error) {
      resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
    } else {
      resultDiv.innerHTML = `
        <h2>${data.City}</h2>
        <p class="temp">${data.Temperature}°C</p>
        <p class="desc">${data.Description}</p>
      `;
    }
  } catch (err) {
    resultDiv.innerHTML = `<p style="color: red;">Is your Python server running?</p>`;
  }
});