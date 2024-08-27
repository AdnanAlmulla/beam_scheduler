"""Edgecases: Test instance where provided reinforcement cannot be met."""

import pytest
from pytest import approx

import SRC.beam
import SRC.beam_design


@pytest.fixture
def example_beam() -> SRC.beam.Beam:
    """Example beam utilised for testing purposes.

    Currently mimicking beam B548 at L24.

    Returns:
        object: Example beam to utilise in tests.
    """
    example_beam = SRC.beam.Beam(
        storey="L24 (Sky Garden)",
        etabs_id="B548",
        width=700,  # mm
        depth=1550,  # mm
        span=5890,  # mm
        comp_conc_grade=45,  # MPa
        flex_overstressed=[False, False],  # pos, neg
        req_top_flex_reinf=[14712, 6140, 3638],  # left, middle, right
        req_bot_flex_reinf=[4584, 5415, 10007],  # left, middle, right
        req_torsion_flex_reinf=[6096, 6096, 6096],  # left, middle, right
        shear_force=[3195, 3169, 1997],  # left, middle, right
        shear_overstressed=[False, False],  # shear, torsion
        req_shear_reinf=[5026, 4971, 2434],  # left, middle, right
        req_torsion_reinf=[800, 437, 458],  # left, middle, right
    )
    return example_beam


@pytest.fixture
def designed_beam(example_beam: SRC.beam.Beam) -> SRC.beam_design.BeamDesign:
    """Example designed beam object utilised for testing purposes.

    Args:
        example_beam (SRC.beam.Beam): Mimicking beam B46 at roof level.

    Returns:
        SRC.beam_design.BeamDesign: Example designed beam to utilise in tests.
    """
    designed_beam = SRC.beam_design.BeamDesign(example_beam)
    designed_beam.calculate_flexural_design()
    designed_beam.calculate_shear_design()
    designed_beam.calculate_sideface_design()
    return designed_beam


@pytest.fixture
def beam_quantities(
    designed_beam: SRC.beam_design.BeamDesign,
) -> SRC.beam_design.BeamQuantities:
    """Example quantities from a designed beam object utilised for testing.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Quantities of designed beam.

    Returns:
        SRC.beam_design.BeamQuantities: Example quantities to utilise in tests.
    """
    beam_quantities = SRC.beam_design.BeamQuantities(designed_beam)
    return beam_quantities


def _assert_shear_link(
    section: dict,
    expected_text: str,
    expected_reinf: float,
    expected_utilization: float | str,
    expected_diameter: int,
    expected_spacing: int,
) -> None:
    assert section["links_text"] == expected_text
    assert section["provided_reinf"] == approx(expected_reinf)
    assert section["utilization"] == expected_utilization
    assert section["diameter"] == expected_diameter
    assert section["spacing"] == expected_spacing


def _assert_flex_rebar(
    section: dict,
    expected_text: str,
    expected_reinf: float,
    expected_utilization: float | str,
    expected_diameter: list[int] | list[float],
) -> None:
    assert section["rebar_text"] == expected_text
    assert section["provided_reinf"] == approx(expected_reinf)
    assert section["utilization"] == expected_utilization
    assert section["diameter"] == expected_diameter


def test_concrete_area(beam_quantities: SRC.beam_design.BeamQuantities) -> None:
    """Check if the concrete area is as expected.

    Args:
        beam_quantities (SRC.beam_design.BeamQuantities): Refer to example.
    """
    assert beam_quantities.conc_area == 1.085  # m^2


def test_concrete_volume(
    beam_quantities: SRC.beam_design.BeamQuantities,
) -> None:
    """Check if the concrete volume is as expected.

    Args:
        beam_quantities (SRC.beam_design.BeamQuantities): Refer to example.
    """
    assert beam_quantities.conc_volume == 6.391  # m^3


def test_get_long_count(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check if the get long count method obtains the correct value.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.flexural_design.flex_rebar_count == 6


def test_get_flex_req(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check if the correct flexural reinforcement values are obtained.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.beam.req_top_flex_reinf == [14712, 6140, 3638]
    assert designed_beam.beam.req_bot_flex_reinf == [4584, 5415, 10007]
    assert designed_beam.beam.req_torsion_flex_reinf == [6096, 6096, 6096]


def test_top_left_flex_rebar(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected top left flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.top_flex_rebar["left"],
        "Required rebar exceeds two layers. Please assess.",
        0,
        "-",
        [float("inf")],
    )


def test_top_middle_flex_rebar(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the expected top middle flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.top_flex_rebar["middle"],
        "6T32 + 6T20",
        6710,
        91.5,
        [32, 20],
    )


def test_top_right_flex_rebar(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the expected top right flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.top_flex_rebar["right"],
        "6T32 + 6T20",
        6710,
        54.2,
        [32, 20],
    )


def test_bot_left_flex_rebar(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected top left flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.bot_flex_rebar["left"],
        "6T25 + 6T25",
        5890,
        77.8,
        [25, 25],
    )


def test_bot_middle_flex_rebar(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the expected top middle flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.bot_flex_rebar["middle"],
        "6T25 + 6T25",
        5890,
        91.9,
        [25, 25],
    )


def test_bot_right_flex_rebar(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the expected top right flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.bot_flex_rebar["right"],
        "Required rebar exceeds two layers. Please assess.",
        0,
        "-",
        [float("inf")],
    )


def test_flex_area(beam_quantities: SRC.beam_design.BeamQuantities) -> None:
    """Check that the sum of all provided flexural rebar area is correct.

    Args:
        beam_quantities (SRC.beam_design.beam_quantities): Refer to example.
    """
    assert beam_quantities.flex_area == 0.025  # m^2


def test_flex_volume(beam_quantities: SRC.beam_design.BeamQuantities) -> None:
    """Check that the sum of all provided flexural rebar volume is correct.

    Args:
        beam_quantities (SRC.beam_design.beam_quantities): Refer to example.
    """
    assert beam_quantities.flex_volume == 0.147  # m^3


def test_residual_rebar(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """This test checks that the residual rebar value is correctly obtained.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.flexural_design.residual_rebar["left"] == approx(0)
    assert designed_beam.flexural_design.residual_rebar["middle"] == approx(0)
    assert designed_beam.flexural_design.residual_rebar["right"] == approx(0)


def test_total_shear_req(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the total shear requirement is correctly calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.shear_design.total_req_shear == [6626, 5845, 3350]


def test_shear_legs(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the correct number of shear legs are calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.shear_design.shear_links_count == [2, 3, 4]


def test_min_shear_long_spacing(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the expected codal spacing is calculated correctly.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.shear_design.shear_spacing == [250, 200, 150, 125, 100]
    assert designed_beam.shear_design.shear_center_spacing == [
        250,
        200,
        150,
        125,
        100,
    ]


def test_left_shear_links(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected left shear links are calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_shear_link(
        designed_beam.shear_design.shear_links["left"],
        "-",
        0,
        "-",
        0,
        0,
    )


def test_middle_shear_links(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected middle shear links are calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_shear_link(
        designed_beam.shear_design.shear_links["middle"],
        "-",
        0,
        "-",
        0,
        0,
    )


def test_right_shear_links(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected right shear links are calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_shear_link(
        designed_beam.shear_design.shear_links["right"],
        "-",
        0,
        "-",
        0,
        0,
    )


def test_shear_area(beam_quantities: SRC.beam_design.BeamQuantities) -> None:
    """Check if the shear area is as expected.

    Args:
        beam_quantities (SRC.beam_design.BeamQuantities): Refer to example.
    """
    assert beam_quantities.shear_area == 0


def test_shear_volume(beam_quantities: SRC.beam_design.BeamQuantities) -> None:
    """Check if the shear volume is as expected.

    Args:
        beam_quantities (SRC.beam_design.BeamQuantities): Refer to example.
    """
    assert beam_quantities.shear_volume == 0


def test_required_sideface_reinforcement(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the correct sideface area requirement is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert (
        designed_beam.sideface_design.required_torsion_reinforcement["left"]
        == 0
    )
    assert (
        designed_beam.sideface_design.required_torsion_reinforcement["middle"]
        == 0
    )
    assert (
        designed_beam.sideface_design.required_torsion_reinforcement["right"]
        == 0
    )
    assert (
        designed_beam.sideface_design.total_required_torsion_reinforcement == 0
    )


def test_sideface_clear_space(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the correct sideface clearspace is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.sideface_design.sideface_clearspace == approx(0)


def test_sideface_string(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the correct sideface rebar is obtained.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.sideface_design.sideface_rebar["rebar_text"] == "-"
    assert designed_beam.sideface_design.sideface_rebar["provided_reinf"] == 0
    assert designed_beam.sideface_design.sideface_rebar["utilization"] == "-"
    assert designed_beam.sideface_design.sideface_rebar["diameter"] == 0
    assert designed_beam.sideface_design.sideface_rebar["spacing"] == 0


def test_sideface_volume(
    beam_quantities: SRC.beam_design.BeamQuantities,
) -> None:
    """Check that the sideface volume is as expected.

    Args:
        beam_quantities (SRC.beam_design.BeamQuantities): Refer to example.
    """
    assert beam_quantities.sideface_volume == 0  # m^3


def test_total_area(beam_quantities: SRC.beam_design.BeamQuantities) -> None:
    """Check that the total rebar area is as expected.

    Args:
        beam_quantities (SRC.beam_design.BeamQuantities): Refer to example.
    """
    assert beam_quantities.total_rebar_area == 0.025  # m^2


def test_total_volume(beam_quantities: SRC.beam_design.BeamQuantities) -> None:
    """Check that the total rebar volume is as expected.

    Args:
        beam_quantities (SRC.beam_design.BeamQuantities): Refer to example.
    """
    assert beam_quantities.total_rebar_volume == 0.147  # m^3
