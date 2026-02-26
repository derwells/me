# Traverse Computation References

Processed reference material for geodetic traverse computation. Sourced from standard surveying references and DENR regulations.

---

## 1. Bearing/Azimuth Conventions

### Bearing vs. Azimuth
- **Bearing**: quadrant-relative direction, e.g. "N 47°30'20" E", "S 12°15'00" W". Range: 0°–90° within each quadrant.
- **Azimuth**: angle measured clockwise from North, 0°–360°. More convenient for computation — signs of sin/cos are automatically correct.

### Bearing → Azimuth Conversion

| Bearing Quadrant | Azimuth |
|---|---|
| N β E | Az = β |
| S β E | Az = 180° − β |
| S β W | Az = 180° + β |
| N β W | Az = 360° − β |

### Azimuth → Bearing Conversion

| Azimuth Range | Bearing |
|---|---|
| 0° – 90° | N (Az) E |
| 90° – 180° | S (180°−Az) E |
| 180° – 270° | S (Az−180°) W |
| 270° – 360° | N (360°−Az) W |

---

## 2. Forward Computation: Polar → Rectangular

Convert a bearing and distance to a ΔNorthing / ΔEasting offset.

**Using azimuth (preferred for code — no sign lookup required):**

```
ΔN = distance × cos(azimuth_radians)
ΔE = distance × sin(azimuth_radians)
```

**Using bearing (requires quadrant sign table):**

| Bearing Quadrant | ΔN sign | ΔE sign |
|---|---|---|
| N _ E | + | + |
| S _ E | − | + |
| S _ W | − | − |
| N _ W | + | − |

**Source**: Jerrymahun Open Access Library (COGO Ch. A, Eqs. A-1, A-2); standard surveying references.

---

## 3. Cumulative Traverse (Corner-to-Corner)

Starting from a known corner (N₀, E₀) — typically Corner 1, derived from the tie point + tie line:

```
For i = 1 to n:
    ΔNᵢ = distᵢ × cos(azᵢ)
    ΔEᵢ = distᵢ × sin(azᵢ)
    Nᵢ = Nᵢ₋₁ + ΔNᵢ
    Eᵢ = Eᵢ₋₁ + ΔEᵢ
```

Last computed point (corner n) should equal corner 0 for a closed traverse.

---

## 4. Inverse Computation: Rectangular → Polar

Given two points (N_from, E_from) → (N_to, E_to):

```
ΔN = N_to − N_from
ΔE = E_to − E_from
distance = √(ΔN² + ΔE²)
β = arctan(|ΔE| / |ΔN|)   # acute angle (0°–90°)
```

Azimuth from quadrant (Table A-1 from Jerrymahun COGO):

| ΔN | ΔE | Azimuth |
|---|---|---|
| + | + | β |
| − | + | 180° − β |
| − | − | 180° + β |
| + | − | 360° − β |

---

## 5. Closure Error Computation

For a closed polygon traverse (returning to start):

```
Linear misclosure in N: eN = ΣΔN  (should be 0)
Linear misclosure in E: eE = ΣΔE  (should be 0)
Linear misclosure:      e  = √(eN² + eE²)
Perimeter (traverse length): P = Σdistᵢ
Relative precision:     1/k = e / P  (expressed as 1:k)
```

**Example**: e = 0.110 m, P = 1200 m → relative precision = 1:10,909 → rounds to 1:10,000 (acceptable for cadastral).

---

## 6. Polygon Area — Shoelace (Gauss) Formula

Given n corners with coordinates (N₁,E₁)...(Nₙ,Eₙ):

```
2A = |Σᵢ (Eᵢ × Nᵢ₊₁ − Eᵢ₊₁ × Nᵢ)|   (indices mod n)
A = |2A| / 2
```

Or equivalently (surveyor's form):

```
2A = Σᵢ Nᵢ × (Eᵢ₊₁ − Eᵢ₋₁)
```

**Units**: If N/E in meters, area is in square meters. Convert to hectares (÷ 10,000) or square meters as appropriate for comparison with the stated title area.

**Floating-point note**: Subtract centroid or minimum N/E from all coordinates before summing to avoid precision loss with large PRS92 grid values (~500,000 m scale).

**Source**: Wikipedia (Shoelace Formula); Wolfram MathWorld; John D. Cook (Surveyor's Formula).

---

## 7. Bowditch (Compass Rule) Adjustment

For distributing misclosure proportionally to course length:

```
For each course i with length Lᵢ:
    ΔNᵢ_corr = ΔNᵢ − eN × (Lᵢ / P)
    ΔEᵢ_corr = ΔEᵢ − eE × (Lᵢ / P)
```

After adjustment: ΣΔNᵢ_corr = 0, ΣΔEᵢ_corr = 0 (exactly).

Adjusted line length and bearing:
```
Lᵢ_adj   = √(ΔNᵢ_corr² + ΔEᵢ_corr²)
Az_adj    = atan2(ΔEᵢ_corr, ΔNᵢ_corr)   [convert to 0–360]
```

**Source**: Jerrymahun Open Access Library (Traverse Adjustments Ch. E, Eqs. E-1 to E-6).

**Note for Philippine land title engine**: Bowditch adjustment changes the bearing and distance of each leg. The title's printed bearings and distances are the *original (unadjusted)* survey values. The engine should compute with the *original* values and report the misclosure as a validation metric — not apply Bowditch to match the stated area. Bowditch is used during original survey, not during title parsing.

---

## 8. Angular Closure (if individual angles are available)

For a closed polygon with n sides:
```
Sum of interior angles = (n − 2) × 180°
Angular misclosure = Σ(measured interior angles) − (n−2)×180°
```

**Note**: Technical descriptions in Philippine titles give bearings, not interior angles. Angular closure of the polygon can be inferred by back-computing the angle at each corner from the published bearing sequence. This is a secondary validation check.

---

## 9. Philippine Survey Closure Tolerances

From DENR regulatory framework (DAO 2007-29, MC 2010-13):

| Survey Type | Allowable Relative Precision |
|---|---|
| Cadastral lot survey | 1:5,000 (urban areas) |
| Isolated lot survey (rural) | ~1:3,000 to 1:5,000 |
| Project control / geodetic | 1:10,000 or better |

**Note**: Exact values in Section 28.b of DAO 2007-29 and MC 2010-13 full text. The 1:5,000 figure for urban lots is confirmed by secondary sources (respicio.ph legal commentary on DAO 2010-13). DENR verification flags surveys that exceed these tolerances.

**Recommended engine thresholds** (conservative):
- Warn if relative precision worse than 1:3,000
- Error if relative precision worse than 1:1,000 (likely data entry problem)

---

## 10. Tie Line Traverse (BLLM → Corner 1)

The tie line is a single traverse leg from the BLLM to Corner 1 of the lot:

```
N_corner1 = N_BLLM + dist_tie × cos(az_tie)
E_corner1 = E_BLLM + dist_tie × sin(az_tie)
```

Where az_tie is derived from the tie line bearing (e.g., "N 45°30'20" E" → az = 45.5056°).

This is the foundation of the entire traverse. BLLM coordinate accuracy directly propagates to all lot corners.

---

## Sources

- Jerrymahun Open Access Surveying Library — COGO Chapter A (Coordinates): https://www.jerrymahun.com/index.php/home/open-access/12-iv-cogo/21-cogo-chap-a
- Jerrymahun Open Access Surveying Library — Traverse Adjustments Chapter E: https://jerrymahun.com/index.php/home/open-access/17-trav-comps/44-travcomps-chap-e
- Wikipedia — Shoelace Formula: https://en.wikipedia.org/wiki/Shoelace_formula
- John D. Cook — Surveyor's Formula for Polygon Area: https://www.johndcook.com/blog/2018/09/26/polygon-area/
- DENR AO 2010-17 (IVAS in PRS92): https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/10/52040
- DENR DAO 2007-29 — Revised Regulations on Land Surveys: https://legaldex.com/laws/revised-regulations-on-land-surveys
- ENR — Azimuth Trick for Traverse Calculations: https://www.enr.com/articles/53271-fundamentals-of-surveying-calculating-traverses-is-easier-using-the-azimuth-trick
- ESE Notes — Traverse Survey (Bowditch's Rule): https://esenotes.com/traverse-survey-latitude-and-departure-closing-error-relative-precision-bowditchs-rule-transit-rule/
