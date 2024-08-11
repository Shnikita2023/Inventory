from dataclasses import dataclass

from apps.base.exceptions import ApplicationException


@dataclass(eq=False, frozen=True)
class NotFoundError(ApplicationException):
    entity: str
    text: int
    status_code: int = 400

    @property
    def message(self) -> str:
        return f"{self.entity} {self.text} not found"
