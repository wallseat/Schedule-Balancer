from typing import List, Dict
from datetime import time
from enum import Enum

from pydantic import BaseModel, Field


class Week(str, Enum):
    odd = "odd"
    even = "even"


class SlotScheme(BaseModel):
    id_: int = Field(..., alias="id")
    start_time: str
    end_time: str


class CourseScheme(BaseModel):
    id_: int = Field(..., alias="id")
    name: str


class Day(str, Enum):
    mon = "mon"
    tue = "tue"
    wed = "wed"
    thu = "thu"
    fri = "fri"
    sat = "sat"

    def __repr__(self) -> str:
        return self.value


class ClassType(str, Enum):
    lecture = "lecture"
    practice = "practice"

    def __repr__(self) -> str:
        return self.value


class ClassScheme(BaseModel):
    course_id: int
    slot_id: int
    type_: ClassType = Field(..., alias="type")
    room: str
    tutor: str


class DayScheme(BaseModel):
    location: str
    schedule: List[ClassScheme] = Field(default_factory=list)


class InputScheme(BaseModel):
    slots: List[SlotScheme]
    courses: List[CourseScheme]
    week: Dict[Week, Dict[Day, DayScheme]]
    students: List[str]
    start_week: int
    end_week: int
    min_on_practice: int
    min_on_lecture: int
