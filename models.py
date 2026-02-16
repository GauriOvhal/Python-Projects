from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime



# TASK TABLE
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    difficulty = Column(Enum('easy', 'medium', 'hard'), default='medium')
    status = Column(Enum('pending', 'in_progress', 'completed'), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to subtasks
    subtasks = relationship("SubTask", cascade="all, delete", back_populates="task")


# SUBTASK TABLE

class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    title = Column(String(255), nullable=False)
    status = Column(Enum('pending', 'completed'), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)  # matches your DB now

    # Relationship back to task
    task = relationship("Task", back_populates="subtasks")
