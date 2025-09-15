"""Simple replacement for ConversationStats after server removal."""

from openhands.llm.metrics import Metrics
from openhands.storage.files import FileStore


class ConversationStats:
    """Simple no-op replacement for ConversationStats."""

    def __init__(self, file_store: FileStore, sid: str, user_id: str | None):
        self.file_store = file_store
        self.sid = sid
        self.user_id = user_id
        self._metrics = Metrics()

    def register_llm(self, llm):
        """Register an LLM for stats tracking (no-op)."""
        pass

    def get_combined_metrics(self) -> Metrics:
        """Return empty metrics."""
        return self._metrics

    def save_metrics(self):
        """Save metrics (no-op)."""
        pass