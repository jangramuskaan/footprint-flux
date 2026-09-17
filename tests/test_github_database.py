from sqlalchemy.orm import Session

from app.database import engine
from app.services.github_collection import collect_github_profile


def test_github_profile_saved_to_database():
    with Session(engine, expire_on_commit=False) as session:
        observations = collect_github_profile(
            session=session,
            username="jangramuskaan",
        )

        assert len(observations) == 7

        for observation in observations:
            assert observation.source_id is not None
            assert observation.value is not None

        print("\nGitHub observations saved:")
        for observation in observations:
            print(
                observation.key,
                "=",
                observation.value,
            )