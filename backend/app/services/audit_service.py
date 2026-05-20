from app.repositories import (
    audit_repo as repo
)


# =====================================================
# LIST LOGS SERVICE
# =====================================================

def list_logs_service(
    db
):

    return repo.list_all_logs(
        db
    )