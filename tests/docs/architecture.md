# Footprint Flux Architecture

## High-Level Architecture

```text
                  ┌─────────────────────┐
                  │   Public Sources    │
                  │                     │
                  │ APIs / Websites     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Collectors      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Normalizer      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Snapshot Engine    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │      Database       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Change Detection   │
                  └──────────┬──────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌─────────────────┐    ┌─────────────────┐
        │   Risk Engine   │    │ Timeline Engine │
        └────────┬────────┘    └────────┬────────┘
                 │                       │
                 └───────────┬───────────┘
                             ▼
                  ┌─────────────────────┐
                  │     Dashboard      │
                  └─────────────────────┘
```

## Main Components

### Collectors

Responsible for retrieving authorized publicly available information from supported sources.

### Normalizer

Converts source-specific data into a common internal representation.

### Snapshot Engine

Creates timestamped representations of a digital footprint.

### Database

Stores people, sources, observations, snapshots, changes, and risk assessments.

### Change Detection

Compares snapshots to identify:

* Added information
* Removed information
* Modified information
* Unchanged information

### Risk Engine

Analyzes observations and changes for documented privacy-risk indicators.

### Timeline Engine

Builds a chronological representation of how the footprint evolved.

### Dashboard

Provides a visual interface for exploring the footprint, historical changes, and risk analysis.
