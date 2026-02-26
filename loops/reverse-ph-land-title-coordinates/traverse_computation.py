#!/usr/bin/env python3
"""
Precise traverse computation for Philippine land title technical descriptions.
Uses math module for full IEEE 754 double precision.
"""

import math

def dms_to_decimal(degrees, minutes, seconds=0.0):
    """Convert degrees, minutes, seconds to decimal degrees."""
    return degrees + minutes / 60.0 + seconds / 3600.0

def bearing_to_azimuth(ns, degrees, minutes, seconds, ew):
    """
    Convert Philippine-style bearing to azimuth (degrees from North, clockwise).
    ns: 'N' or 'S'
    ew: 'E' or 'W'
    Returns azimuth in decimal degrees.
    """
    beta = dms_to_decimal(degrees, minutes, seconds)
    if ns == 'N' and ew == 'E':
        return beta
    elif ns == 'S' and ew == 'E':
        return 180.0 - beta
    elif ns == 'S' and ew == 'W':
        return 180.0 + beta
    elif ns == 'N' and ew == 'W':
        return 360.0 - beta
    else:
        raise ValueError(f"Invalid bearing: {ns} {degrees}°{minutes}' {ew}")

def compute_delta(azimuth_deg, distance):
    """Compute dN, dE from azimuth (degrees) and distance (meters)."""
    az_rad = math.radians(azimuth_deg)
    dN = distance * math.cos(az_rad)
    dE = distance * math.sin(az_rad)
    return dN, dE

def compute_traverse(name, bllm_n, bllm_e, tie_line, legs, stated_area, num_corners):
    """
    Compute full traverse.
    tie_line: (ns, deg, min, sec, ew, distance) for BLLM -> Corner 1
    legs: list of (ns, deg, min, sec, ew, distance) for Corner i -> Corner i+1
          Last leg should close back to Corner 1.
    """
    print("=" * 80)
    print(f"  {name}")
    print("=" * 80)

    # --- Tie Line ---
    tie_ns, tie_deg, tie_min, tie_sec, tie_ew, tie_dist = tie_line
    tie_az = bearing_to_azimuth(tie_ns, tie_deg, tie_min, tie_sec, tie_ew)
    tie_dN, tie_dE = compute_delta(tie_az, tie_dist)

    print(f"\n--- Tie Line: BLLM -> Corner 1 ---")
    print(f"  BLLM coordinates: N = {bllm_n:.6f}, E = {bllm_e:.6f}")
    print(f"  Bearing: {tie_ns} {tie_deg}°{tie_min:02d}'{tie_sec:04.1f}\" {tie_ew}")
    print(f"  Azimuth: {tie_az:.15f}°")
    print(f"  Distance: {tie_dist:.6f} m")
    print(f"  dN = {tie_dN:.15f} m")
    print(f"  dE = {tie_dE:.15f} m")

    corner1_n = bllm_n + tie_dN
    corner1_e = bllm_e + tie_dE
    print(f"  Corner 1: N = {corner1_n:.15f}, E = {corner1_e:.15f}")

    # --- Compute all legs ---
    print(f"\n--- Leg Computations ---")
    print(f"{'Leg':<12} {'Bearing':<22} {'Azimuth (°)':<22} {'Dist (m)':<14} {'dN (m)':<22} {'dE (m)':<22}")
    print("-" * 114)

    corners_n = [corner1_n]
    corners_e = [corner1_e]

    total_dN = 0.0
    total_dE = 0.0
    perimeter = 0.0

    for i, leg in enumerate(legs):
        ns, deg, mn, sec, ew, dist = leg

        # Special case: Due North
        if ns == 'DUE' and ew == 'N':
            az = 0.0
            bearing_str = "Due North"
        else:
            az = bearing_to_azimuth(ns, deg, mn, sec, ew)
            bearing_str = f"{ns} {deg}°{mn:02d}'{sec:04.1f}\" {ew}"

        dN, dE = compute_delta(az, dist)
        total_dN += dN
        total_dE += dE
        perimeter += dist

        from_pt = i + 1
        to_pt = i + 2 if i < len(legs) - 1 else 1
        leg_label = f"{from_pt}->{to_pt}"

        print(f"{leg_label:<12} {bearing_str:<22} {az:<22.15f} {dist:<14.6f} {dN:<22.15f} {dE:<22.15f}")

        next_n = corners_n[-1] + dN
        next_e = corners_e[-1] + dE

        # Don't append the closing point (it should be corner 1 again)
        if i < len(legs) - 1:
            corners_n.append(next_n)
            corners_e.append(next_e)
        else:
            closing_n = next_n
            closing_e = next_e

    n = len(corners_n)  # number of corners

    # --- Corner Coordinates ---
    print(f"\n--- Corner Coordinates (Unadjusted) ---")
    print(f"{'Corner':<10} {'Northing (m)':<30} {'Easting (m)':<30}")
    print("-" * 70)
    for i in range(n):
        print(f"{i+1:<10} {corners_n[i]:<30.15f} {corners_e[i]:<30.15f}")

    print(f"\n  Closing point (should equal Corner 1):")
    print(f"  N = {closing_n:.15f}, E = {closing_e:.15f}")

    # --- Closure Error ---
    eN = closing_n - corner1_n  # = total_dN
    eE = closing_e - corner1_e  # = total_dE
    e_linear = math.sqrt(eN**2 + eE**2)

    if e_linear > 0:
        precision_k = perimeter / e_linear
    else:
        precision_k = float('inf')

    print(f"\n--- Closure Error ---")
    print(f"  Sum dN (eN) = {eN:.15f} m")
    print(f"  Sum dE (eE) = {eE:.15f} m")
    print(f"  Also:  total_dN = {total_dN:.15f} m")
    print(f"  Also:  total_dE = {total_dE:.15f} m")
    print(f"  Linear error (e) = {e_linear:.15f} m")
    print(f"  Perimeter (P)    = {perimeter:.15f} m")
    print(f"  Precision ratio  = 1:{precision_k:.6f}")
    print(f"  Precision ratio  ~ 1:{round(precision_k)}")

    # --- Shoelace Area ---
    # Shift coordinates: subtract N_min and E_min
    n_min = min(corners_n)
    e_min = min(corners_e)

    n_adj = [c - n_min for c in corners_n]
    e_adj = [c - e_min for c in corners_e]

    print(f"\n--- Shifted Coordinates for Shoelace ---")
    print(f"  N_min = {n_min:.15f}")
    print(f"  E_min = {e_min:.15f}")
    print(f"{'Corner':<10} {'n_adj (m)':<30} {'e_adj (m)':<30}")
    print("-" * 70)
    for i in range(n):
        print(f"{i+1:<10} {n_adj[i]:<30.15f} {e_adj[i]:<30.15f}")

    two_A = 0.0
    for i in range(n):
        j = (i + 1) % n
        cross = e_adj[i] * n_adj[j] - e_adj[j] * n_adj[i]
        two_A += cross
        print(f"  i={i+1}, j={j+1}: e_adj[{i+1}]*n_adj[{j+1}] - e_adj[{j+1}]*n_adj[{i+1}] = "
              f"{e_adj[i]:.15f} * {n_adj[j]:.15f} - {e_adj[j]:.15f} * {n_adj[i]:.15f} = {cross:.15f}")

    area = abs(two_A) / 2.0

    pct_diff = ((area - stated_area) / stated_area) * 100.0

    print(f"\n--- Area ---")
    print(f"  2A (signed)    = {two_A:.15f}")
    print(f"  Computed area  = {area:.15f} sq m")
    print(f"  Stated area    = {stated_area:.6f} sq m")
    print(f"  Difference     = {area - stated_area:.15f} sq m")
    print(f"  % difference   = {pct_diff:.10f} %")
    print()

    return corners_n, corners_e, area


# =============================================================================
# SAMPLE 3: Lot 2, Mr-1018-D, Malabon, Rizal (1950, Luzon 1911)
# =============================================================================

# BLLM coordinates (Luzon 1911 PTM Zone 3)
bllm3_n = 1620500.000
bllm3_e = 501200.000

# Tie line: S. 44°36' W., 90.02 m from BLLM 1
tie3 = ('S', 44, 36, 0.0, 'W', 90.02)

# Legs (7 corners, 7 legs including closing leg)
legs3 = [
    ('N', 68, 44, 0.0, 'E', 5.81),     # 1->2
    ('S', 23, 11, 0.0, 'E', 32.85),     # 2->3
    ('S', 23, 11, 0.0, 'E', 47.00),     # 3->4
    ('S', 23, 34, 0.0, 'E', 15.33),     # 4->5
    ('S', 22, 59, 0.0, 'E', 17.24),     # 5->6
    ('S', 61, 37, 0.0, 'W', 5.99),      # 6->7
    ('N', 23,  8, 0.0, 'W', 113.14),    # 7->1 (closing)
]

compute_traverse(
    name="Sample 3: Lot 2, Mr-1018-D, Malabon, Rizal (1950, Luzon 1911)",
    bllm_n=bllm3_n,
    bllm_e=bllm3_e,
    tie_line=tie3,
    legs=legs3,
    stated_area=664.0,
    num_corners=7
)


# =============================================================================
# SAMPLE 5: Lot 1, Psu-(af)-02-001767, Peñablanca, Cagayan (2011, PRS92)
# =============================================================================

# BLLM coordinates (PRS92 Zone 3)
bllm5_n = 1990000.000
bllm5_e = 480000.000

# Tie line: N. 11°05' W., 4,317.52 m from BLLM 1
tie5 = ('N', 11, 5, 0.0, 'W', 4317.52)

# Legs (11 corners, 11 legs including closing leg)
legs5 = [
    ('S', 36, 43, 0.0, 'E', 98.73),      # 1->2
    ('S', 83, 12, 0.0, 'E', 519.94),      # 2->3
    ('S', 83, 16, 0.0, 'E', 196.00),      # 3->4
    ('S',  0,  6, 0.0, 'W', 5.55),        # 4->5
    ('N', 83,  4, 0.0, 'W', 247.07),      # 5->6
    ('N', 83,  4, 0.0, 'W', 236.00),      # 6->7
    ('N', 83,  4, 0.0, 'W', 239.99),      # 7->8
    ('N', 35, 56, 0.0, 'W', 94.00),       # 8->9
    ('N', 80, 13, 0.0, 'W', 180.26),      # 9->10
    ('DUE', 0, 0, 0.0, 'N', 5.64),        # 10->11: Due North
    ('S', 80, 27, 0.0, 'E', 183.16),      # 11->1 (closing)
]

compute_traverse(
    name="Sample 5: Lot 1, Psu-(af)-02-001767, Peñablanca, Cagayan (2011, PRS92)",
    bllm_n=bllm5_n,
    bllm_e=bllm5_e,
    tie_line=tie5,
    legs=legs5,
    stated_area=4926.0,
    num_corners=11
)
