from http import HTTPStatus

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: to_camel(field_name),
        populate_by_name=True,
        from_attributes=True,
    )


class BaseResponseSchema(BaseSchema):
    status_code: HTTPStatus = HTTPStatus.OK
    code: str | None = None
