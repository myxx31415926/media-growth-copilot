from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAdapter(ABC):

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        pass

    def fetch_comments(self) -> List[Dict[str, Any]]:
        return []
