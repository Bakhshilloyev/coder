const API = "http://127.0.0.1:8000";
const logEl = document.getElementById("log");
const input = document.getElementById("input");
const form = document.getElementById("form");
const status = document.getElementById("status");

function append(cls, text) {
  const div = document.createElement("div");
  div.className = cls;
  div.textContent = text;
  logEl.appendChild(div);
  logEl.scrollTop = logEl.scrollHeight;
}

async function checkHealth() {
  try {
    const r = await fetch(`${API}/health`);
    const j = await r.json();
    status.textContent = j.status === "ok" ? "online" : "offline";
  } catch {
    status.textContent = "offline (start server: python -m agent.main server)";
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = input.value.trim();
  if (!msg) return;
  input.value = "";
  append("user", "You: " + msg);
  try {
    const r = await fetch(`${API}/v1/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });
    const j = await r.json();
    append("agent", "Agent: " + (j.reply || JSON.stringify(j)));
  } catch (err) {
    append("agent", "Agent: error contacting API (" + err + ")");
  }
});

checkHealth();
