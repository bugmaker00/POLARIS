"""Unit tests for polaris.core."""

import math
import pytest

from polaris.core import Observation, Observer


def test_observation_defaults():
    obs = Observation(ra=37.95, dec=89.26)
    assert obs.ra == pytest.approx(37.95)
    assert obs.dec == pytest.approx(89.26)
    assert obs.magnitude is None
    assert obs.notes == ""


def test_angular_separation_same_point():
    obs = Observation(ra=100.0, dec=45.0)
    assert obs.angular_separation(obs) == pytest.approx(0.0, abs=1e-9)


def test_angular_separation_known():
    # Sirius -> Canopus, well-known separation ≈ 36.2°
    sirius   = Observation(ra=101.29, dec=-16.72)
    canopus  = Observation(ra=95.99,  dec=-52.70)
    sep = sirius.angular_separation(canopus)
    assert 35.0 < sep < 38.0


def test_observer_nearest_empty():
    obs = Observer("test")
    result = obs.nearest(Observation(ra=0.0, dec=0.0))
    assert result is None


def test_observer_nearest_single():
    obs = Observer("test")
    recorded = Observation(ra=37.95, dec=89.26)
    obs.record(recorded)
    target = Observation(ra=38.0, dec=89.0)
    assert obs.nearest(target) is recorded


def test_observer_summary():
    obs = Observer("test")
    obs.record(Observation(ra=0.0, dec=0.0))
    obs.record(Observation(ra=10.0, dec=10.0))
    s = obs.summary()
    assert s["count"] == 2
    # TODO: assert magnitude stats once summary() includes them
    # TODO: assert observer name appears correctly in the output dict
