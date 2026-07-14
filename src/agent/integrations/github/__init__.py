"""GitHub integration: issue triage and PR helpers (optional; uses PyGithub)."""

from ...runtime.errors import AgentError
from ...runtime.logging import get_logger

logger = get_logger("agent.github")


def summarize_issue(repo: str, issue_number: int, provider: str = None) -> str:
    try:
        from github import Github
    except ImportError as exc:
        raise AgentError("PyGithub is not installed. Run: pip install PyGithub") from exc
    from ...app import get_agent

    agent = get_agent(provider=provider)
    token = __import__("os").environ.get("GITHUB_TOKEN")
    gh = Github(token) if token else Github()
    issue = gh.get_repo(repo).get_issue(issue_number)
    return agent.chat(f"Summarize and propose next steps for this issue:\n{issue.body}")
