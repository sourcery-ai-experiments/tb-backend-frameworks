from abc import ABC, abstractmethod
from typing import Any, Dict

class DatabaseInterface(ABC):
    """
    DatabaseInterface is an abstract base class that defines a common interface for CRUD operations on a database.
    """

    @abstractmethod
    def create(self, item: Dict[str, Any]) -> None:
        """
        Create a new item in the database.

        :param item: A dictionary representing the item to be created.
        :raises NotImplementedError: This method must be overridden in a subclass.
        """
        ...

    @abstractmethod
    def read(self, key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read an item from the database.

        :param key: A dictionary representing the key of the item to be read.
        :return: A dictionary representing the retrieved item, or an empty dictionary if the item is not found.
        :raises NotImplementedError: This method must be overridden in a subclass.
        """
        ...

    @abstractmethod
    def update(self, key: Dict[str, Any], update_values: Dict[str, Any]) -> None:
        """
        Update an existing item in the database.

        :param key: A dictionary representing the key of the item to be updated.
        :param update_values: A dictionary representing the attributes to be updated and their new values.
        :raises NotImplementedError: This method must be overridden in a subclass.
        """
        ...

    @abstractmethod
    def delete(self, key: Dict[str, Any]) -> None:
        """
        Delete an item from the database.

        :param key: A dictionary representing the key of the item to be deleted.
        :raises NotImplementedError: This method must be overridden in a subclass.
        """
        ...
