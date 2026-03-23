const form = document.getElementById("query-form");
const queryInput = document.getElementById("query-input");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusEl.textContent = "Running...";
  resultEl.textContent = "";

  try {
    const response = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: queryInput.value,
        mode: "simple",
        resource_filter: [],
        save_md_report: true,
      }),
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "request failed");
    }

    resultEl.textContent = [
      `Answer:\n${payload.answer || ""}`,
      payload.normalized_query ? `\nNormalized Query:\n${payload.normalized_query}` : "",
      payload.query_id ? `\nQuery ID:\n${payload.query_id}` : "",
    ].filter(Boolean).join("\n");
    statusEl.textContent = "Done";
  } catch (error) {
    resultEl.textContent = `Error: ${error.message}`;
    statusEl.textContent = "Failed";
  }
});
