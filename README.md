# LLM Router Gateway and Adaptive Router

Multi-model LLM gateway with a Streamlit interface and a separate FastAPI
service. The router chooses a model route based on prompt complexity, latency
target, and privacy settings.

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


