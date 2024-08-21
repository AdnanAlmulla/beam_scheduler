"""Edgecases: Span less than 6m, must copy reinforcement to all locations.

Also checks that torsion reinforcement is split to top and bottom reinf.
"""

import pytest
from pytest import approx

import SRC.beam
import SRC.beam_design


@pytest.fixture
def example_beam() -> SRC.beam.Beam:
    """Example beam utilised for testing purposes.

    Currently mimicking beam B46 at roof level.

    Returns:
        object: Example beam to utilise in tests.
    """
    example_beam = SRC.beam.Beam(
        storey="Roof",
        etabs_id="B46",
        width=400,  # mm
        depth=600,  # mm
        span=2650,  # mm
        comp_conc_grade=45,  # MPa
        flex_overstressed=[False, False],  # pos, neg
        req_top_flex_reinf=[365, 173, 195],  # left, middle, right
        req_bot_flex_reinf=[207, 247, 146],  # left, middle, right
        req_torsion_flex_reinf=[1343, 1343, 1343],  # left, middle, right
        shear_force=[30, 31, 36],  # left, middle, right
        shear_overstressed=[False, False],  # shear, torsion
        req_shear_reinf=[105, 107, 107],  # left, middle, right
        req_torsion_reinf=[792, 792, 761],  # left, middle, right
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


def test_get_long_count(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check if the get long count method obtains the correct value.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.flexural_design.flex_rebar_count == 3


def test_get_flex_req(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check if the correct flexural reinforcement values are obtained.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.beam.req_top_flex_reinf == [1036.5, 844.5, 866.5]
    assert designed_beam.beam.req_bot_flex_reinf == [878.5, 918.5, 817.5]
    assert designed_beam.beam.req_torsion_flex_reinf == [0, 0, 0]


def test_top_left_flex_rebar(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected top left flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.top_flex_rebar["left"],
        "3T16 + 3T16",
        1206,
        85.9,
        [16, 16],
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
        "3T16 + 3T16",
        1206,
        70.0,
        [16, 16],
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
        "3T16 + 3T16",
        1206,
        71.8,
        [16, 16],
    )


def test_bot_left_flex_rebar(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected top left flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.bot_flex_rebar["left"],
        "3T20",
        942,
        93.3,
        [20],
    )
    print(designed_beam.beam.req_top_flex_reinf)


def test_bot_middle_flex_rebar(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the expected top middle flex rebar is calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_flex_rebar(
        designed_beam.flexural_design.bot_flex_rebar["middle"],
        "3T20",
        942,
        97.5,
        [20],
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
        "3T20",
        942,
        86.8,
        [20],
    )


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
    assert designed_beam.shear_design.total_req_shear == [1689, 1691, 1629]


def test_shear_legs(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the correct number of shear legs are calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.shear_design.shear_links_count == [2, 3]


def test_min_shear_long_spacing(
    designed_beam: SRC.beam_design.BeamDesign,
) -> None:
    """Check that the expected codal spacing is calculated correctly.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    assert designed_beam.shear_design.shear_spacing == [100]
    assert designed_beam.shear_design.shear_center_spacing == [
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
        "2L-T12@100",
        2262,
        74.7,
        12,
        100,
    )


def test_middle_shear_links(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected middle shear links are calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_shear_link(
        designed_beam.shear_design.shear_links["middle"],
        "3L-T12@200",
        1696,
        99.7,
        12,
        200,
    )


def test_right_shear_links(designed_beam: SRC.beam_design.BeamDesign) -> None:
    """Check that the expected right shear links are calculated.

    Args:
        designed_beam (SRC.beam_design.BeamDesign): Refer to example.
    """
    _assert_shear_link(
        designed_beam.shear_design.shear_links["right"],
        "2L-T12@100",
        2262,
        72.0,
        12,
        100,
    )


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
