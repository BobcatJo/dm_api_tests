from pydantic import BaseModel, Field, ConfigDict

class PasswordChangePost(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='Логин')
    password: str = Field(..., description='Старый пароль')
    email: str = Field(..., description='Email')