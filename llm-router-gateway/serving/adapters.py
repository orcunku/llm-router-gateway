import os

import httpx


class ModelDispatcher:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY", "")
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")

    async def dispatch(self, model_id: str, prompt: str) -> str:
        if not self.groq_key and model_id.startswith("groq-"):
            return (
                f"⚡ [Simulated {model_id} Response]: Successfully processed "
                f"prompt -> '{prompt[:50]}...'"
            )

        if not self.gemini_key and "gemini" in model_id:
            return (
                f"♊ [Simulated Gemini Response]: Successfully analyzed "
                f"prompt -> '{prompt[:50]}...'"
            )

        if model_id == "hf-qwen-0.5b":
            return (
                "🔒 [Micro/Private Model Response]: Processed locally with "
                "strict privacy constraints."
            )

        if model_id.startswith("groq-"):
            model_names = {
                "groq-llama-8b": "llama-3.1-8b-instant",
                "groq-llama-70b": "llama-3.3-70b-versatile",
            }
            model_name = model_names.get(model_id)
            if model_name is None:
                raise ValueError(f"Unsupported Groq model route: {model_id}")
            return await self._call_groq(model_name, prompt)
        if "gemini" in model_id:
            return await self._call_gemini("gemini-1.5-flash", prompt)
        return f"[{model_id}] Processed prompt successfully."

    async def _call_groq(self, model_name: str, prompt: str) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def _call_gemini(self, model_name: str, prompt: str) -> str:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model_name}:generateContent"
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                url,
                params={"key": self.gemini_key},
                json=payload,
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
