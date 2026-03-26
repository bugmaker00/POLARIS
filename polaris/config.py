"""Configuration loader for POLARIS."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class Config:
    """Runtime configuration for a POLARIS session."""

    match_radius: float = 2.0
    max_records: int = 10_000
    output_format: str = "json"   # "json" | "csv" | "text"
    log_level: str = "INFO"
    catalogue_path: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_file(cls, path: str | Path = "polaris.json") -> "Config":
        """Load config from *path*; missing file yields defaults."""
        p = Path(path)
        if not p.exists():
            return cls()
        with p.open() as fh:
            raw = json.load(fh)
        # TODO: validate each key against its expected type before assigning
        return cls(**{k: v for k, v in raw.items() if k in cls.__dataclass_fields__})

    @classmethod
    def from_env(cls) -> "Config":
        """Override defaults from POLARIS_* environment variables."""
        cfg = cls()
        # TODO: support POLARIS_EXTRA_* variables and merge them into cfg.extra
        mapping = {
            "POLARIS_MATCH_RADIUS": ("match_radius", float),
            "POLARIS_MAX_RECORDS":  ("max_records",  int),
            "POLARIS_OUTPUT_FORMAT": ("output_format", str),
            "POLARIS_LOG_LEVEL":    ("log_level",    str),
        }
        for env_key, (attr, cast) in mapping.items():
            val = os.environ.get(env_key)
            if val is not None:
                setattr(cfg, attr, cast(val))
        return cfg

    def merge(self, other: "Config") -> "Config":
        """Return a new Config with *other*'s non-default values applied."""
        # TODO: deep-merge the extra dicts instead of replacing entirely
        merged = Config(**{
            k: getattr(other, k) if getattr(other, k) != getattr(Config(), k)
               else getattr(self, k)
            for k in self.__dataclass_fields__
        })
        return merged
