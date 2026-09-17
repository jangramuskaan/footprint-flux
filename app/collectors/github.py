import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from typing import Any


GITHUB_API_URL = "https://api.github.com"


class GitHubCollector:
    def __init__(self, username: str):
        self.username = username

    def collect(self) -> list[dict[str, Any]]:
        url = f"{GITHUB_API_URL}/users/{self.username}"

        token = os.getenv("GITHUB_TOKEN")

        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "Footprint-Flux",
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        request = Request(
            url,
            headers=headers,
        )

        try:
            with urlopen(request, timeout=10) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

        except HTTPError as error:
            raise RuntimeError(
                f"GitHub API returned HTTP {error.code}"
            ) from error

        except URLError as error:
            raise RuntimeError(
                "Unable to connect to GitHub API"
            ) from error

        return [
            {
                "category": "profile",
                "key": "username",
                "value": data["login"],
            },
            {
                "category": "profile",
                "key": "name",
                "value": data.get("name") or "",
            },
            {
                "category": "profile",
                "key": "bio",
                "value": data.get("bio") or "",
            },
            {
                "category": "profile",
                "key": "public_repos",
                "value": str(data.get("public_repos", 0)),
            },
            {
                "category": "profile",
                "key": "followers",
                "value": str(data.get("followers", 0)),
            },
            {
                "category": "profile",
                "key": "following",
                "value": str(data.get("following", 0)),
            },
            {
                "category": "profile",
                "key": "profile_url",
                "value": data["html_url"],
            },
        ]