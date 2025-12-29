from typing import List, Optional, Literal
from pydantic import BaseModel

class ParseRequest(BaseModel):
    text: str

class RSTNode(BaseModel):
    id: int
    relation: str
    nuclearity: str
    text: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    children: List['RSTNode'] = []

class ParseResponse(BaseModel):
    tree: RSTNode
