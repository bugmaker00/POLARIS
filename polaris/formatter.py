"""Output formatters for POLARIS observation records."""

from __future__ import annotations

import csv
import io
import json
from typing import List

from polaris.core import Observation


class Formatter:
    """Convert lists of :class:`Observation` objects to various text formats."""

    # ------------------------------------------------------------------
    # CSV
    # ------------------------------------------------------------------

    @staticmethod
    def to_csv(observations: List[Observation]) -> str:
        """Serialise observations to a CSV string."""
        buf = io.StringIO()
        writer = csv.DictWriter(
            buf, fieldnames=["ra", "dec", "timestamp", "magnitude", "notes"]
        )
        writer.writeheader()
        for obs in observations:
            # TODO: escape newlines inside the 'notes' field before writing
            writer.writerow({
                "ra": obs.ra,
                "dec": obs.dec,
                "timestamp": obs.timestamp,
                "magnitude": obs.magnitude if obs.magnitude is not None else "",
                "notes": obs.notes,
            })
        return buf.getvalue()

    # ------------------------------------------------------------------
    # JSON
    # ------------------------------------------------------------------

    @staticmethod
    def to_json(observations: List[Observation], indent: int = 2) -> str:
        """Serialise observations to a JSON string."""
        # TODO: honour a user-supplied datetime format for the timestamp field
        records = [
            {
                "ra": obs.ra,
                "dec": obs.dec,
                "timestamp": obs.timestamp,
                "magnitude": obs.magnitude,
                "notes": obs.notes,
            }
            for obs in observations
        ]
        return json.dumps(records, indent=indent)

    # ------------------------------------------------------------------
    # Plain text
    # ------------------------------------------------------------------

    @staticmethod
    def to_text(observations: List[Observation]) -> str:
        """Human-readable plain-text summary."""
        # TODO: add a configurable column-width parameter for terminal output
        lines = []
        for i, obs in enumerate(observations, start=1):
            mag = f"{obs.magnitude:.2f}" if obs.magnitude is not None else "n/a"
            lines.append(
                f"{i:4d}.  RA={obs.ra:.4f}°  Dec={obs.dec:.4f}°  "
                f"mag={mag}  ts={obs.timestamp:.0f}"
            )
        return "
".join(lines)
