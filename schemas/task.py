from datetime import datetime
from pydantic import BaseModel


# Task
class TaskBase(BaseModel):
    title: str
    create_date: datetime
    date_end: datetime | None


class TaskCreate(TaskBase):
    description: str
    priority_id: int
    status_id: int
    labels_id: list[int]


class TaskDelete(BaseModel):
    id: int


class TaskUpdate(TaskBase):
    id: int
    description: str
    priority_id: int
    status_id: int
    labels_id: list[int]


class TaskShow(TaskBase):
    id: int
    priority: "Priority"
    status: "Status"
    labels: list["Label"] = []

    class Config:
        from_attributes = True


class Task(TaskBase):
    id: int
    description: str
    priority: "Priority"
    status: "Status"
    labels: list["Label"] = []

    class Config:
        from_attributes = True


# Priority
class PriorityBase(BaseModel):
    name: str


class PriorityCreate(PriorityBase):
    pass


class Priority(PriorityBase):
    id: int

    class Config:
        from_attributes = True


# Status
class StatusBase(BaseModel):
    name: str


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    id: int

    class Config:
        from_attributes = True


# Labels
class LabelBase(BaseModel):
    name: str


class LabelCreate(LabelBase):
    pass


class Label(LabelBase):
    id: int

    class Config:
        from_attributes = True
