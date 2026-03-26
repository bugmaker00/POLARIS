"""Star-tracker subsystem – identifies bright stars from raw observations."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

from polaris.core import Observation

logger = logging.getLogger(__name__)


# Minimal bright-star catalogue (name -> (ra_deg, dec_deg, magnitude))
CATALOGUE: Dict[str, Tuple[float, float, float]] = {
    "Polaris":   (37.95, 89.26, 1.97),
    "Sirius":    (101.29, -16.72, -1.46),
    "Canopus":   (95.99, -52.70, -0.74),
    "Arcturus":  (213.92, 19.18, -0.05),
    "Vega":      (279.23, 38.78, 0.03),
}


class StarTracker:
    """Match an observation to the nearest catalogue entry."""

    # TODO: load catalogue from an external CSV file instead of hard-coding it
    MATCH_RADIUS_DEG: float = 2.0

    def __init__(self, match_radius: float = MATCH_RADIUS_DEG) -> None:
        self.match_radius = match_radius
        # TODO: add a calibration offset (delta_ra, delta_dec) per session
        self._calibration: Tuple[float, float] = (0.0, 0.0)

    def identify(self, obs: Observation) -> Optional[str]:
        """Return the star name if *obs* falls within *match_radius* of a catalogue entry."""
        best_name: Optional[str] = None
        best_sep = float("inf")
        for name, (ra, dec, _mag) in CATALOGUE.items():
            ref = Observation(ra=ra, dec=dec)
            sep = obs.angular_separation(ref)
            if sep < best_sep:
                best_sep = sep
                best_name = name
        if best_sep <= self.match_radius:
            return best_name
        # TODO: emit a WARNING log when no match is found within the radius
        return None

    def batch_identify(self, observations: List[Observation]) -> Dict[int, Optional[str]]:
        """Identify all observations; returns {index: star_name_or_None}."""
        # TODO: parallelise with a thread pool for large batches (> 500 items)
        return {i: self.identify(obs) for i, obs in enumerate(observations)}
