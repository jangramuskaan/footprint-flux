from app.collectors.github import GitHubCollector


def test_real_github_profile():
    collector = GitHubCollector("jangramuskaan")

    observations = collector.collect()

    assert len(observations) == 7

    for observation in observations:
        print(
            observation["category"],
            "|",
            observation["key"],
            "|",
            observation["value"],
        )