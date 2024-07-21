from pydantic import BaseModel, Field
from typing import List, Any


class List_objects(BaseModel):
    field1: float | None= Field(default=None,)
    field2: bool | None= Field(default=None,)
    

class Specification(BaseModel):
    spec1: float | str | None= Field(default=None,)
    

class Settings(BaseModel):
    sett1: str | None= Field(default=None,)
    

class Configuration(BaseModel):
    specification: Specification = Field(...,) 
    settings: Settings | None = Field(default=None)  
    

class Custom_schema(BaseModel):
    kind: str= Field(...,max_lenght=32,)
    name: str= Field(...,max_lenght=128,)
    version: str= Field(...,pattern=r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$',)
    description: str= Field(...,max_lenght=4096,)
    list: List[float] | None= Field(default=None,)
    list_objects: List[List_objects] | None = Field(default=None)  
    configuration: Configuration = Field(...,) 
    
