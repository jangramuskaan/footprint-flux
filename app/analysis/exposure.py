from app.models import Observation


def calculate_exposure_score(observations: list[Observation]) -> int:
    """
    Calculate a simple digital exposure score from 0 to 100.

    Higher score = more publicly exposed information.
    """

    if not observations:
        return 0

    score = 0

    for observation in observations:
        category = observation.category.lower()

        if category == "identity":
            score += 20

        elif category == "contact":
            score += 25

        elif category == "profile":
            score += 15

        elif category == "activity":
            score += 10

        else:
            score += 5

    return min(score, 100)