from datetime import datetime
from typing import Any, Optional


class Record:
    """A class representing a record in a database, allowing for dictionary-like access with typed getters."""

    data: dict
    id: str
    collectionId: str
    createdAt: datetime
    collection: dict

    def __init__(self, data: dict):
        self.data = data.get("data", {})
        self.id = data.get("id", "")
        self.collectionId = data.get("collection_id", "")
        self.createdAt = datetime.fromtimestamp(data.get("created_at", 0))
        self.collection = data.get("collection", {})

    def __repr__(self):
        return f"Record({self.data})"

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def items(self):
        return self.data.items()

    # -----------------------------
    # Typed getter helpers below
    # -----------------------------

    def get_string(self, key: str, raise_error: bool = False) -> Optional[str]:
        value = self.data.get(key)
        try:
            return str(value) if value is not None else None
        except Exception:
            if raise_error:
                raise TypeError(f"Value for '{key}' is not string-convertible: {value}")
            return None

    def get_int(self, key: str, raise_error: bool = False) -> Optional[int]:
        value = self.data.get(key)
        if value is None:
            return None
        try:
            return int(value)
        except Exception:
            if raise_error:
                raise TypeError(f"Value for '{key}' is not int-convertible: {value}")
            return None

    def get_float(self, key: str, raise_error: bool = False) -> Optional[float]:
        value = self.data.get(key)
        if value is None:
            return None
        try:
            return float(value)
        except Exception:
            if raise_error:
                raise TypeError(f"Value for '{key}' is not float-convertible: {value}")
            return None

    def get_bool(self, key: str, raise_error: bool = False) -> Optional[bool]:
        value = self.data.get(key)
        if value is None:
            return None
        try:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                val = value.strip().lower()
                if val in ("true", "1", "yes"):
                    return True
                if val in ("false", "0", "no"):
                    return False
            return bool(int(value))  # for numeric truthiness
        except Exception:
            if raise_error:
                raise TypeError(f"Value for '{key}' is not bool-convertible: {value}")
            return None

    def get_datetime(self, key: str, raise_error: bool = False) -> Optional[datetime]:
        value = self.data.get(key)
        try:
            if isinstance(value, datetime):
                return value
            if isinstance(value, (int, float)):
                return datetime.fromtimestamp(value)
            if isinstance(value, str):
                return datetime.fromisoformat(value)
        except Exception:
            pass
        if raise_error:
            raise TypeError(f"Value for '{key}' is not datetime-convertible: {value}")
        return None
