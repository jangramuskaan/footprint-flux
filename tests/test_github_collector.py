import json

from app.collectors.github import GitHubCollector


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def read(self):
        return json.dumps(
            {
                "login": "testuser",
                "name": "Test User",
                "bio": "A test profile",
                "public_repos": 12,
                "followers": 5,
                "following": 7,
                "html_url": "https://github.com/testuser",
            }
        ).encode("utf-8")


def test_github_collector(monkeypatch):
    def fake_urlopen(request, timeout):
        return FakeResponse()

    monkeypatch.setattr(
        "app.collectors.github.urlopen",
        fake_urlopen,
    )

    collector = GitHubCollector("testuser")

    observations = collector.collect()

    assert len(observations) == 7

    assert observations[0] == {
        "category": "profile",
        "key": "username",
        "value": "testuser",
    }

    assert observations[3]["key"] == "public_repos"
    assert observations[3]["value"] == "12"

    assert observations[6]["key"] == "profile_url"