from typing import Annotated,Literal
from pydantic import Field, BaseModel, computed_field,field_validator

class TodoDetails(BaseModel):
    todo : Annotated[str, Field(...,description="Enter your todo details.")]
    status : Annotated[str, Field(...,description = "Enter Status Complete or Incomplete",example = "Incomplete")]
    
    @field_validator('status')
    @classmethod
    def udpate_status(cls, s:str) -> str:
        return s.strip().title()


class todo_data(BaseModel):
    todo: Annotated[str, Field(..., description= "Enter your new todo for update.")]

class status_data(BaseModel):
    status: Annotated[Literal['Complete','Incomplete'], Field(..., description= "Select from Complete or Incomplete")]

    @field_validator('status')
    @classmethod
    def udpate_status(cls, s: str) -> str:
        return s.strip().title()
