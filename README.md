# LLM Router Gateway and Adaptive Router

Multi-model LLM gateway with a Streamlit interface and a separate FastAPI
service. The router chooses a model route based on prompt complexity, latency
target, and privacy settings.

LLM Router Gateway and Adaptive Router
I built an interactive demonstration of how an LLM gateway can select a model route based on prompt complexity, latency requirements, prompt size, and privacy settings. The project uses Streamlit for the public interface and FastAPI for a separate backend, with routing logic that distinguishes simple, complex, and privacy-restricted requests. I also created sample prompts, benchmark visualizations, and an interactive 3D project guide with browser-based narration.

The public demo is deliberately credential-free: it runs the routing logic and shows the selected route, but does not send prompts to AI providers or generate model answers. The separate backend is designed for optional provider integrations, with bearer-token authentication and provider keys kept in server environment variables. This project gave me hands-on experience with API design, routing logic, interactive UI development, and safe handling of credentials.

## Run locally

From this repository's root:

```bash
cd llm-router-gateway
python -m pip install -r web/requirements.txt
python -m pip install -r requirements.txt
```

Set a random `API_AUTH_TOKEN` in the environment for both services, then start
the FastAPI gateway:

```bash
cd llm-router-gateway
uvicorn main:app --host 0.0.0.0 --port 8000
```

In a second terminal, set `API_BASE_URL=http://127.0.0.1:8000` and the same
`API_AUTH_TOKEN`, then start Streamlit from the repository root:

```bash
streamlit run llm-router-gateway/web/app_streamlit.py
```

`GROQ_API_KEY` and `GEMINI_API_KEY` are optional. Without provider keys, the
gateway returns demo responses for those routes.


