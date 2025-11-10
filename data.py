import uuid
from src.models import EntityRequest, AdditionRequest

def default_entity() -> EntityRequest:
    return EntityRequest(
        title=f"Новая тестовая сущность - {uuid.uuid4().hex[:4]}",
        verified=True,
        important_numbers=[10, 20, 30],
        addition=AdditionRequest(
            additional_info="Стандартная доп. информация", additional_number=123
        ),
    )

def updated_entity_payload() -> EntityRequest:
    return EntityRequest(
        title=f"Обновленный заголовок - {uuid.uuid4().hex[:4]}",
        verified=False
    )

def verified_entity() -> EntityRequest:
    unique_part = uuid.uuid4().hex[:8]
    return EntityRequest(title=f"Verified Entity {unique_part}", verified=True)

def unverified_entity() -> EntityRequest:
    unique_part = uuid.uuid4().hex[:8]
    return EntityRequest(title=f"Unverified Entity {unique_part}", verified=False)