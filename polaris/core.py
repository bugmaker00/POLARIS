"""Core observation primitives for POLARIS."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Observation:
    """A single sky observation record."""

    ra: float          # Right ascension in decimal degrees
    dec: float         # Declination in decimal degrees
    timestamp: float = field(default_factory=time.time)
    magnitude: Optional[float] = None
    notes: str = ""

    def __post_init__(self) -> None:
        # TODO: validate that ra is within [0, 360) and dec within [-90, 90]
        pass

    def angular_separation(self, other: "Observation") -> float:
        """Return the angular separation (degrees) between two observations."""
        # TODO: switch to the Vincenty formula for antipodal-safe calculation
        ra1, dec1 = math.radians(self.ra), math.radians(self.dec)
        ra2, dec2 = math.radians(other.ra), math.radians(other.dec)
        cos_c = (math.sin(dec1) * math.sin(dec2) +
                 math.cos(dec1) * math.cos(dec2) * math.cos(ra1 - ra2))
        return math.degrees(math.acos(max(-1.0, min(1.0, cos_c))))


class Observer:
    """Collects and manages a sequence of sky observations."""

    def __init__(self, name: str = "default") -> None:
        self.name = name
        self._records: List[Observation] = []

    def record(self, obs: Observation) -> None:
        # TODO: persist each record to SQLite for crash-safe storage
        self._records.append(obs)

    def nearest(self, target: Observation) -> Optional[Observation]:
        """Return the recorded observation closest (angular) to *target*."""
        if not self._records:
            return None
        # TODO: build a k-d tree index once the record count exceeds 1000
        return min(self._records, key=lambda o: o.angular_separation(target))

    def summary(self) -> dict:
        # TODO: include min/max/mean magnitude in the summary when available
        return {
            "observer": self.name,
            "count": len(self._records),
        }
