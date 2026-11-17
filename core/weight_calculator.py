"""Steel weight engine. Pure Python, no UI, no database.

All dimensions are in millimetres, length in metres, result in kg.
Density of steel = 7850 kg/m3.
"""
import math

DENSITY = 7850  # kg per cubic metre
MM3_TO_M3 = 1e-9


def _check(**values):
    for name, v in values.items():
        if v is None or v <= 0:
            raise ValueError(f"{name} must be greater than 0")


def plate_weight(length_mm, width_mm, thickness_mm, qty=1):
    _check(length_mm=length_mm, width_mm=width_mm, thickness_mm=thickness_mm, qty=qty)
    return length_mm * width_mm * thickness_mm * MM3_TO_M3 * DENSITY * qty


def round_bar_weight(diameter_mm, length_m, qty=1):
    """Also used for rebar."""
    _check(diameter_mm=diameter_mm, length_m=length_m, qty=qty)
    area_mm2 = math.pi * diameter_mm ** 2 / 4
    return area_mm2 * 1e-6 * length_m * DENSITY * qty


def square_bar_weight(side_mm, length_m, qty=1):
    _check(side_mm=side_mm, length_m=length_m, qty=qty)
    return side_mm ** 2 * 1e-6 * length_m * DENSITY * qty


def flat_bar_weight(width_mm, thickness_mm, length_m, qty=1):
    _check(width_mm=width_mm, thickness_mm=thickness_mm, length_m=length_m, qty=qty)
    return width_mm * thickness_mm * 1e-6 * length_m * DENSITY * qty


def pipe_weight(outer_diameter_mm, wall_thickness_mm, length_m, qty=1):
    _check(outer_diameter_mm=outer_diameter_mm, wall_thickness_mm=wall_thickness_mm,
           length_m=length_m, qty=qty)
    if wall_thickness_mm * 2 >= outer_diameter_mm:
        raise ValueError("wall thickness too large for this diameter")
    area_mm2 = math.pi * (outer_diameter_mm - wall_thickness_mm) * wall_thickness_mm
    return area_mm2 * 1e-6 * length_m * DENSITY * qty


def angle_weight(leg1_mm, leg2_mm, thickness_mm, length_m, qty=1):
    """Angle bar (approximate, ignores corner radius)."""
    _check(leg1_mm=leg1_mm, leg2_mm=leg2_mm, thickness_mm=thickness_mm,
           length_m=length_m, qty=qty)
    area_mm2 = thickness_mm * (leg1_mm + leg2_mm - thickness_mm)
    return area_mm2 * 1e-6 * length_m * DENSITY * qty


def beam_weight(kg_per_metre, length_m, qty=1):
    """Beams/channels: use the kg/m from the section table."""
    _check(kg_per_metre=kg_per_metre, length_m=length_m, qty=qty)
    return kg_per_metre * length_m * qty


def calculate(steel_type, **dims):
    """Single entry point for the UI: calculate('pipe', outer_diameter_mm=48, ...)."""
    funcs = {
        "plate": plate_weight,
        "round_bar": round_bar_weight,
        "rebar": round_bar_weight,
        "square_bar": square_bar_weight,
        "flat_bar": flat_bar_weight,
        "pipe": pipe_weight,
        "angle": angle_weight,
        "beam": beam_weight,
    }
    if steel_type not in funcs:
        raise ValueError(f"Unknown steel type: {steel_type}")
    return round(funcs[steel_type](**dims), 3)
