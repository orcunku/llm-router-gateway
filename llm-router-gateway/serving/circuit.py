import time

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time_sec: int = 30):
        self.threshold = failure_threshold
        self.recovery = recovery_time_sec
        self.failures = {}
        self.last_failure = {}

    def is_available(self, model_id: str) -> bool:
        if self.failures.get(model_id, 0) >= self.threshold:
            if time.time() - self.last_failure.get(model_id, 0) < self.recovery:
                return False  # Breaker OPEN (Unhealthy backend)
            self.failures[model_id] = 0  # Recover
        return True

    def record_failure(self, model_id: str):
        self.failures[model_id] = self.failures.get(model_id, 0) + 1
        self.last_failure[model_id] = time.time()

    def record_success(self, model_id: str):
        self.failures[model_id] = 0