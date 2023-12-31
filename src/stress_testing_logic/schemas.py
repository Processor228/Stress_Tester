from pydantic import BaseModel


class TestingOutput(BaseModel):
    elapsed_time: float  # time to run the testing procedure
    output: str


