let currentStep = 0;
const script = [
  "Welcome! Relying solely on frontier models causes high costs and latency. My router fixes this.",
  "When a request arrives, my classifier evaluates privacy, context length, and query complexity.",
  "Simple requests are routed to fast 8B models, while complex reasoning queries go to large frontier models.",
  "Exact and semantic Redis caching returns matching responses in under 5ms at zero cost!",
  "Check out the live Pareto Frontier: 91%+ quality preserved at over 50% cost savings."
];

function nextChapter() {
  const text = script[currentStep];
  document.getElementById('narrator-text').innerText = text;

  // Web Speech API (Free Native Browser Voice)
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 1.0;
  window.speechSynthesis.speak(utterance);

  currentStep = (currentStep + 1) % script.length;
}

async function sendRequest() {
  const prompt = document.getElementById('prompt-input').value;
  const output = document.getElementById('response-output');
  output.innerText = "Routing request through gateway...";

  try {
    const res = await fetch('http://localhost:8000/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: prompt, max_latency_ms: 1000 })
    });
    const data = await res.json();
    output.innerText = JSON.stringify(data, null, 2);
  } catch (err) {
    output.innerText = "Error: Ensure FastAPI gateway is running on port 8000.";
  }
}