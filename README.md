# POLARIS

**Passive Observation & Location Analysis Runtime Inference System**

POLARIS is a lightweight Python library for recording, matching, and exporting
astronomical observations.  It provides a high-level `Observer` that collects
`Observation` records, a `StarTracker` that matches observations against a
built-in star catalogue, and pluggable `Formatter` classes for CSV, JSON, and
plain-text output.

---

## Features

| Feature | Status |
|---|---|
| Celestial coordinate recording | ✅ stable |
| Angular separation calculation | ✅ stable |
| Catalogue-based star identification | ✅ stable |
| CSV / JSON / plain-text export | ✅ stable |
| Config from file + env vars | ✅ stable |
| External catalogue loading | 🔜 planned |
| SQLite persistence | 🔜 planned |
| k-d tree spatial index | 🔜 planned |

---

## Installation

```bash
pip install polaris-obs   # once published to PyPI
```

Or for local development:

```bash
git clone https://github.com/bugmaker00/POLARIS
cd POLARIS
pip install -e .
```

---

## Quick Start

```python
from polaris import Observer, Observation, StarTracker

observer = Observer("my-session")
tracker  = StarTracker()

# Record a raw observation
obs = Observation(ra=37.95, dec=89.26, magnitude=1.97)
observer.record(obs)

# Match against the built-in catalogue
name = tracker.identify(obs)
print(name)   # → "Polaris"
```

---

## Project Layout

```
polaris/
├── __init__.py     – public API
├── core.py         – Observer + Observation primitives
├── tracker.py      – StarTracker catalogue matching
├── formatter.py    – CSV / JSON / text export
└── config.py       – Config loader (file + env vars)
tests/
└── test_core.py    – pytest suite
```

---

### 📝 Pending TODOs

<!-- auto-generated – do not edit manually -->
<!-- last refreshed: 2026-03-26 | 17 items -->

- `polaris/core.py:22` — validate that ra is within [0, 360) and dec within [-90, 90]
- `polaris/core.py:27` — switch to the Vincenty formula for antipodal-safe calculation
- `polaris/core.py:43` — persist each record to SQLite for crash-safe storage
- `polaris/core.py:50` — build a k-d tree index once the record count exceeds 1000
- `polaris/core.py:54` — include min/max/mean magnitude in the summary when available
- `polaris/tracker.py:26` — load catalogue from an external CSV file instead of hard-coding it
- `polaris/tracker.py:31` — add a calibration offset (delta_ra, delta_dec) per session
- `polaris/tracker.py:46` — emit a WARNING log when no match is found within the radius
- `polaris/tracker.py:51` — parallelise with a thread pool for large batches (> 500 items)
- `polaris/formatter.py:29` — escape newlines inside the 'notes' field before writing
- `polaris/formatter.py:46` — honour a user-supplied datetime format for the timestamp field
- `polaris/formatter.py:66` — add a configurable column-width parameter for terminal output
- `polaris/config.py:35` — validate each key against its expected type before assigning
- `polaris/config.py:42` — support POLARIS_EXTRA_* variables and merge them into cfg.extra
- `polaris/config.py:57` — deep-merge the extra dicts instead of replacing entirely
- `tests/test_core.py:50` — assert magnitude stats once summary() includes them
- `tests/test_core.py:51` — assert observer name appears correctly in the output dict

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Contributing

1. Fork the repository and create a feature branch from `main`.
2. Add or update tests for every changed behaviour.
3. Open a pull request; CI must pass before merging.

---

## License

MIT © POLARIS Contributors
