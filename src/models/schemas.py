from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Operator(str, Enum):
    EQUALS = "equals"
    CONTAINS = "contains"
    EXISTS = "exists"


class Tag(BaseModel):
    key: str
    value: str


class CloudAccount(BaseModel):
    id: str
    name: str


class Asset(BaseModel):
    name: str
    type: str
    tags: List[Tag]
    cloud_account: CloudAccount
    owner_id: str
    region: str

    # internal fields
    id: Optional[str] = None
    group_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class GroupingCondition(BaseModel):
    field: str
    operator: Operator
    value: Optional[str] = None
    tag_key: Optional[str] = None
    tag_value: Optional[str] = None


class GroupingRule(BaseModel):
    group_name: str
    conditions: List[GroupingCondition]
    description: Optional[str] = None

    # internal fields
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
