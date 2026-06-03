from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from app.services.sla_monitor_service import (
    monitor_sla
)

scheduler = BackgroundScheduler()

# FAST TESTING
scheduler.add_job(
    monitor_sla,
    "interval",
    seconds=5
)

scheduler.start()

print("SLA SCHEDULER STARTED")