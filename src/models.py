from typing import List, Optional
from pydantic import BaseModel, Field

class AdditionRequest(BaseModel):
    additional_info: Optional[str] = "Дополнительные сведения"
    additional_number: Optional[int] = 123

class AdditionResponse(BaseModel):
    id: int
    additional_info: str
    additional_number: int

class EntityRequest(BaseModel):
    title: str = "Заголовок сущности по умолчанию"
    verified: bool = True
    important_numbers: List[int] = Field(
        default_factory=list, description="Список важных числовых идентификаторов"
    )
    addition: AdditionRequest = Field(default_factory=AdditionRequest)

class EntityResponse(BaseModel):
    id: int
    title: str
    verified: bool
    important_numbers: List[int] = Field(default_factory=list)
    addition: AdditionResponse

class EntityListResponse(BaseModel):
    entity: List[EntityResponse]