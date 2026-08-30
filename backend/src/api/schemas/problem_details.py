from pydantic import BaseModel


# Mirar RFC -> https://datatracker.ietf.org/doc/html/rfc7807
class ProblemDetails(BaseModel):
    type: str
    title: str
    status: int
    detail: str | dict
    instance: str
