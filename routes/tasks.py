from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db import get_session
from models.tasks import Task
from models.users import User
from schemas.user import UserRead
from dependencies import get_current_user
from schemas.task import TaskCreate, TaskRead, TaskUpdate
from uuid import UUID

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/")
async def read_tasks(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(Task).where(Task.user_id == user.id)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/", response_model=TaskRead)
async def create_task(task: TaskCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    task = Task(title=task.title, description=task.description, user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskRead)
async def read_task(task_id: UUID, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_id: UUID, task_update: TaskUpdate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: UUID, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id, Task.user_id == user.id)
    task = session.exec(statement).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"detail": "Task deleted successfully"}