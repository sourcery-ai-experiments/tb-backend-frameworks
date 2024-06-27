from abc import ABC, abstractmethod
from typing import Any, Dict

class DatabaseInterface(ABC):
    @abstractmethod
    def create(self, item: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def read(self, key: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update(self, key: Dict[str, Any], update_values: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def delete(self, key: Dict[str, Any]) -> None:
        pass
    