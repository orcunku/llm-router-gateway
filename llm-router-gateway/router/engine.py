from pydantic import BaseModel
from router.classifier import ComplexityClassifier

class RequestMetaData(BaseModel):
    prompt: str
    max_latency_ms: int = 2000
    privacy_restricted: bool = False
    context_length: int = 0

class AdaptiveRouter:
    def __init__(self):
        self.classifier = ComplexityClassifier()

    def route(self, req: RequestMetaData) -> str:
        # Rule 1: Strict local/private requirement
        if req.privacy_restricted:
            return "hf-qwen-0.5b"

        # Rule 2: Large Context SLA
        if req.context_length > 32000 or len(req.prompt.split()) > 4000:
            return "gemini-flash"

        complexity = self.classifier.estimate(req.prompt)

        # Rule 3: Low Latency SLA or simple complexity -> Micro/Speed tier
        if req.max_latency_ms < 300 or complexity < 0.3:
            return "groq-llama-8b"

        # Rule 4: High complexity reasoning -> Frontier tier
        if complexity > 0.70:
            return "groq-llama-70b"

        # Default Mid-Tier
        return "groq-llama-8b"