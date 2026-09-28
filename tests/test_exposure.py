from datetime import datetime, timezone
from uuid import uuid4

from app.models import Observation
from app.analysis.exposure import calculate_exposure_score


def make_observation(category: str) -> Observation:
    return Observation(
        id=uuid4(),
        source_id=uuid4(),
        category=category,
        key="test",
        value="test_value",
        observed_at=datetime.now(timezone.utc),
    )


def test_empty_observations_have_zero_score():
    score = calculate_exposure_score([])

    assert score == 0


def test_exposure_score_is_calculated():
    observations = [
        make_observation("identity"),
        make_observation("profile"),
        make_observation("activity"),
    ]

    score = calculate_exposure_score(observations)

    assert score == 45


def test_exposure_score_is_capped_at_100():
    observations = [
        make_observation("identity"),
        make_observation("identity"),
        make_observation("identity"),
        make_observation("identity"),
        make_observation("identity"),
        make_observation("contact"),
    ]

    score = calculate_exposure_score(observations)

    assert score == 100