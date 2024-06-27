from typing import Any, Dict
from .Interface import DatabaseInterface

class DynamoDBProvider(DatabaseInterface):
    def create(self, item: Dict[str, Any]) -> None:
        pass
    
    def read(self, key: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def update(self, key: Dict[str, Any], update_values: Dict[str, Any]) -> None:
        pass

    def delete(self, key: Dict[str, Any]) -> None:
        pass
    