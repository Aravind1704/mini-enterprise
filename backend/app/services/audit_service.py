<<<<<<< HEAD
from sqlalchemy.orm import Session

from app.repositories.audit_repo import AuditRepo
=======
from app.repositories import (
    audit_repo as repo
)
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2


# =====================================================
# LIST LOGS SERVICE
# =====================================================

def list_logs_service(
<<<<<<< HEAD
    db: Session
):

    return AuditRepo.list_all(
=======
    db
):

    return repo.list_all_logs(
>>>>>>> 4500000c8c54ec045a9125ffb74854e6cb5209d2
        db
    )