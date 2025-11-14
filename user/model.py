# profile/model.py
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

import user


@dataclass(frozen=True)
class User:
    id: str = ""
    name: str = ""
    scenario: str = "normal"
    created_at: str = datetime.now(timezone.utc).isoformat()
    updated_at: str = datetime.now(timezone.utc).isoformat()

    def __repr__(self):
        return f"User:{asdict(self)}"

    def to_dict(self):
        return asdict(self)
    
    def __add__(self, other):
        return User(**{**asdict(self), **asdict(other), "updated_at": datetime.now(timezone.utc).isoformat()})
