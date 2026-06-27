from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.core.slug import make_slug
from app.core.security import hash_password
from app.models.Team import Team
from app.models.ai_meeting_summary import AiMeetingSummary
from app.models.meeting import Meeting
from app.models.meeting_note import MeetingNote
from app.models.project import Project
from app.models.project_document import ProjectDocument
from app.models.project_team import ProjectTeam
from app.models.task import Task
from app.models.team_member import TeamMember
from app.models.tenant import Tenant
from app.models.user import User
from app.models.workspace_member import WorkspaceMember
from app.models.channel_member import ChannelMember
from app.models.workspace import Workspace
from app.models.channel import Channel


UPLOAD_DIR = Path("uploads") / "project_documents"


SAMPLE_WORKFLOWS: dict[str, dict[str, Any]] = {
    "software": {
        "tenant": {
            "name": "TechNova Solutions Pvt Ltd",
            "contact_email": "admin@technova.example.com",
            "industry": "Software",
        },
        "workspace": {
            "name": "Engineering Workspace",
            "description": "Engineering delivery workspace for product development.",
        },
        "users": [
            {
                "name": "TechNova Admin",
                "email": "admin@technova.example.com",
                "password": "DemoPass123!",
                "role": "admin",
            },
            {
                "name": "Backend Lead",
                "email": "backend.lead@technova.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "Backend Team",
            },
            {
                "name": "Frontend Lead",
                "email": "frontend.lead@technova.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "Frontend Team",
            },
            {
                "name": "QA Lead",
                "email": "qa.lead@technova.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "QA Team",
            },
            {
                "name": "DevOps Lead",
                "email": "devops.lead@technova.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "DevOps Team",
            },
        ],
        "teams": [
            "Backend Team",
            "Frontend Team",
            "QA Team",
            "DevOps Team",
        ],
        "project": {
            "name": "Enterprise Flow SaaS Development",
            "description": "Enterprise product delivery workflow for a SaaS platform.",
            "status": "ACTIVE",
            "priority": "HIGH",
        },
        "channels": [
            "backend",
            "frontend",
            "testing",
            "deployment",
        ],
        "tasks": [
            {
                "title": "Implement Login API",
                "team": "Backend Team",
                "assignee": "backend.lead@technova.example.com",
            },
            {
                "title": "Create Dashboard UI",
                "team": "Frontend Team",
                "assignee": "frontend.lead@technova.example.com",
            },
            {
                "title": "Test Approval Workflow",
                "team": "QA Team",
                "assignee": "qa.lead@technova.example.com",
            },
            {
                "title": "Deploy Release Build",
                "team": "DevOps Team",
                "assignee": "devops.lead@technova.example.com",
            },
        ],
        "meetings": [
            {
                "title": "Sprint Planning",
                "note": "Plan the sprint scope and confirm owner allocation.",
                "summary": "Sprint planning for the SaaS delivery increment.",
                "decisions": "Commit to API, UI, QA, and deployment milestones.",
                "risks": "Release coordination across backend and frontend teams.",
                "action_items": "Finalize user stories and sprint board before EOD.",
            },
            {
                "title": "Daily Standup",
                "note": "Track blockers and daily delivery progress.",
                "summary": "Daily execution sync for delivery teams.",
                "decisions": "Continue with current sprint priorities.",
                "risks": "Cross-team dependencies on shared APIs.",
                "action_items": "Resolve blockers before the next standup.",
            },
            {
                "title": "Sprint Review",
                "note": "Demonstrate completed work to stakeholders.",
                "summary": "Sprint review for completed platform features.",
                "decisions": "Approve the release candidate after QA sign-off.",
                "risks": "Potential defects found late in the release window.",
                "action_items": "Collect feedback and update the backlog.",
            },
            {
                "title": "Client Demo",
                "note": "Showcase the working product increment to the client.",
                "summary": "Client-facing demo of the SaaS upgrade.",
                "decisions": "Client sign-off required after the demo.",
                "risks": "Demo scope may shift based on client feedback.",
                "action_items": "Prepare demo script and backup screenshots.",
            },
        ],
        "documents": [
            {
                "file_name": "Requirement Specification.pdf",
                "mime_type": "application/pdf",
                "document_type": "REQUIREMENT",
                "content": "TechNova requirement specification for enterprise flow SaaS development.",
            },
            {
                "file_name": "API Contract.docx",
                "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "document_type": "DESIGN",
                "content": "API contract and integration notes for the enterprise flow project.",
            },
            {
                "file_name": "Deployment Guide.pdf",
                "mime_type": "application/pdf",
                "document_type": "RELEASE",
                "content": "Deployment guide for the SaaS release workflow.",
            },
            {
                "file_name": "Test Plan.xlsx",
                "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "document_type": "TEST",
                "content": "Test plan checklist for the SaaS project.",
            },
        ],
    },
    "bank": {
        "tenant": {
            "name": "ABC Bank",
            "contact_email": "admin@abcbank.example.com",
            "industry": "Banking",
        },
        "workspace": {
            "name": "Digital Banking Workspace",
            "description": "Digital banking transformation workspace.",
        },
        "users": [
            {
                "name": "ABC Bank Admin",
                "email": "admin@abcbank.example.com",
                "password": "DemoPass123!",
                "role": "admin",
            },
            {
                "name": "Core Banking Lead",
                "email": "core.banking@abcbank.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "Core Banking Team",
            },
            {
                "name": "Mobile Banking Lead",
                "email": "mobile.banking@abcbank.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "Mobile Banking Team",
            },
            {
                "name": "Security Analyst",
                "email": "security@abcbank.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "Security Team",
            },
            {
                "name": "QA Analyst",
                "email": "qa@abcbank.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "QA Team",
            },
            {
                "name": "Compliance Analyst",
                "email": "compliance@abcbank.example.com",
                "password": "DemoPass123!",
                "role": "employee",
                "team": "Compliance Team",
            },
        ],
        "teams": [
            "Core Banking Team",
            "Mobile Banking Team",
            "Security Team",
            "QA Team",
            "Compliance Team",
        ],
        "project": {
            "name": "Mobile Banking App Upgrade",
            "description": "Mobile banking upgrade for security, testing, and release readiness.",
            "status": "ACTIVE",
            "priority": "CRITICAL",
        },
        "channels": [
            "security-review",
            "mobile-ui",
            "api-integration",
            "uat-testing",
        ],
        "tasks": [
            {
                "title": "Implement OTP Login",
                "team": "Mobile Banking Team",
                "assignee": "mobile.banking@abcbank.example.com",
            },
            {
                "title": "Review Security Compliance",
                "team": "Security Team",
                "assignee": "security@abcbank.example.com",
            },
            {
                "title": "Test Fund Transfer Flow",
                "team": "QA Team",
                "assignee": "qa@abcbank.example.com",
            },
            {
                "title": "Prepare UAT Report",
                "team": "Compliance Team",
                "assignee": "compliance@abcbank.example.com",
            },
        ],
        "meetings": [
            {
                "title": "Security Review Meeting",
                "note": "Confirm OTP, encryption, and compliance findings.",
                "summary": "Security review for the mobile banking upgrade.",
                "decisions": "Approve the security review checklist before UAT.",
                "risks": "Regulatory issues may block release if unresolved.",
                "action_items": "Complete security sign-off and update the checklist.",
            },
            {
                "title": "UAT Planning Meeting",
                "note": "Prepare the UAT scope and test readiness.",
                "summary": "UAT planning for the mobile banking release.",
                "decisions": "Schedule UAT after security approval.",
                "risks": "Insufficient test coverage for transfer workflows.",
                "action_items": "Publish UAT scope and test cases.",
            },
            {
                "title": "Release Approval Meeting",
                "note": "Review release readiness and rollout approval.",
                "summary": "Final release approval for the banking upgrade.",
                "decisions": "Release only after QA and compliance sign-off.",
                "risks": "Late defects can delay production rollout.",
                "action_items": "Collect approvals and prepare release notes.",
            },
        ],
        "documents": [
            {
                "file_name": "RBI Compliance Checklist.pdf",
                "mime_type": "application/pdf",
                "document_type": "REQUIREMENT",
                "content": "RBI compliance checklist for the mobile banking upgrade.",
            },
            {
                "file_name": "Security Audit Report.pdf",
                "mime_type": "application/pdf",
                "document_type": "DESIGN",
                "content": "Security audit findings and remediation items for banking release.",
            },
            {
                "file_name": "UAT Test Cases.xlsx",
                "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "document_type": "TEST",
                "content": "UAT test cases for mobile banking upgrade validation.",
            },
        ],
    },
}


def _touch_document(
    tenant_slug: str,
    project_slug: str,
    file_name: str,
    content: str,
) -> str:
    directory = UPLOAD_DIR / tenant_slug / project_slug
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / file_name
    path.write_text(content, encoding="utf-8")
    return str(path)


def _get_or_create_user(
    db: Session,
    *,
    tenant_id: int,
    name: str,
    email: str,
    password: str,
    role: str,
) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.tenant_id = tenant_id
        user.role = role
        user.is_active = True
        return user

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role=role,
        is_active=True,
        tenant_id=tenant_id,
    )
    db.add(user)
    db.flush()
    return user


def _get_or_create_tenant(db: Session, spec: dict[str, Any]) -> Tenant:
    slug = make_slug(spec["name"])
    tenant = db.query(Tenant).filter(Tenant.slug == slug).first()
    if tenant:
        tenant.contact_email = spec["contact_email"]
        tenant.industry = spec["industry"]
        tenant.status = "ACTIVE"
        return tenant

    tenant = Tenant(
        name=spec["name"],
        slug=slug,
        contact_email=spec["contact_email"],
        industry=spec["industry"],
        status="ACTIVE",
    )
    db.add(tenant)
    db.flush()
    return tenant


def _get_or_create_workspace(
    db: Session,
    *,
    tenant_id: int,
    name: str,
    description: str,
    created_by: int,
) -> Workspace:
    slug = make_slug(name)
    workspace = (
        db.query(Workspace)
        .filter(Workspace.tenant_id == tenant_id, Workspace.slug == slug)
        .first()
    )
    if workspace:
        workspace.name = name
        workspace.description = description
        workspace.created_by = created_by
        workspace.visibility = "PUBLIC"
        workspace.is_archived = False
        return workspace

    workspace = Workspace(
        tenant_id=tenant_id,
        name=name,
        slug=slug,
        description=description,
        visibility="PUBLIC",
        created_by=created_by,
        is_archived=False,
    )
    db.add(workspace)
    db.flush()
    return workspace


def _get_or_create_team(
    db: Session,
    *,
    tenant_id: int,
    workspace_id: int,
    name: str,
    description: str,
    created_by: int,
) -> Team:
    team = (
        db.query(Team)
        .filter(Team.tenant_id == tenant_id, Team.workspace_id == workspace_id, Team.name == name)
        .first()
    )
    if team:
        team.description = description
        team.created_by = created_by
        team.is_active = True
        return team

    team = Team(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        name=name,
        description=description,
        created_by=created_by,
        is_active=True,
    )
    db.add(team)
    db.flush()
    return team


def _get_or_create_team_member(
    db: Session,
    *,
    tenant_id: int,
    team_id: int,
    user_id: int,
    role: str = "MEMBER",
) -> TeamMember:
    member = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
        .first()
    )
    if member:
        member.tenant_id = tenant_id
        member.role = role
        member.is_active = True
        return member

    member = TeamMember(
        tenant_id=tenant_id,
        team_id=team_id,
        user_id=user_id,
        role=role,
        is_active=True,
    )
    db.add(member)
    db.flush()
    return member


def _get_or_create_workspace_member(
    db: Session,
    *,
    workspace_id: int,
    user_id: int,
    role: str = "MEMBER",
) -> WorkspaceMember:
    member = (
        db.query(WorkspaceMember)
        .filter(WorkspaceMember.workspace_id == workspace_id, WorkspaceMember.user_id == user_id)
        .first()
    )
    if member:
        member.role = role
        member.is_active = True
        return member

    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user_id,
        role=role,
        is_active=True,
    )
    db.add(member)
    db.flush()
    return member


def _get_or_create_project(
    db: Session,
    *,
    tenant_id: int,
    workspace_id: int,
    owner_id: int,
    name: str,
    description: str,
    status: str,
    priority: str,
) -> Project:
    project = (
        db.query(Project)
        .filter(Project.tenant_id == tenant_id, Project.workspace_id == workspace_id, Project.name == name)
        .first()
    )
    if project:
        project.owner_id = owner_id
        project.description = description
        project.status = status
        project.priority = priority
        return project

    project = Project(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        owner_id=owner_id,
        name=name,
        description=description,
        status=status,
        priority=priority,
    )
    db.add(project)
    db.flush()
    return project


def _get_or_create_project_team(
    db: Session,
    *,
    tenant_id: int,
    project_id: int,
    team_id: int,
) -> ProjectTeam:
    assignment = (
        db.query(ProjectTeam)
        .filter(ProjectTeam.project_id == project_id, ProjectTeam.team_id == team_id)
        .first()
    )
    if assignment:
        assignment.tenant_id = tenant_id
        return assignment

    assignment = ProjectTeam(
        tenant_id=tenant_id,
        project_id=project_id,
        team_id=team_id,
    )
    db.add(assignment)
    db.flush()
    return assignment


def _get_or_create_channel(
    db: Session,
    *,
    tenant_id: int,
    workspace_id: int,
    project_id: int,
    created_by: int,
    name: str,
    description: str,
) -> Channel:
    channel = (
        db.query(Channel)
        .filter(Channel.workspace_id == workspace_id, Channel.project_id == project_id, Channel.name == name)
        .first()
    )
    if channel:
        channel.description = description
        channel.created_by = created_by
        channel.is_archived = False
        return channel

    channel = Channel(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        project_id=project_id,
        name=name,
        description=description,
        channel_type="PUBLIC",
        created_by=created_by,
        is_archived=False,
    )
    db.add(channel)
    db.flush()
    return channel


def _get_or_create_channel_member(
    db: Session,
    *,
    channel_id: int,
    user_id: int,
) -> ChannelMember:
    member = (
        db.query(ChannelMember)
        .filter(ChannelMember.channel_id == channel_id, ChannelMember.user_id == user_id)
        .first()
    )
    if member:
        return member

    member = ChannelMember(
        channel_id=channel_id,
        user_id=user_id,
    )
    db.add(member)
    db.flush()
    return member


def _get_or_create_task(
    db: Session,
    *,
    tenant_id: int,
    workspace_id: int,
    project_id: int,
    team_id: int,
    created_by: int,
    title: str,
    description: str,
    status: str,
    priority: str,
    due_date: datetime,
    assigned_to_id: int,
) -> Task:
    task = (
        db.query(Task)
        .filter(Task.project_id == project_id, Task.title == title)
        .first()
    )
    if task:
        task.tenant_id = tenant_id
        task.workspace_id = workspace_id
        task.team_id = team_id
        task.created_by_id = created_by
        task.assigned_to_id = assigned_to_id
        task.description = description
        task.status = status
        task.priority = priority
        task.due_date = due_date
        return task

    task = Task(
        tenant_id=tenant_id,
        workspace_id=workspace_id,
        project_id=project_id,
        team_id=team_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
        created_by_id=created_by,
        assigned_to_id=assigned_to_id,
    )
    db.add(task)
    db.flush()
    return task


def _get_or_create_meeting(
    db: Session,
    *,
    tenant_id: int,
    project_id: int,
    created_by: int,
    title: str,
    description: str,
    start_time: datetime,
    end_time: datetime,
) -> Meeting:
    meeting = (
        db.query(Meeting)
        .filter(Meeting.project_id == project_id, Meeting.title == title)
        .first()
    )
    if meeting:
        meeting.description = description
        meeting.start_time = start_time
        meeting.end_time = end_time
        meeting.created_by = created_by
        meeting.status = "SCHEDULED"
        return meeting

    meeting = Meeting(
        tenant_id=tenant_id,
        project_id=project_id,
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
        created_by=created_by,
        status="SCHEDULED",
    )
    db.add(meeting)
    db.flush()
    return meeting


def _get_or_create_note(
    db: Session,
    *,
    tenant_id: int,
    meeting_id: int,
    created_by: int,
    notes: str,
) -> MeetingNote:
    note = (
        db.query(MeetingNote)
        .filter(MeetingNote.meeting_id == meeting_id)
        .first()
    )
    if note:
        note.tenant_id = tenant_id
        note.created_by = created_by
        note.notes = notes
        return note

    note = MeetingNote(
        tenant_id=tenant_id,
        meeting_id=meeting_id,
        created_by=created_by,
        notes=notes,
    )
    db.add(note)
    db.flush()
    return note


def _get_or_create_summary(
    db: Session,
    *,
    tenant_id: int,
    meeting_id: int,
    summary: str,
    action_items: str,
    risks: str,
    decisions: str,
) -> AiMeetingSummary:
    existing = (
        db.query(AiMeetingSummary)
        .filter(AiMeetingSummary.meeting_id == meeting_id)
        .first()
    )
    if existing:
        existing.tenant_id = tenant_id
        existing.summary = summary
        existing.action_items = action_items
        existing.risks = risks
        existing.decisions = decisions
        return existing

    summary_obj = AiMeetingSummary(
        tenant_id=tenant_id,
        meeting_id=meeting_id,
        summary=summary,
        action_items=action_items,
        risks=risks,
        decisions=decisions,
    )
    db.add(summary_obj)
    db.flush()
    return summary_obj


def _get_or_create_document(
    db: Session,
    *,
    tenant_id: int,
    project_id: int,
    uploaded_by: int,
    tenant_slug: str,
    project_slug: str,
    file_name: str,
    mime_type: str,
    document_type: str,
    content: str,
) -> ProjectDocument:
    document = (
        db.query(ProjectDocument)
        .filter(ProjectDocument.project_id == project_id, ProjectDocument.file_name == file_name)
        .first()
    )
    file_path = _touch_document(tenant_slug, project_slug, file_name, content)

    if document:
        document.tenant_id = tenant_id
        document.uploaded_by = uploaded_by
        document.file_path = file_path
        document.file_size = len(content.encode("utf-8"))
        document.mime_type = mime_type
        document.document_type = document_type
        return document

    document = ProjectDocument(
        tenant_id=tenant_id,
        project_id=project_id,
        uploaded_by=uploaded_by,
        file_name=file_name,
        file_path=file_path,
        file_size=len(content.encode("utf-8")),
        mime_type=mime_type,
        document_type=document_type,
    )
    db.add(document)
    db.flush()
    return document


def seed_sample_workflow(db: Session, example_key: str) -> dict[str, Any]:
    key = example_key.strip().lower()
    if key not in SAMPLE_WORKFLOWS:
        raise ValueError("Unknown sample workflow")

    spec = SAMPLE_WORKFLOWS[key]
    tenant = _get_or_create_tenant(db, spec["tenant"])
    tenant_slug = tenant.slug

    users: dict[str, User] = {}
    for user_spec in spec["users"]:
        users[user_spec["email"]] = _get_or_create_user(
            db,
            tenant_id=tenant.id,
            name=user_spec["name"],
            email=user_spec["email"],
            password=user_spec["password"],
            role=user_spec["role"],
        )

    admin_user = next(user for user in users.values() if user.role == "admin")

    workspace = _get_or_create_workspace(
        db,
        tenant_id=tenant.id,
        name=spec["workspace"]["name"],
        description=spec["workspace"]["description"],
        created_by=admin_user.id,
    )

    teams: dict[str, Team] = {}
    for team_name in spec["teams"]:
        teams[team_name] = _get_or_create_team(
            db,
            tenant_id=tenant.id,
            workspace_id=workspace.id,
            name=team_name,
            description=f"{team_name} for {tenant.name}",
            created_by=admin_user.id,
        )

    for user in users.values():
        _get_or_create_workspace_member(
            db,
            workspace_id=workspace.id,
            user_id=user.id,
            role="ADMIN" if user.id == admin_user.id else "MEMBER",
        )

    for user_spec in spec["users"]:
        team_name = user_spec.get("team")
        if not team_name:
            continue
        _get_or_create_team_member(
            db,
            tenant_id=tenant.id,
            team_id=teams[team_name].id,
            user_id=users[user_spec["email"]].id,
            role="MEMBER",
        )

    project = _get_or_create_project(
        db,
        tenant_id=tenant.id,
        workspace_id=workspace.id,
        owner_id=admin_user.id,
        name=spec["project"]["name"],
        description=spec["project"]["description"],
        status=spec["project"]["status"],
        priority=spec["project"]["priority"],
    )
    project_slug = make_slug(project.name)

    project_teams = []
    for team_name in spec["teams"]:
        project_teams.append(
            _get_or_create_project_team(
                db,
                tenant_id=tenant.id,
                project_id=project.id,
                team_id=teams[team_name].id,
            )
        )

    channels = []
    for channel_name in spec["channels"]:
        channels.append(
            _get_or_create_channel(
                db,
                tenant_id=tenant.id,
                workspace_id=workspace.id,
                project_id=project.id,
                created_by=admin_user.id,
                name=channel_name,
                description=f"Project channel for {channel_name}",
            )
        )

    for channel in channels:
        for user in users.values():
            _get_or_create_channel_member(
                db,
                channel_id=channel.id,
                user_id=user.id,
            )

    task_date = datetime.utcnow() + timedelta(days=7)
    tasks = []
    for task_spec in spec["tasks"]:
        assignee = users[task_spec["assignee"]]
        team = teams[task_spec["team"]]
        tasks.append(
            _get_or_create_task(
                db,
                tenant_id=tenant.id,
                workspace_id=workspace.id,
                project_id=project.id,
                team_id=team.id,
                created_by=admin_user.id,
                title=task_spec["title"],
                description=f"{task_spec['title']} for {project.name}",
                status="TODO",
                priority="HIGH" if key == "bank" else "MEDIUM",
                due_date=task_date,
                assigned_to_id=assignee.id,
            )
        )
        task_date += timedelta(days=1)

    meetings = []
    meeting_start = datetime.utcnow() + timedelta(days=1)
    for meeting_spec in spec["meetings"]:
        meeting = _get_or_create_meeting(
            db,
            tenant_id=tenant.id,
            project_id=project.id,
            created_by=admin_user.id,
            title=meeting_spec["title"],
            description=f"{meeting_spec['title']} for {project.name}",
            start_time=meeting_start,
            end_time=meeting_start + timedelta(hours=1),
        )
        _get_or_create_note(
            db,
            tenant_id=tenant.id,
            meeting_id=meeting.id,
            created_by=admin_user.id,
            notes=meeting_spec["note"],
        )
        _get_or_create_summary(
            db,
            tenant_id=tenant.id,
            meeting_id=meeting.id,
            summary=meeting_spec["summary"],
            action_items=meeting_spec["action_items"],
            risks=meeting_spec["risks"],
            decisions=meeting_spec["decisions"],
        )
        meetings.append(meeting)
        meeting_start += timedelta(days=1)

    documents = []
    for document_spec in spec["documents"]:
        documents.append(
            _get_or_create_document(
                db,
                tenant_id=tenant.id,
                project_id=project.id,
                uploaded_by=admin_user.id,
                tenant_slug=tenant_slug,
                project_slug=project_slug,
                file_name=document_spec["file_name"],
                mime_type=document_spec["mime_type"],
                document_type=document_spec["document_type"],
                content=document_spec["content"],
            )
        )

    db.commit()

    return {
        "example_key": key,
        "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "slug": tenant.slug,
        },
        "workspace": {
            "id": workspace.id,
            "name": workspace.name,
            "slug": workspace.slug,
        },
        "project": {
            "id": project.id,
            "name": project.name,
        },
        "users": [
            {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
            for user in users.values()
        ],
        "teams": [
            {"id": team.id, "name": team.name}
            for team in teams.values()
        ],
        "project_teams": [
            {"id": assignment.id, "project_id": assignment.project_id, "team_id": assignment.team_id}
            for assignment in project_teams
        ],
        "channels": [
            {"id": channel.id, "name": channel.name, "project_id": channel.project_id}
            for channel in channels
        ],
        "tasks": [
            {"id": task.id, "title": task.title, "team_id": task.team_id, "assigned_to_id": task.assigned_to_id}
            for task in tasks
        ],
        "meetings": [
            {"id": meeting.id, "title": meeting.title}
            for meeting in meetings
        ],
        "documents": [
            {"id": document.id, "file_name": document.file_name}
            for document in documents
        ],
    }
