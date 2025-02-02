document.getElementById("search-form").addEventListener("submit", (e) => {
    e.preventDefault(); // フォーム送信のデフォルト動作を無効化
    const query = document.getElementById("search-input").value;

    axios.post("/search", { query })
        .then(response => {
            const results = response.data;
            const resultsDiv = document.getElementById("results");
            resultsDiv.innerHTML = "";

            if (results.length === 0) {
                resultsDiv.innerHTML = "<p>該当する句が見つかりませんでした。</p>";
            } else {
                results.forEach(poem => {
                    const div = document.createElement("div");
                    div.classList.add("result-item");
                    div.innerHTML = `
                        <p><strong>${poem["句"]}</strong></p>
                        <p>データ元: ${poem["データ元"]} | 年齢: ${poem["年齢"]} | 居住地: ${poem["在住地"]}</p>
                    `;
                    resultsDiv.appendChild(div);
                });
            }
        })
        .catch(error => console.error("Error:", error));
});