from sqlalchemy.orm import Session

from app.repositories.audit_repo import AuditRepo



# =====================================================
# LIST LOGS SERVICE
# =====================================================

def list_logs_service(

    db: Session
):

    return AuditRepo.list_all(
        db
    )