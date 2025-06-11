from pydantic import BaseModel, Field
from pydantic_core import core_schema
from typing import Optional, List, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId string")
            return ObjectId(value)
        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId), 
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(validate_from_str),
                    ]
                ),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema_obj: core_schema.CoreSchema, handler: Any 
    ) -> dict[str, Any]:
        json_schema = handler(core_schema_obj)
        json_schema = handler.resolve_ref_schema(json_schema)
        json_schema.update(type='string', example='507f191e810c19729de860ea')
        return json_schema

class SongBase(BaseModel):
    title: str
    category: str
    originalTonality: str 
    bpm: Optional[int] = None
    youtubeLink: Optional[str] = None
    docsLink: Optional[str] = None
    lyricsWithChords: Optional[str] = None 

    class Config:
        populate_by_name = True 

class SongCreate(SongBase):
    
    pass

class SongUpdate(BaseModel): 
    title: Optional[str] = None
    category: Optional[str] = None
    originalTonality: Optional[str] = None
    bpm: Optional[int] = None
    youtubeLink: Optional[str] = None
    docsLink: Optional[str] = None
    lyricsWithChords: Optional[str] = None

class SongInDB(SongBase):
    id: PyObjectId = Field(alias="_id") 

    class Config:
        populate_by_name = True 
        json_encoders = { ObjectId: str, PyObjectId: str } 
        arbitrary_types_allowed = True 