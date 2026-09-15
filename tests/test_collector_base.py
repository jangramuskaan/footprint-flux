import pytest

from app.collectors.base import Collector


def test_collector_requires_collect():
    with pytest.raises(TypeError):
        Collector()