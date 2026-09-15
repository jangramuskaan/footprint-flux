from abc import ABC, abstractmethod
from typing import Any


class Collector(ABC):
    @abstractmethod
    def collect(self) -> list[dict[str, Any]]:
        """Collect raw public footprint data."""
        raise NotImplementedError