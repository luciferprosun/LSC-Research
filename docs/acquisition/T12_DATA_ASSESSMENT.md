# T12 Data Assessment

## Verdict

**BLOCKED_DIRECTIONAL_DATA_INSUFFICIENT**

Every required T12 gate must pass. The current archive does not meet that condition.

## Prerequisite status

| Prerequisite | Status | Evidence |
|---|---|---|
| Exact event/sub-run UTC timing | MISSING | Radiochemical measurements provide multi-day exposure intervals, not event-resolved capture times |
| Sufficient sidereal time resolution | MISSING | Exposure averaging suppresses daily structure and cannot be inverted |
| Surveyed detector orientation | MISSING | No authoritative Earth-fixed axes/azimuth/elevation located |
| Surveyed source orientation | MISSING | Source placement descriptions do not establish the required tensor orientation |
| Earth-fixed machine-readable geometry | MISSING | Dimensions/averages are not a surveyed directional model |
| Complete active 6.3.0 tensor | MISSING | Only symbolic A_a^{ij}; historical 5.5 D is inadmissible |
| Frame transformations | MISSING | No complete model-to-detector-to-Earth transform |
| Required units | MISSING | Frozen unit contract is incomplete |
| Frozen T12 statistic/power rule | SPECIFICATION_INCOMPLETE | Historical source does not define an executable PASS/FAIL statistic |

## Timing consequences

BEST exposes each target over approximately multi-day intervals. SAGE and GALLEX are also radiochemical integrations. Exposure start/end information can support scalar integration bookkeeping but cannot substitute for capture-event timestamps. An exposure midpoint is explicitly forbidden as an event-time fallback.

No sidereal modulation was calculated. No timing, orientation, tensor, unit, or frame value was reconstructed. T12 remains blocked even if the scalar frozen bundle is later recovered.
