from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship


Base = declarative_base()


class TaskLabel(Base):
    __tablename__ = 'task_label'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label_id = Column(Integer, ForeignKey('labels.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    create_date = Column(DateTime)
    date_end = Column(DateTime, nullable=True)
    status_id = Column(Integer, ForeignKey("statuses.id"))
    priority_id = Column(Integer, ForeignKey("priorities.id"))

    status = relationship("Status", back_populates="tasks")
    priority = relationship("Priority", back_populates="tasks")

    labels = relationship(
        "Label", secondary=TaskLabel.__tablename__, back_populates="tasks")


class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    tasks = relationship("Task", back_populates="status")


class Priority(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    tasks = relationship("Task", back_populates="priority")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    tasks = relationship("Task", secondary=TaskLabel.__tablename__,
                         back_populates="labels")
