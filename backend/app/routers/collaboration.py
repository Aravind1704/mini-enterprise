import os

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.schemas.approval import ApprovalAction, ApprovalCreate, ApprovalOut
from app.schemas.collaboration import (
    ApprovalDocumentOut,
    ChannelMessageOut,
    MessageCreate,
    MessageUpdate,
    ScopedTaskCreate,
    ScopedTaskOut,
    TaskAssign,
    TaskDocumentOut,
    WorkspaceMessageOut,
)
from app.services import collaboration_service as service


router = APIRouter(tags=["Workspace & Channel Collaboration"])


# ===================== WORKSPACE MESSAGES =====================

@router.post(
    "/workspaces/{workspace_id}/messages",
    response_model=WorkspaceMessageOut,
)
def send_workspace_message(
    workspace_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.create_workspace_message(db, workspace_id, payload, user)


@router.get(
    "/workspaces/{workspace_id}/messages",
    response_model=list[WorkspaceMessageOut],
)
def list_workspace_messages(
    workspace_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.list_workspace_messages(db, workspace_id, user)


@router.put(
    "/workspace-messages/{message_id}",
    response_model=WorkspaceMessageOut,
)
def edit_workspace_message(
    message_id: int,
    payload: MessageUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.update_workspace_message(db, message_id, payload, user)


@router.delete("/workspace-messages/{message_id}")
def delete_workspace_message(
    message_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.delete_workspace_message(db, message_id, user)


# ===================== CHANNEL MESSAGES =====================

@router.post(
    "/channels/{channel_id}/messages",
    response_model=ChannelMessageOut,
)
def send_channel_message(
    channel_id: int,
    payload: MessageCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.create_channel_message(db, channel_id, payload, user)


@router.get(
    "/channels/{channel_id}/messages",
    response_model=list[ChannelMessageOut],
)
def list_channel_messages(
    channel_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.list_channel_messages(db, channel_id, user)


@router.put(
    "/channel-messages/{message_id}",
    response_model=ChannelMessageOut,
)
def edit_channel_message(
    message_id: int,
    payload: MessageUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.update_channel_message(db, message_id, payload, user)


@router.delete("/channel-messages/{message_id}")
def delete_channel_message(
    message_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.delete_channel_message(db, message_id, user)


# ===================== WORKSPACE TASKS =====================

@router.post(
    "/workspaces/{workspace_id}/tasks",
    response_model=ScopedTaskOut,
)
def create_workspace_task(
    workspace_id: int,
    payload: ScopedTaskCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.create_workspace_task(db, workspace_id, payload, user)


@router.get(
    "/workspaces/{workspace_id}/tasks",
    response_model=list[ScopedTaskOut],
)
def list_workspace_tasks(
    workspace_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.list_workspace_tasks(db, workspace_id, user)


@router.get(
    "/workspaces/{workspace_id}/tasks/{task_id}",
    response_model=ScopedTaskOut,
)
def get_workspace_task(
    workspace_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.get_workspace_task(db, workspace_id, task_id, user)


@router.patch(
    "/workspaces/{workspace_id}/tasks/{task_id}/assign",
    response_model=ScopedTaskOut,
)
def assign_workspace_task(
    workspace_id: int,
    task_id: int,
    payload: TaskAssign,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.assign_workspace_task(db, workspace_id, task_id, payload, user)


# ===================== CHANNEL TASKS =====================

@router.post(
    "/channels/{channel_id}/tasks",
    response_model=ScopedTaskOut,
)
def create_channel_task(
    channel_id: int,
    payload: ScopedTaskCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.create_channel_task(db, channel_id, payload, user)


@router.get(
    "/channels/{channel_id}/tasks",
    response_model=list[ScopedTaskOut],
)
def list_channel_tasks(
    channel_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.list_channel_tasks(db, channel_id, user)


@router.get(
    "/channels/{channel_id}/tasks/{task_id}",
    response_model=ScopedTaskOut,
)
def get_channel_task(
    channel_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.get_channel_task(db, channel_id, task_id, user)


@router.patch(
    "/channels/{channel_id}/tasks/{task_id}/assign",
    response_model=ScopedTaskOut,
)
def assign_channel_task(
    channel_id: int,
    task_id: int,
    payload: TaskAssign,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.assign_channel_task(db, channel_id, task_id, payload, user)


# ===================== TASK DOCUMENTS =====================

@router.post(
    "/tasks/{task_id}/documents",
    response_model=TaskDocumentOut,
)
def upload_task_document(
    task_id: int,
    document_type: str = Form("OTHER"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.upload_task_document(db, task_id, file, document_type, user)


@router.get(
    "/tasks/{task_id}/documents",
    response_model=list[TaskDocumentOut],
)
def list_task_documents(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.list_task_documents(db, task_id, user)


@router.get("/task-documents/{document_id}/download")
def download_task_document(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    document = service.get_task_document_download(db, document_id, user)
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(
        path=document.file_path,
        filename=document.file_name,
        media_type=document.mime_type or "application/octet-stream",
    )


@router.delete("/task-documents/{document_id}")
def delete_task_document(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.delete_task_document(db, document_id, user)


# ===================== APPROVALS =====================

@router.post(
    "/approvals/",
    response_model=ApprovalOut,
)
def create_approval(
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.create_approval(db, payload, user)


@router.patch(
    "/approvals/{approval_id}/action",
    response_model=ApprovalOut,
)
def action_approval(
    approval_id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.action_approval(db, approval_id, payload, user)


@router.post(
    "/approvals/{approval_id}/documents",
    response_model=ApprovalDocumentOut,
)
def upload_approval_document(
    approval_id: int,
    document_type: str = Form("SUPPORTING"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.upload_approval_document(db, approval_id, file, document_type, user)


@router.get(
    "/approvals/{approval_id}/documents",
    response_model=list[ApprovalDocumentOut],
)
def list_approval_documents(
    approval_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.list_approval_documents(db, approval_id, user)


@router.get("/approval-documents/{document_id}/download")
def download_approval_document(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    document = service.get_approval_document_download(db, document_id, user)
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(
        path=document.file_path,
        filename=document.file_name,
        media_type=document.mime_type or "application/octet-stream",
    )


@router.delete("/approval-documents/{document_id}")
def delete_approval_document(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return service.delete_approval_document(db, document_id, user)