# app/routes/channel_routes.py

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from typing import List

from app.database import get_db

from app.schemas.channel import (
    ChannelCreate,
    ChannelUpdate,
    ChannelOut
)

from app.services.channel_service import (
    create_channel,
    get_channel,
    list_channels,
    update_channel,
    archive_channel,
    restore_channel,
    join_channel,
    leave_channel
)

router = APIRouter(
    tags=["Channel Management"]
)

# =========================================
# CREATE CHANNEL
# =========================================

@router.post(
    "/channels",
    response_model=ChannelOut,
    status_code=status.HTTP_201_CREATED
)
def api_create_channel(
    payload: ChannelCreate,
    db: Session = Depends(get_db)
):

    try:

        return create_channel(
            db,
            payload,
            payload.created_by
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================
# LIST CHANNELS BY WORKSPACE
# =========================================

@router.get(
    "/workspaces/{workspace_id}/channels",
    response_model=List[ChannelOut]
)
def api_list_channels(
    workspace_id: int,
    db: Session = Depends(get_db)
):

    return list_channels(
        db,
        workspace_id
    )


# =========================================
# GET CHANNEL DETAILS
# =========================================

@router.get(
    "/channels/{channel_id}",
    response_model=ChannelOut
)
def api_get_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):

    channel = get_channel(
        db,
        channel_id
    )

    if not channel:

        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return channel


# =========================================
# UPDATE CHANNEL
# =========================================

@router.put(
    "/channels/{channel_id}",
    response_model=ChannelOut
)
def api_update_channel(
    channel_id: int,
    payload: ChannelUpdate,
    db: Session = Depends(get_db)
):

    channel = get_channel(
        db,
        channel_id
    )

    if not channel:

        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return update_channel(
        db,
        channel,
        payload
    )


# =========================================
# ARCHIVE CHANNEL
# =========================================

@router.patch(
    "/channels/{channel_id}/archive",
    response_model=ChannelOut
)
def api_archive_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):

    channel = get_channel(
        db,
        channel_id
    )

    if not channel:

        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return archive_channel(
        db,
        channel
    )


# =========================================
# RESTORE CHANNEL
# =========================================

@router.patch(
    "/channels/{channel_id}/restore",
    response_model=ChannelOut
)
def api_restore_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):

    channel = get_channel(
        db,
        channel_id
    )

    if not channel:

        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return restore_channel(
        db,
        channel
    )


# =========================================
# JOIN CHANNEL
# =========================================

@router.post(
    "/channels/{channel_id}/join"
)
def api_join_channel(
    channel_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    try:

        return join_channel(
            db,
            channel_id,
            user_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================
# LEAVE CHANNEL
# =========================================

@router.post(
    "/channels/{channel_id}/leave"
)
def api_leave_channel(
    channel_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    try:

        return leave_channel(
            db,
            channel_id,
            user_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )