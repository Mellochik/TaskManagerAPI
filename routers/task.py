from typing import Annotated
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from server.setup import get_db
import server.schemas.task as schemas
import server.models.task as models


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

templates = Jinja2Templates(directory="static/templates")


# Роуты для задач
@router.get("/read", response_model=list[schemas.TaskShow])
def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


@router.get("/read/{status}", response_model=list[schemas.TaskShow])
def read_tasks_by_status(status: str, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).join(models.Task.status).filter(
        models.Status.name == status).all()
    return tasks


@router.get("/show/{task_id}", response_class=HTMLResponse)
def read_task_form(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    validated_task = schemas.Task.model_validate(task)
    dumped_task = validated_task.model_dump()
    return templates.TemplateResponse(request=request, name="task_form.jinja", context=dumped_task)


@router.post("/create", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    labels_id = task.labels_id
    task = models.Task(
        title=task.title,
        description=task.description,
        create_date=task.create_date,
        date_end=task.date_end,
        status_id=task.status_id,
        priority_id=task.priority_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    for label_id in labels_id:
        db.add(models.TaskLabel(label_id=label_id, task_id=task.id))
    db.commit()
    db.refresh(task)
    return task


@router.put("/update", response_model=schemas.Task)
def update_task(task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    labels_id = task.labels_id
    db.query(models.Task).filter(models.Task.id == task.id).update(
        {
            models.Task.title: task.title,
            models.Task.description: task.description,
            models.Task.create_date: task.create_date,
            models.Task.date_end: task.date_end,
            models.Task.status_id: task.status_id,
            models.Task.priority_id: task.priority_id
        }
    )
    labels = db.query(models.TaskLabel).filter(
        models.TaskLabel.task_id == task.id).all()
    for label in labels:
        db.query(models.TaskLabel).filter(
            models.TaskLabel.id == label.id).delete()
    for label_id in labels_id:
        db.add(models.TaskLabel(label_id=label_id, task_id=task.id))
    db.commit()
    task = db.query(models.Task).filter(models.Task.id == task.id).first()
    return task


# Роуты для меток
@router.get("/labels", response_model=list[schemas.Label])
def read_labels(db: Session = Depends(get_db)):
    labels = db.query(models.Label).all()
    return labels


@router.post("/label", response_model=schemas.Label)
def create_label(label: schemas.LabelCreate, db: Session = Depends(get_db)):
    label = models.Label(name=label.name)
    db.add(label)
    db.commit()
    db.refresh(label)
    return label


# Роуты для статусов
@router.get("/statuses", response_model=list[schemas.Status])
def read_statuses(db: Session = Depends(get_db)):
    statuses = db.query(models.Status).all()
    return statuses


@router.post("/status", response_model=schemas.Status)
def create_status(status: schemas.StatusCreate, db: Session = Depends(get_db)):
    status = models.Status(name=status.name)
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


# Роуты для приоритетов
@router.get("/priorities", response_model=list[schemas.Priority])
def read_priorities(db: Session = Depends(get_db)):
    priorities = db.query(models.Priority).all()
    return priorities


@router.post("/priority", response_model=schemas.Priority)
def create_priority(priority: schemas.PriorityCreate, db: Session = Depends(get_db)):
    priority = models.Priority(name=priority.name)
    db.add(priority)
    db.commit()
    db.refresh(priority)
    return priority
