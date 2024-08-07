from typing import Annotated, Optional, Union

from pydantic import (
    UUID4,
    BaseModel,
    DirectoryPath,
    EmailStr,
    FilePath,
    HttpUrl,
    IPvAnyAddress,
    Json,
    StringConstraints,
)


class Item(BaseModel):
    name: str
    price: float = 10.0
    on_stack: Optional[Union[int, float]] = None


class User(BaseModel):
    name: str = ""
    email: EmailStr
    info: Optional[Json] = None
    id: Optional[UUID4] = None
    ip_address: Optional[IPvAnyAddress] = None
    file_path: Optional[FilePath | DirectoryPath] = None
    url: Optional[HttpUrl] = None
    card_number: Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True, pattern=r"^\d{16}$")]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "email": "abc@def.ghi",
                    "info": '{"foo": "bar"}',
                    "id": "0f32feaa-fafc-4faa-8072-0e591e9b4a4e",
                    "ip_address": "128.1.2.3",
                    "file_path": "/tmp",
                    "url": "http://example.com",
                    "card_number": "1234567890123456",
                }
            ]
        }
    }
