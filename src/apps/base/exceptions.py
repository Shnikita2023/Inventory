class ApplicationException(Exception):
    entity: str = "Application"
    text: int | str = ""
    status_code: int = 500

    @property
    def message(self) -> str:
        return "Что-то пошло не так, попробуйте позже"
