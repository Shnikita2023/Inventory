from dataclasses import dataclass

from apps.base.exceptions import ApplicationException


@dataclass(eq=False, frozen=True)
class UserAlreadyExists(ApplicationException):
    text: str
    status_code: int = 400

    @property
    def message(self) -> str:
        return f"User {self.text} already exists"
