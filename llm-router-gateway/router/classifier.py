import re

class ComplexityClassifier:
    def estimate(self, prompt: str) -> float:
        score = 0.0
        words = len(prompt.split())
        
        # Word count contribution
        score += min(words / 400.0, 0.4)
        
        # Code block / programming syntax detection
        code_keywords = ["def ", "class ", "import ", "select ", "function", "curl", "docker", "const "]
        if any(k in prompt.lower() for k in code_keywords) or "```" in prompt:
            score += 0.35

        # Complex reasoning triggers
        reasoning_keywords = ["explain step by step", "prove", "math", "evaluate", "compare", "benchmark"]
        if any(k in prompt.lower() for k in reasoning_keywords):
            score += 0.25

        return min(score, 1.0)