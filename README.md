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

## Deploy to Streamlit Community Cloud

1. Push the repository to GitHub.
2. Create a Community Cloud app using
   `llm-router-gateway/web/app_streamlit.py` as the main file.
3. The app is a public routing preview. Visitors can try prompts and see the
   selected route without calling FastAPI, sending prompts to model providers,
   or configuring any API keys. The page explicitly labels this as a routing
   preview rather than a generated model response.
4. The public preview requires no Streamlit secrets. If you later enable live
   model responses, deploy FastAPI separately to a public HTTPS host and keep
   `API_AUTH_TOKEN`, `GROQ_API_KEY`, and `GEMINI_API_KEY` as environment
   variables on that backend only. Never put provider keys in the Streamlit
   page or GitHub.

Never commit real tokens, provider keys, or `.streamlit/secrets.toml`.
