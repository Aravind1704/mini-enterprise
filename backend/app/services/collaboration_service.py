from datetime import datetime
import os
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.approval import Approval, ApprovalHistory
from app.models.channel import Channel
from app.models.channel_member import ChannelMember
from app.models.collaboration import (
    ApprovalDocument,
    ChannelMessage,
    TaskDocument,
    WorkspaceMessage,
)
from app.models.task import Task
from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember


UPLOAD_ROOT = Path("uploads")
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "image/jpeg",
    "image/png",
    "text/plain",
}
TASK_DOCUMENT_TYPES = {
    "REQUIREMENT",
    "SPECIFICATION",
    "REFERENCE",
    "DELIVERABLE",
    "OTHER",
}


def _forbidden(detail: str = "Permission denied"):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def _not_found(detail: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def _role(value: str | None) -> str:
    return (value or "").lower()


def _member_role(value: str | None) -> str:
    return (value or "").upper()


def _ensure_tenant(user: User, tenant_id: int):
    if user.role == "super_admin":
        return
    if user.tenant_id != tenant_id:
        _forbidden("Cross-tenant access is not allowed")


def _workspace(db: Session, workspace_id: int) -> Workspace:
    workspace = db.get(Workspace, workspace_id)
    if not workspace:
        _not_found("Workspace not found")
    return workspace


def _channel(db: Session, channel_id: int) -> Channel:
    channel = db.get(Channel, channel_id)
    if not channel:
        _not_found("Channel not found")
    return channel


def _workspace_member(
    db: Session,
    workspace_id: int,
    user_id: int
) -> WorkspaceMember | None:
    return db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
            WorkspaceMember.is_active == True,
        )
    ).scalar_one_or_none()


def _channel_member(
    db: Session,
    channel_id: int,
    user_id: int
) -> ChannelMember | None:
    return db.execute(
        select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id,
        )
    ).scalar_one_or_none()


def _can_view_workspace(
    db: Session,
    workspace: Workspace,
    user: User
) -> WorkspaceMember | None:
    _ensure_tenant(user, workspace.tenant_id)
    member = _workspace_member(db, workspace.id, user.id)
    if member or workspace.created_by == user.id or _role(user.role) == "admin":
        return member
    _forbidden("Workspace membership required")


def _can_view_channel(
    db: Session,
    channel: Channel,
    user: User
) -> tuple[Workspace, ChannelMember | None, WorkspaceMember | None]:
    workspace = _workspace(db, channel.workspace_id)
    _ensure_tenant(user, channel.tenant_id)
    workspace_member = _can_view_workspace(db, workspace, user)
    channel_member = _channel_member(db, channel.id, user.id)
    if (
        channel_member
        or channel.created_by == user.id
        or workspace.created_by == user.id
        or _role(user.role) == "admin"
    ):
        return workspace, channel_member, workspace_member
    _forbidden("Channel membership required")


def _can_manage_workspace_tasks(member: WorkspaceMember | None, user: User) -> bool:
    if _role(user.role) in {"admin", "manager"}:
        return True
    return _member_role(getattr(member, "role", None)) in {"ADMIN", "MODERATOR", "MANAGER"}


def _can_manage_channel_tasks(member: WorkspaceMember | None, user: User) -> bool:
    return _can_manage_workspace_tasks(member, user)


def _can_admin_workspace(workspace: Workspace, member: WorkspaceMember | None, user: User) -> bool:
    if workspace.created_by == user.id or _role(user.role) == "admin":
        return True
    return _member_role(getattr(member, "role", None)) in {"ADMIN", "MODERATOR"}


def _task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if not task:
        _not_found("Task not found")
    return task


def _approval(db: Session, approval_id: int) -> Approval:
    approval = db.get(Approval, approval_id)
    if not approval:
        _not_found("Approval not found")
    return approval


def _ensure_workspace_assignee(db: Session, workspace_id: int, user_id: int | None):
    if user_id is None:
        return
    if not _workspace_member(db, workspace_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignee must be an active workspace member",
        )


def _ensure_channel_assignee(db: Session, channel_id: int, user_id: int | None):
    if user_id is None:
        return
    if not _channel_member(db, channel_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignee must be a channel member",
        )


def _can_view_task(db: Session, task: Task, user: User):
    if task.tenant_id is not None:
        _ensure_tenant(user, task.tenant_id)

    if task.channel_id:
        _can_view_channel(db, _channel(db, task.channel_id), user)
        return

    if task.workspace_id:
        _can_view_workspace(db, _workspace(db, task.workspace_id), user)
        return

    if _role(user.role) == "admin" or task.created_by_id == user.id or task.assigned_to_id == user.id:
        return

    _forbidden("Task access required")


# ===================== WORKSPACE MESSAGES =====================

def create_workspace_message(db: Session, workspace_id: int, payload, user: User):
    workspace = _workspace(db, workspace_id)
    _can_view_workspace(db, workspace, user)
    message = WorkspaceMessage(
        tenant_id=workspace.tenant_id,
        workspace_id=workspace.id,
        sender_id=user.id,
        content=payload.content,
        message_type=payload.message_type,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_workspace_messages(db: Session, workspace_id: int, user: User):
    workspace = _workspace(db, workspace_id)
    _can_view_workspace(db, workspace, user)
    return db.execute(
        select(WorkspaceMessage)
        .where(
            WorkspaceMessage.workspace_id == workspace_id,
            WorkspaceMessage.tenant_id == workspace.tenant_id,
        )
        .order_by(WorkspaceMessage.created_at.asc())
    ).scalars().all()


def update_workspace_message(db: Session, message_id: int, payload, user: User):
    message = db.get(WorkspaceMessage, message_id)
    if not message:
        _not_found("Workspace message not found")
    workspace = _workspace(db, message.workspace_id)
    member = _can_view_workspace(db, workspace, user)
    if message.sender_id != user.id and not _can_admin_workspace(workspace, member, user):
        _forbidden("Only sender or workspace admin can edit this message")
    if message.deleted_at:
        raise HTTPException(status_code=400, detail="Deleted messages cannot be edited")
    message.content = payload.content
    message.edited_at = datetime.utcnow()
    db.commit()
    db.refresh(message)
    return message


def delete_workspace_message(db: Session, message_id: int, user: User):
    message = db.get(WorkspaceMessage, message_id)
    if not message:
        _not_found("Workspace message not found")
    workspace = _workspace(db, message.workspace_id)
    member = _can_view_workspace(db, workspace, user)
    if message.sender_id != user.id and not _can_admin_workspace(workspace, member, user):
        _forbidden("Only sender or workspace admin can delete this message")
    message.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Message deleted successfully"}


# ===================== CHANNEL MESSAGES =====================

def create_channel_message(db: Session, channel_id: int, payload, user: User):
    channel = _channel(db, channel_id)
    workspace, _, _ = _can_view_channel(db, channel, user)
    message = ChannelMessage(
        tenant_id=channel.tenant_id,
        workspace_id=workspace.id,
        channel_id=channel.id,
        sender_id=user.id,
        content=payload.content,
        message_type=payload.message_type,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def list_channel_messages(db: Session, channel_id: int, user: User):
    channel = _channel(db, channel_id)
    _can_view_channel(db, channel, user)
    return db.execute(
        select(ChannelMessage)
        .where(
            ChannelMessage.channel_id == channel_id,
            ChannelMessage.tenant_id == channel.tenant_id,
        )
        .order_by(ChannelMessage.created_at.asc())
    ).scalars().all()


def update_channel_message(db: Session, message_id: int, payload, user: User):
    message = db.get(ChannelMessage, message_id)
    if not message:
        _not_found("Channel message not found")
    channel = _channel(db, message.channel_id)
    workspace, _, workspace_member = _can_view_channel(db, channel, user)
    if (
        message.sender_id != user.id
        and channel.created_by != user.id
        and not _can_admin_workspace(workspace, workspace_member, user)
    ):
        _forbidden("Only sender, channel moderator, or workspace admin can edit this message")
    if message.deleted_at:
        raise HTTPException(status_code=400, detail="Deleted messages cannot be edited")
    message.content = payload.content
    message.edited_at = datetime.utcnow()
    db.commit()
    db.refresh(message)
    return message


def delete_channel_message(db: Session, message_id: int, user: User):
    message = db.get(ChannelMessage, message_id)
    if not message:
        _not_found("Channel message not found")
    channel = _channel(db, message.channel_id)
    workspace, _, workspace_member = _can_view_channel(db, channel, user)
    if (
        message.sender_id != user.id
        and channel.created_by != user.id
        and not _can_admin_workspace(workspace, workspace_member, user)
    ):
        _forbidden("Only sender, channel moderator, or workspace admin can delete this message")
    message.deleted_at = datetime.utcnow()
    db.commit()
    return {"message": "Message deleted successfully"}


# ===================== WORKSPACE TASKS =====================

def create_workspace_task(db: Session, workspace_id: int, payload, user: User):
    workspace = _workspace(db, workspace_id)
    member = _can_view_workspace(db, workspace, user)
    if not _can_manage_workspace_tasks(member, user):
        _forbidden("Workspace admin, moderator, or manager access required")
    _ensure_workspace_assignee(db, workspace_id, payload.assigned_to_id)
    task = Task(
        tenant_id=workspace.tenant_id,
        workspace_id=workspace.id,
        channel_id=None,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
        assigned_to_id=payload.assigned_to_id,
        created_by_id=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_workspace_tasks(db: Session, workspace_id: int, user: User):
    workspace = _workspace(db, workspace_id)
    _can_view_workspace(db, workspace, user)
    return db.execute(
        select(Task)
        .where(
            Task.workspace_id == workspace_id,
            Task.channel_id == None,
            Task.tenant_id == workspace.tenant_id,
        )
        .order_by(Task.created_at.desc())
    ).scalars().all()


def get_workspace_task(db: Session, workspace_id: int, task_id: int, user: User):
    task = _task(db, task_id)
    if task.workspace_id != workspace_id or task.channel_id is not None:
        _not_found("Workspace task not found")
    _can_view_task(db, task, user)
    return task


def assign_workspace_task(db: Session, workspace_id: int, task_id: int, payload, user: User):
    workspace = _workspace(db, workspace_id)
    member = _can_view_workspace(db, workspace, user)
    if not _can_manage_workspace_tasks(member, user):
        _forbidden("Workspace admin, moderator, or manager access required")
    task = get_workspace_task(db, workspace_id, task_id, user)
    _ensure_workspace_assignee(db, workspace_id, payload.assigned_to_id)
    task.assigned_to_id = payload.assigned_to_id
    task.updated_by = user.id
    db.commit()
    db.refresh(task)
    return task


# ===================== CHANNEL TASKS =====================

def create_channel_task(db: Session, channel_id: int, payload, user: User):
    channel = _channel(db, channel_id)
    workspace, _, workspace_member = _can_view_channel(db, channel, user)
    if not _can_manage_channel_tasks(workspace_member, user):
        _forbidden("Channel moderator, workspace admin, or manager access required")
    _ensure_channel_assignee(db, channel_id, payload.assigned_to_id)
    task = Task(
        tenant_id=channel.tenant_id,
        workspace_id=workspace.id,
        channel_id=channel.id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
        assigned_to_id=payload.assigned_to_id,
        created_by_id=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_channel_tasks(db: Session, channel_id: int, user: User):
    channel = _channel(db, channel_id)
    _can_view_channel(db, channel, user)
    return db.execute(
        select(Task)
        .where(
            Task.channel_id == channel_id,
            Task.tenant_id == channel.tenant_id,
        )
        .order_by(Task.created_at.desc())
    ).scalars().all()


def get_channel_task(db: Session, channel_id: int, task_id: int, user: User):
    task = _task(db, task_id)
    if task.channel_id != channel_id:
        _not_found("Channel task not found")
    _can_view_task(db, task, user)
    return task


def assign_channel_task(db: Session, channel_id: int, task_id: int, payload, user: User):
    channel = _channel(db, channel_id)
    _, _, workspace_member = _can_view_channel(db, channel, user)
    if not _can_manage_channel_tasks(workspace_member, user):
        _forbidden("Channel moderator, workspace admin, or manager access required")
    task = get_channel_task(db, channel_id, task_id, user)
    _ensure_channel_assignee(db, channel_id, payload.assigned_to_id)
    task.assigned_to_id = payload.assigned_to_id
    task.updated_by = user.id
    db.commit()
    db.refresh(task)
    return task


# ===================== TASK DOCUMENTS =====================

def _validate_document_type(document_type: str, allowed: set[str]) -> str:
    normalized = (document_type or "OTHER").upper()
    if normalized not in allowed:
        raise HTTPException(status_code=400, detail="Invalid document type")
    return normalized


def _save_upload(file: UploadFile, folder: str) -> tuple[str, int]:
    if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    safe_name = os.path.basename(file.filename or "upload.bin")
    upload_dir = UPLOAD_ROOT / folder
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / f"{uuid4().hex}_{safe_name}"

    size = 0
    with file_path.open("wb") as buffer:
        while True:
            chunk = file.file.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_UPLOAD_SIZE:
                buffer.close()
                file_path.unlink(missing_ok=True)
                raise HTTPException(status_code=400, detail="File exceeds 10 MB limit")
            buffer.write(chunk)

    return str(file_path), size


def upload_task_document(db: Session, task_id: int, file: UploadFile, document_type: str, user: User):
    task = _task(db, task_id)
    _can_view_task(db, task, user)
    if user.id not in {task.created_by_id, task.assigned_to_id} and _role(user.role) not in {"admin", "manager"}:
        _forbidden("Only creator, assignee, manager, or admin can upload task documents")
    normalized_type = _validate_document_type(document_type, TASK_DOCUMENT_TYPES)
    file_path, file_size = _save_upload(file, "task_documents")
    document = TaskDocument(
        tenant_id=task.tenant_id or user.tenant_id,
        task_id=task.id,
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        uploaded_by=user.id,
        document_type=normalized_type,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def list_task_documents(db: Session, task_id: int, user: User):
    task = _task(db, task_id)
    _can_view_task(db, task, user)
    return db.execute(
        select(TaskDocument)
        .where(TaskDocument.task_id == task_id)
        .order_by(TaskDocument.created_at.desc())
    ).scalars().all()


def get_task_document_download(db: Session, document_id: int, user: User):
    document = db.get(TaskDocument, document_id)
    if not document:
        _not_found("Task document not found")
    task = _task(db, document.task_id)
    _can_view_task(db, task, user)
    return document


def delete_task_document(db: Session, document_id: int, user: User):
    document = db.get(TaskDocument, document_id)
    if not document:
        _not_found("Task document not found")
    task = _task(db, document.task_id)
    _can_view_task(db, task, user)
    if document.uploaded_by != user.id and _role(user.role) not in {"admin", "manager"}:
        _forbidden("Only uploader, manager, or admin can delete this document")
    Path(document.file_path).unlink(missing_ok=True)
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}


# ===================== APPROVALS =====================

def create_approval(db: Session, payload, user: User):
    approval = Approval(
        tenant_id=user.tenant_id,
        workspace_id=getattr(payload, "workspace_id", None),
        channel_id=getattr(payload, "channel_id", None),
        title=payload.title,
        description=payload.description,
        requested_by=user.id,
    )
    db.add(approval)
    db.commit()
    db.refresh(approval)
    return approval


def action_approval(db: Session, approval_id: int, payload, user: User):
    approval = _approval(db, approval_id)
    if approval.tenant_id is not None:
        _ensure_tenant(user, approval.tenant_id)
    if _role(user.role) not in {"admin", "manager"}:
        _forbidden("Approver or admin access required")
    if payload.action not in {"approved", "rejected", "hold"}:
        raise HTTPException(status_code=400, detail="Invalid approval action")
    approval.status = payload.action
    history = ApprovalHistory(
        approval_id=approval.id,
        action_by=user.id,
        action=payload.action,
        comment=payload.comment,
    )
    db.add(history)
    db.commit()
    db.refresh(approval)
    return approval


def _can_view_approval(approval: Approval, user: User):
    if approval.tenant_id is not None:
        _ensure_tenant(user, approval.tenant_id)
    if approval.requested_by == user.id or _role(user.role) in {"admin", "manager"}:
        return
    _forbidden("Approval access required")


def upload_approval_document(db: Session, approval_id: int, file: UploadFile, document_type: str, user: User):
    approval = _approval(db, approval_id)
    _can_view_approval(approval, user)
    normalized_type = (document_type or "SUPPORTING").upper()
    file_path, file_size = _save_upload(file, "approval_documents")
    document = ApprovalDocument(
        tenant_id=approval.tenant_id or user.tenant_id,
        approval_id=approval.id,
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        uploaded_by=user.id,
        document_type=normalized_type,
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def list_approval_documents(db: Session, approval_id: int, user: User):
    approval = _approval(db, approval_id)
    _can_view_approval(approval, user)
    return db.execute(
        select(ApprovalDocument)
        .where(ApprovalDocument.approval_id == approval_id)
        .order_by(ApprovalDocument.created_at.desc())
    ).scalars().all()


def get_approval_document_download(db: Session, document_id: int, user: User):
    document = db.get(ApprovalDocument, document_id)
    if not document:
        _not_found("Approval document not found")
    approval = _approval(db, document.approval_id)
    _can_view_approval(approval, user)
    return document


def delete_approval_document(db: Session, document_id: int, user: User):
    document = db.get(ApprovalDocument, document_id)
    if not document:
        _not_found("Approval document not found")
    approval = _approval(db, document.approval_id)
    _can_view_approval(approval, user)
    if document.uploaded_by != user.id and _role(user.role) != "admin":
        _forbidden("Only uploader or admin can delete this document")
    Path(document.file_path).unlink(missing_ok=True)
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}