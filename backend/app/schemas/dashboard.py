from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_tasks: int
    todo: int
    in_progress: int
    review: int
    done: int
    pending_approvals: int

class TaskDistribution(BaseModel):
    status: str
    count: int