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
<!-- last refreshed: initial scaffold (stale placeholder) -->

- `polaris/core.py` — add coordinate validation
- `polaris/tracker.py` — load catalogue from CSV
- `polaris/formatter.py` — honour datetime format

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
