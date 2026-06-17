# app/services/channel_service.py
from app.models.channel_member import ChannelMember
from app.models.user import User

from sqlalchemy.orm import Session

from app.models.channel import Channel

from app.repositories.channel_repo import (
    ChannelRepo
)

from app.repositories.channel_member_repo import (
    ChannelMemberRepo
)

from app.models.channel_member import (
    ChannelMember
)

from app.schemas.channel import (
    ChannelCreate,
    ChannelUpdate
)

from app.services.tenant_collaboration_settings_service import (
    get_collaboration_settings,
    create_default_settings,
    check_channel_enabled,
    validate_channel_limit
)


# =========================================
# CREATE CHANNEL
# =========================================

def create_channel(
    db: Session,
    payload: ChannelCreate,
    created_by: int
):

    existing = (
        ChannelRepo.get_by_name(
            db,
            payload.workspace_id,
            payload.name
        )
    )

    if existing:

        raise ValueError(
            "Channel already exists"
        )

    # enforce tenant settings and limits
    settings = get_collaboration_settings(
        db,
        payload.tenant_id
    )

    if not settings:
        settings = create_default_settings(
            db,
            payload.tenant_id
        )

    check_channel_enabled(settings)

    current_channel_count = len(
        ChannelRepo.list_active_by_workspace(
            db,
            payload.workspace_id
        )
    )

    validate_channel_limit(
        settings,
        current_channel_count
    )

    channel = Channel(
        tenant_id=payload.tenant_id,
        workspace_id=payload.workspace_id,
        name=payload.name,
        description=payload.description,
        channel_type=payload.channel_type,
        created_by=created_by,
        is_archived=False
    )

    return (
        ChannelRepo.create(
            db,
            channel
        )
    )


# =========================================
# GET CHANNEL
# =========================================

def get_channel(
    db: Session,
    channel_id: int
):

    return (
        ChannelRepo.get(
            db,
            channel_id
        )
    )


# =========================================
# LIST CHANNELS
# =========================================

def list_channels(
    db: Session,
    workspace_id: int
):

    return (
        ChannelRepo.list_active_by_workspace(
            db,
            workspace_id
        )
    )


# =========================================
# UPDATE CHANNEL
# =========================================

def update_channel(
    db: Session,
    channel: Channel,
    payload: ChannelUpdate
):

    update_data = payload.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            channel,
            key,
            value
        )

    return (
        ChannelRepo.save(
            db,
            channel
        )
    )


# =========================================
# ARCHIVE CHANNEL
# =========================================

def archive_channel(
    db: Session,
    channel: Channel
):

    channel.is_archived = True

    return (
        ChannelRepo.save(
            db,
            channel
        )
    )


# =========================================
# RESTORE CHANNEL
# =========================================

def restore_channel(
    db: Session,
    channel: Channel
):

    channel.is_archived = False

    return (
        ChannelRepo.save(
            db,
            channel
        )
    )


# =========================================
# JOIN CHANNEL
# =========================================

def join_channel(
    db: Session,
    channel_id: int,
    user_id: int
):

    existing = (
        ChannelMemberRepo
        .get_member(
            db,
            channel_id,
            user_id
        )
    )

    if existing:

        raise ValueError(
            "Already joined channel"
        )

    member = ChannelMember(
        channel_id=channel_id,
        user_id=user_id,
        is_muted=False,
        last_read_message_id=None
    )

    return (
        ChannelMemberRepo.create(
            db,
            member
        )
    )


# =========================================
# LEAVE CHANNEL
# =========================================

def leave_channel(
    db: Session,
    channel_id: int,
    user_id: int
):

    member = (
        ChannelMemberRepo
        .get_member(
            db,
            channel_id,
            user_id
        )
    )

    if not member:

        raise ValueError(
            "User not in channel"
        )

    ChannelMemberRepo.delete(
        db,
        member
    )

    return {
        "message":
        "Left channel successfully"
    }

    

def get_channel_members(
    db: Session,
    channel_id: int
):
    members = (
        db.query(ChannelMember, User)
        .join(
            User,
            ChannelMember.user_id == User.id
        )
        .filter(
            ChannelMember.channel_id == channel_id
        )
        .all()
    )

    return [
        {
            "id": member.id,
            "channel_id": member.channel_id,
            "user_id": member.user_id,
            "user_name": user.name,
            "email": user.email
        }
        for member, user in members
    ]