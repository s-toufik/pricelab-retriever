from pydantic import BaseModel
from typing import Optional, List, Dict

class AuthSchema(BaseModel):
    type: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    key_name: Optional[str] = None
    key_value: Optional[str] = None

class EndpointSchema(BaseModel):
    name: str
    path: str
    method: str
    params: Optional[Dict] = None

class ApiConfigurationSchema(BaseModel):
    source: str
    base_url: str
    timeout: int
    retry: int
    auth: AuthSchema
    endpoints: List[EndpointSchema]

class AppBaseConfigurationSchema(BaseModel):
    run: str
    primary_database_type: str
    secondary_database_type: str

class AppConfigurationSchema(AppBaseConfigurationSchema):
    api_configurations: List[ApiConfigurationSchema]