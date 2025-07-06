from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from src.application.services.todo_service import TodoService
from src.application.dtos.todo.create_todo import CreateTodoRequest
from src.application.dtos.todo.update_todo import UpdateTodoRequest
from src.application.dtos.todo.todo_response import TodoResponse
from src.presentation.dependencies import get_todo_service
from src.presentation.auth import get_current_user_id


router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse)
async def create_todo(
    request: CreateTodoRequest,
    current_user_id: str = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        # Set user_id from authenticated user
        request.user_id = current_user_id
        return await todo_service.create_todo(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[TodoResponse])
async def get_my_todos(
    current_user_id: str = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service)
):
    """Get current user's todos (requires authentication)"""
    try:
        return await todo_service.get_user_todos(current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/debug", response_model=dict)
async def debug_todos(
    current_user_id: str = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service)
):
    """Debug endpoint to check user and todos"""
    try:
        # Get user details
        user = await todo_service.user_repo.get_by_id(current_user_id)
        
        # Get raw todos from repo
        todos = await todo_service.todo_repo.get_by_user_id(current_user_id)
        
        return {
            "current_user_id": current_user_id,
            "user_exists": user is not None,
            "user_email": user.email if user else None,
            "todos_count": len(todos),
            "todos": [{"id": t.id, "title": t.title, "user_id": t.user_id} for t in todos]
        }
    except Exception as e:
        return {
            "error": str(e),
            "current_user_id": current_user_id
        }


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: str,
    current_user_id: str = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        return await todo_service.get_todo(todo_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: str,
    request: UpdateTodoRequest,
    current_user_id: str = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        request.todo_id = todo_id
        return await todo_service.update_todo(request, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{todo_id}/complete", response_model=TodoResponse)
async def complete_todo(
    todo_id: str,
    current_user_id: str = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        return await todo_service.complete_todo(todo_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    current_user_id: str = Depends(get_current_user_id),
    todo_service: TodoService = Depends(get_todo_service)
):
    try:
        deleted = await todo_service.delete_todo(todo_id, current_user_id)
        if deleted:
            return {"message": "Todo deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete todo")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))