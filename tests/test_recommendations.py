from unittest.mock import patch

from app.services.recommendations import generate_recommendations


def test_username_exposure_recommendation():
    with patch(
        "app.services.recommendations.calculate_exposure_score",
        return_value={
            "score": 15,
            "risk_level": "low",
            "factors": [
                {"factor": "Username exposure", "points": 15}
            ],
        },
    ):
        recommendations = generate_recommendations(
            session=None,
            person_id=None,
        )

    assert len(recommendations) == 1
    assert "username" in recommendations[0].lower()


def test_public_profile_exposure_recommendation():
    with patch(
        "app.services.recommendations.calculate_exposure_score",
        return_value={
            "score": 20,
            "risk_level": "low",
            "factors": [
                {"factor": "Public profiles", "points": 20}
            ],
        },
    ):
        recommendations = generate_recommendations(
            session=None,
            person_id=None,
        )

    assert len(recommendations) == 1
    assert "public profile" in recommendations[0].lower()


def test_default_recommendation_when_no_factors():
    with patch(
        "app.services.recommendations.calculate_exposure_score",
        return_value={
            "score": 0,
            "risk_level": "low",
            "factors": [],
        },
    ):
        recommendations = generate_recommendations(
            session=None,
            person_id=None,
        )

    assert len(recommendations) == 1
    assert "snapshots" in recommendations[0].lower()
