from typing import List, Optional, Union
from pydantic import BaseModel, model_validator


class UserCreate(BaseModel):
    login: str
    password: str


class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    photo_url: Optional[str] = None
    photo: Optional[Union[List[str], str]] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_photo(cls, values):
        if isinstance(values, dict):
            p = values.get("photo") or values.get("photo_url")
            if isinstance(p, list):
                val = p[0] if p else None
            else:
                val = p
            values["photo_url"] = val
            values["photo"] = val
        return values


class TeacherUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    photo_url: Optional[str] = None
    photo: Optional[Union[List[str], str]] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_photo(cls, values):
        if isinstance(values, dict):
            p = values.get("photo") or values.get("photo_url")
            if isinstance(p, list):
                val = p[0] if p else None
            else:
                val = p
            values["photo_url"] = val
            values["photo"] = val
        return values


class NewsCreate(BaseModel):
    description: str
    photo: Optional[Union[List[str], str]] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_photo(cls, values):
        if isinstance(values, dict):
            p = values.get("photo")
            if isinstance(p, list):
                values["photo"] = p[0] if p else None
        return values


class NewsUpdate(BaseModel):
    description: Optional[str] = None
    photo: Optional[Union[List[str], str]] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_photo(cls, values):
        if isinstance(values, dict):
            p = values.get("photo")
            if isinstance(p, list):
                values["photo"] = p[0] if p else None
        return values


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None


class DeficiencyCreate(BaseModel):
    description: Optional[str] = None
    photo: Optional[Union[List[str], str]] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, values):
        if isinstance(values, dict):
            p = values.get("photo")
            if isinstance(p, list):
                values["photo"] = p[0] if p else None
            if not values.get("description") and values.get("title"):
                values["description"] = values.get("title")
        return values


class DeficiencyUpdate(BaseModel):
    description: Optional[str] = None
    photo: Optional[Union[List[str], str]] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_fields(cls, values):
        if isinstance(values, dict):
            p = values.get("photo")
            if isinstance(p, list):
                values["photo"] = p[0] if p else None
            if not values.get("description") and values.get("title"):
                values["description"] = values.get("title")
        return values
