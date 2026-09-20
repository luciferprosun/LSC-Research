# Data Exposure Assessment

This assessment classifies provenance, not physical quality. It does not accuse the project of tuning without evidence.

## Reference boundary

The canonical 6.3.0 freeze is dated 2026-05-25. It is:

- `POST_DATA` relative to published BEST, GALLEX/GNO, and SAGE values already used or discussed in the historical archive;
- `PRE_DATA` relative to a future BEST-2 result, as expressly intended by the release;
- not proven pre-data for other previously public constraints merely because it is called “frozen”.

The registry uses `POST_DATA` for canonical documents because the Step 01 recovery gate asks whether existing validation datasets could have informed the object. Notes preserve the narrower pre-BEST-2 meaning.

| Candidate | Evidence of exposure | Classification | Exposure decision |
|---|---|---|---|
| Canonical E1-E12 and parameter structures | Published 2026-05-25 after BEST; release explicitly targets future BEST-2 | `AUTHENTIC_FROZEN` documentation | `POST_DATA` overall; pre-BEST-2 only |
| Toy M5/M6 `c0/c1` | Generator loads observed BEST/GALLEX/SAGE ratios and fits coefficients | `HISTORICAL_POST_DATA` | `POST_DATA` |
| LSC 6.2.1 five-anchor coefficients | README and source identify BEST/GALLEX/SAGE anchors; code calls `numpy.linalg.lstsq` | `HISTORICAL_POST_DATA` | `POST_DATA` |
| LSC 5.5 tensor/alpha objects | Optimized output contains BEST/GALLEX targets and fitted `alpha_optimal` | `HISTORICAL_POST_DATA` | `POST_DATA` |
| LSC 6.0 toy scenarios | Source contains `TARGET_R_BEST=0.79` and selected scenarios | `HISTORICAL_POST_DATA` | `POST_DATA` |
| LSC 6.2 `delta≈0.05` | Source explicitly labels it representative, illustrative, and not a measurement | `HISTORICAL_POST_DATA` | `POST_DATA`, not necessarily fitted |
| Deprecated 4.x PBH configuration | Native Git only proves import by 2026-05-23; artifact is semantically obsolete | `HISTORICAL_POST_DATA` | `POST_DATA` relative to BEST based on documented 2026 lineage; original pre-Git timing otherwise unverified |
| Complete 6.3.0 numeric vector | No candidate exists | `MISSING` | `UNKNOWN_EXPOSURE` |

## Consequence

No recovered numerical candidate qualifies as a pre-BEST frozen prediction. The authentic freeze is primarily a symbolic and methodological boundary. A future blind BEST-2 prediction would require a separately adjudicated complete object before viewing BEST-2 outcomes.
