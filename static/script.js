// タグボタンを押したときに検索する
function searchByTag(tag) {
    axios.post("/search", { tag: tag }) // タグをサーバーに送信
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
                        <p>データ元: ${poem["データ元"]} | 年齢: ${poem["年齢"]} | 居住地: ${poem["在住地"]} | AIタグ：${poem["AIタグ"].join(', ')}</p>
                    `;
                    resultsDiv.appendChild(div);
                });
            }
        })
        .catch(error => console.error("Error:", error));
}