import pytest
from core.weight_calculator import calculate


def test_plate():
    # 2440 x 1220 x 10 mm = 233.7 kg
    assert calculate("plate", length_mm=2440, width_mm=1220, thickness_mm=10) == pytest.approx(233.68, abs=0.1)


def test_rebar_12mm_12m():
    # 12 mm bar is about 0.888 kg/m -> 10.66 kg per 12 m
    assert calculate("rebar", diameter_mm=12, length_m=12) == pytest.approx(10.66, abs=0.05)


def test_pipe():
    # 48.3 OD x 3.2 wall is about 3.56 kg/m
    assert calculate("pipe", outer_diameter_mm=48.3, wall_thickness_mm=3.2, length_m=1) == pytest.approx(3.56, abs=0.05)


def test_quantity_multiplies():
    one = calculate("square_bar", side_mm=20, length_m=6)
    five = calculate("square_bar", side_mm=20, length_m=6, qty=5)
    assert five == pytest.approx(one * 5, abs=0.01)


def test_invalid_input():
    with pytest.raises(ValueError):
        calculate("plate", length_mm=0, width_mm=10, thickness_mm=5)
    with pytest.raises(ValueError):
        calculate("magic_steel", length_mm=1)
