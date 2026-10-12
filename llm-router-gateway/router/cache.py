import hashlib
import json
import numpy as np
import redis
from sentence_transformers import SentenceTransformer

class PromptCache:
    def __init__(self, redis_host="localhost", redis_port=6379, sim_threshold=0.92):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=False)
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
        self.sim_threshold = sim_threshold

    def _hash(self, prompt: str) -> str:
        return hashlib.sha256(prompt.strip().lower().encode()).hexdigest()

    def get_exact(self, prompt: str):
        key = f"exact:{self._hash(prompt)}"
        val = self.r.get(key)
        if val:
            return json.loads(val.decode("utf-8"))
        return None

    def set_exact(self, prompt: str, response_text: str, ttl: int = 3600):
        key = f"exact:{self._hash(prompt)}"
        self.r.setex(key, ttl, json.dumps({"response": response_text, "cached": True, "type": "exact"}))

    def get_semantic(self, prompt: str):
        query_emb = self.encoder.encode(prompt)
        keys = self.r.keys("sem:*")
        
        best_match = None
        highest_sim = -1.0

        for key in keys:
            raw = self.r.get(key)
            if not raw:
                continue
            data = json.loads(raw.decode("utf-8"))
            stored_emb = np.array(data["embedding"], dtype=np.float32)
            
            # Cosine similarity calculation
            sim = np.dot(query_emb, stored_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(stored_emb))
            if sim > highest_sim:
                highest_sim = sim
                best_match = data["response"]

        if highest_sim >= self.sim_threshold:
            return {"response": best_match, "cached": True, "type": "semantic", "similarity": float(highest_sim)}
        return None

    def set_semantic(self, prompt: str, response_text: str, ttl: int = 3600):
        emb = self.encoder.encode(prompt).tolist()
        key = f"sem:{self._hash(prompt)}"
        payload = {"embedding": emb, "response": response_text}
        self.r.setex(key, ttl, json.dumps(payload))