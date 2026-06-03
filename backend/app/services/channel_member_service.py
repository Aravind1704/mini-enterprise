# app/services/channel_member_service.py

from sqlalchemy.orm import Session

from app.models.channel_member import (
    ChannelMember
)

from app.repositories.channel_member_repo import (
    ChannelMemberRepo
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
            "User already joined channel"
        )

    member = ChannelMember(
        channel_id=channel_id,
        user_id=user_id,
        is_muted=False,
        last_read_message_id=None
    )

    return (
        ChannelMemberRepo
        .create(
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
            "Member not found"
        )

    ChannelMemberRepo.delete(
        db,
        member
    )

    return {
        "message":
        "Left channel successfully"
    }


# =========================================
# LIST CHANNEL MEMBERS
# =========================================

def list_channel_members(
    db: Session,
    channel_id: int
):

    return (
        ChannelMemberRepo
        .list_members(
            db,
            channel_id
        )
    )


# =========================================
# GET MEMBER
# =========================================

def get_channel_member(
    db: Session,
    channel_id: int,
    user_id: int
):

    return (
        ChannelMemberRepo
        .get_member(
            db,
            channel_id,
            user_id
        )
    )


# =========================================
# MUTE CHANNEL
# =========================================

def mute_channel(
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
            "Member not found"
        )

    member.is_muted = True

    return (
        ChannelMemberRepo
        .save(
            db,
            member
        )
    )


# =========================================
# UNMUTE CHANNEL
# =========================================

def unmute_channel(
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
            "Member not found"
        )

    member.is_muted = False

    return (
        ChannelMemberRepo
        .save(
            db,
            member
        )
    )


# =========================================
# UPDATE LAST READ MESSAGE
# =========================================

def update_last_read_message(
    db: Session,
    channel_id: int,
    user_id: int,
    message_id: int
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
            "Member not found"
        )

    member.last_read_message_id = (
        message_id
    )

    return (
        ChannelMemberRepo
        .save(
            db,
            member
        )
    )