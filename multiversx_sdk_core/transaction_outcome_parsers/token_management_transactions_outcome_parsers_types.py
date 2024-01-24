from dataclasses import dataclass
from typing import List


@dataclass
class RegisterAndSetAllRolesOutcome:
    token_identifier: str
    roles: List[str]
