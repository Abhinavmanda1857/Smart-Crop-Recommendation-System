
document.getElementById("recommendBtn").addEventListener("click", async (e) => {
    e.preventDefault(); 
    
    const form = document.getElementById("agricultureForm");
    const formData = new FormData(form);
    const resultDiv = document.getElementById("result");
    
    const data = {};
    formData.forEach((value, key) => {
        if (key !== "crop") data[key] = value;
    });
    
    resultDiv.innerText = "🌾 Recommending...";
    
    try {
        const response = await fetch("http://127.0.0.1:5000/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (response.ok) {
            resultDiv.innerText = `🌱 Best Crop: ${result.recommended_crop}, Expected Yield: ${result.expected_yield}`;
        } else {
            resultDiv.innerText = `❌ Recommendation failed: ${result.error || "Unknown error"}`;
        }
    } catch (err) {
        console.error("Recommendation error:", err);
        resultDiv.innerText = "❌ Recommendation failed. Check console for details.";
    }
});

document.querySelector("form button[type='submit']").addEventListener("click", async (e) => {
    e.preventDefault();
    
    const form = document.getElementById("agricultureForm");
    const formData = new FormData(form);
    const resultDiv = document.getElementById("result");
    
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    resultDiv.innerText = "🌾 Predicting yield...";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST", 
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
            resultDiv.innerText = `🌾 Predicted Yield: ${result.prediction}`;
        } else {
            resultDiv.innerText = `❌ Prediction failed: ${result.error || "Unknown error"}`;
        }
    } catch (err) {
        console.error("Prediction error:", err);
        resultDiv.innerText = "❌ Prediction failed. Check console for details.";
    }
});

