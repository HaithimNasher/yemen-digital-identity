# YDII National Observatory Dashboard

The dashboard aggregates project state from existing YDII datasets.

It does not create new authoritative facts.

## Inputs

- GCC benchmark
- Yemen namespace model
- national entity directory
- registry / registrar architecture
- eligibility engine
- policy center
- live observatory snapshot
- domain-search sample

## Separation of concerns

The dashboard must keep these distinct:

1. **Architecture status**
2. **Static directory data**
3. **Policy state**
4. **Live technical observations**
5. **Search/availability observations**

## Important limitations

- `NOT_FOUND_IN_RDAP` is not equivalent to domain availability.
- live scan results are time-specific.
- proposed zones are not operational zones.
- screenshot references are not live ownership evidence.
- the dashboard is not an official `.ye` registry dashboard.
