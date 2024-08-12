"""Edgecases: Span less than 3m, must copy reinforcement to all locations.

Also checks that torsion reinforcement is split to top and bottom reinf.
"""

import pytest
from pytest import approx

import SRC.beam
import SRC.flexure
import SRC.shear
import SRC.sideface


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
def example_flexure(example_beam: SRC.beam.Beam) -> SRC.flexure.Flexure:
    """Example flexure object utilised for testing purposes.

    Currently mimicking beam B46 at roof level.

    Returns:
        SRC.flexure.Flexure: Example flexure to utilise in tests.
    """
    example_flexure = SRC.flexure.Flexure(example_beam)
    example_flexure.get_long_count()
    example_flexure.flex_torsion_splitting()
    example_flexure.get_flex_rebar()
    example_flexure.assess_feasibility()
    example_flexure.get_residual_rebar()
    return example_flexure


@pytest.fixture
def example_shear(
    example_beam: SRC.beam.Beam, example_flexure: SRC.flexure.Flexure
) -> SRC.shear.Shear:
    """Example shear object utilised for testing purposes.

    Currently mimicking beam B46 at roof level.

    Returns:
        SRC.shear.Shear: Example shear to utilise in tests.
    """
    example_shear = SRC.shear.Shear(example_beam, example_flexure)
    example_shear.get_shear_links()
    example_shear.get_total_shear_req()
    example_shear.get_min_shear_spacing()
    example_shear.get_shear_links()
    return example_shear


def test_get_long_count(example_beam: SRC.beam.Beam) -> None:
    """Check if the get long count method obtains the correct value.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.get_long_count()
    assert flexural_design.flex_rebar_count == 3


def test_get_flex_top_req(example_beam: SRC.beam.Beam) -> None:
    """Check if the correct flexural reinforcement values are obtained.

    Args:
        example_beam (Beam): Refer to beam example.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.flex_torsion_splitting()
    assert example_beam.req_top_flex_reinf == [
        1036.5,
        844.5,
        866.5,
    ] and example_beam.req_torsion_flex_reinf == [0, 0, 0]


def test_get_flex_bot_req(example_beam: SRC.beam.Beam) -> None:
    """Check if the correct flexural reinforcement values are obtained.

    Args:
        example_beam (Beam): Refer to beam example.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.flex_torsion_splitting()
    assert example_beam.req_bot_flex_reinf == [
        878.5,
        918.5,
        817.5,
    ] and example_beam.req_torsion_flex_reinf == [0, 0, 0]


def test_top_flex_rebar_string(example_beam: SRC.beam.Beam) -> None:
    """Check that the top flexural rebar matches is what is expected.

    Args:
        example_beam (Beam): Refer to beam example.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.get_long_count()
    flexural_design.flex_torsion_splitting()
    flexural_design.get_flex_rebar()
    flexural_design.assess_feasibility()
    assert flexural_design.top_flex_rebar["left"]["rebar_text"] == "3T16 + 3T16"
    assert (
        flexural_design.top_flex_rebar["middle"]["rebar_text"] == "3T16 + 3T16"
    )
    assert (
        flexural_design.top_flex_rebar["right"]["rebar_text"] == "3T16 + 3T16"
    )


def test_bot_flex_rebar_string(example_beam: SRC.beam.Beam) -> None:
    """CCheck that the bottom flexural rebar matches what is expected.

    Args:
        example_beam (Beam): Refer to beam example.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.get_long_count()
    flexural_design.flex_torsion_splitting()
    flexural_design.get_flex_rebar()
    flexural_design.assess_feasibility()
    assert flexural_design.bot_flex_rebar["left"]["rebar_text"] == "3T20"
    assert flexural_design.bot_flex_rebar["middle"]["rebar_text"] == "3T20"
    assert flexural_design.bot_flex_rebar["right"]["rebar_text"] == "3T20"


def test_top_flex_rebar_area(example_beam: SRC.beam.Beam) -> None:
    """Check that the top flexural rebar matches what would be expected.

    Args:
        example_beam (Beam): Refer to example beam.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.get_long_count()
    flexural_design.flex_torsion_splitting()
    flexural_design.get_flex_rebar()
    flexural_design.assess_feasibility()
    assert flexural_design.top_flex_rebar["left"]["provided_reinf"] == approx(
        1206
    )
    assert flexural_design.top_flex_rebar["middle"]["provided_reinf"] == approx(
        1206
    )
    assert flexural_design.top_flex_rebar["right"]["provided_reinf"] == approx(
        1206
    )


def test_bot_flex_rebar_area(example_beam: SRC.beam.Beam) -> None:
    """Check that the bottom flexural rebar matches what would be expected.

    Args:
        example_beam (Beam): Refer to example beam.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.get_long_count()
    flexural_design.flex_torsion_splitting()
    flexural_design.get_flex_rebar()
    flexural_design.assess_feasibility()
    assert flexural_design.bot_flex_rebar["left"]["provided_reinf"] == approx(
        942
    )
    assert flexural_design.bot_flex_rebar["middle"]["provided_reinf"] == approx(
        942
    )
    assert flexural_design.bot_flex_rebar["right"]["provided_reinf"] == approx(
        942
    )


def test_residual_rebar(example_beam: SRC.beam.Beam) -> None:
    """This test checks that the residual rebar value is correctly obtained.

    Args:
        example_beam (Beam): Refer to example beam.
    """
    flexural_design = SRC.flexure.Flexure(example_beam)
    flexural_design.get_long_count()
    flexural_design.flex_torsion_splitting()
    flexural_design.get_flex_rebar()
    flexural_design.assess_feasibility()
    flexural_design.get_residual_rebar()
    assert flexural_design.residual_rebar["left"] == approx(0)
    assert flexural_design.residual_rebar["middle"] == approx(0)
    assert flexural_design.residual_rebar["right"] == approx(0)


def test_total_shear_req(
    example_beam: SRC.beam.Beam, example_flexure: SRC.flexure.Flexure
) -> None:
    """Check that the total shear requirement is correctly calculated.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
    """
    shear_design = SRC.shear.Shear(example_beam, example_flexure)
    shear_design.get_total_shear_req()
    assert shear_design.total_req_shear == [1689, 1691, 1629]


def test_shear_legs(
    example_beam: SRC.beam.Beam, example_flexure: SRC.flexure.Flexure
) -> None:
    """Check that the correct number of shear legs are calculated.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
    """
    shear_design = SRC.shear.Shear(example_beam, example_flexure)
    shear_design.get_shear_links_count()
    assert shear_design.shear_links_count == [2, 3]


def test_min_shear_long_spacing(
    example_beam: SRC.beam.Beam, example_flexure: SRC.flexure.Flexure
) -> None:
    """Check that the expected codal spacing is calculated correctly.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
    """
    shear_design = SRC.shear.Shear(example_beam, example_flexure)
    shear_design.get_min_shear_spacing()
    assert shear_design.shear_spacing == [100]
    assert shear_design.shear_center_spacing == [200, 150, 125, 100]


def test_get_shear_string(
    example_beam: SRC.beam.Beam, example_flexure: SRC.flexure.Flexure
) -> None:
    """Check that the expected shear links are calculated.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
    """
    shear_design = SRC.shear.Shear(example_beam, example_flexure)
    shear_design.get_total_shear_req()
    shear_design.get_shear_links_count()
    shear_design.get_min_shear_spacing()
    shear_design.get_shear_links()
    assert shear_design.shear_links["left"]["links_text"] == "2L-T12@100"
    assert shear_design.shear_links["middle"]["links_text"] == "3L-T12@200"
    assert shear_design.shear_links["right"]["links_text"] == "2L-T12@100"


def test_shear_area(
    example_beam: SRC.beam.Beam, example_flexure: SRC.flexure.Flexure
) -> None:
    """Check that the shear links match the derived shear string.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
    """
    shear_design = SRC.shear.Shear(example_beam, example_flexure)
    shear_design.get_total_shear_req()
    shear_design.get_shear_links_count()
    shear_design.get_min_shear_spacing()
    shear_design.get_shear_links()
    assert shear_design.shear_links["left"]["provided_reinf"] == approx(2262)
    assert shear_design.shear_links["middle"]["provided_reinf"] == approx(1696)
    assert shear_design.shear_links["right"]["provided_reinf"] == approx(2262)


def test_required_sideface_reinforcement(
    example_beam: SRC.beam.Beam,
    example_flexure: SRC.flexure.Flexure,
    example_shear: SRC.shear.Shear,
) -> None:
    """Check that the correct sideface area requirement is calculated.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
        example_shear (SRC.shear.Shear): Refer to shear example.
    """
    sideface_design = SRC.sideface.Sideface(
        example_beam, example_flexure, example_shear
    )
    sideface_design.get_required_reinforcement()
    assert sideface_design.required_torsion_reinforcement["left"] == 0
    assert sideface_design.required_torsion_reinforcement["middle"] == 0
    assert sideface_design.required_torsion_reinforcement["right"] == 0


def test_sideface_clear_space(
    example_beam: SRC.beam.Beam,
    example_flexure: SRC.flexure.Flexure,
    example_shear: SRC.shear.Shear,
) -> None:
    """Check that the correct sideface clearspace is calculated.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
        example_shear (SRC.shear.Shear): Refer to shear example.
    """
    sideface_design = SRC.sideface.Sideface(
        example_beam, example_flexure, example_shear
    )
    sideface_design.get_sideface_clear_space()
    assert sideface_design.sideface_clearspace == 0


def test_sideface_string(
    example_beam: SRC.beam.Beam,
    example_flexure: SRC.flexure.Flexure,
    example_shear: SRC.shear.Shear,
) -> None:
    """Check that the correct sideface rebar string is calculated.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
        example_shear (SRC.shear.Shear): Refer to shear example.
    """
    sideface_design = SRC.sideface.Sideface(
        example_beam, example_flexure, example_shear
    )
    sideface_design.get_required_reinforcement()
    sideface_design.get_sideface_clear_space()
    sideface_design.get_sideface_rebar()
    assert sideface_design.sideface_rebar["rebar_text"] == "-"


def test_sideface_area(
    example_beam: SRC.beam.Beam,
    example_flexure: SRC.flexure.Flexure,
    example_shear: SRC.shear.Shear,
) -> None:
    """Check that the correct sideface rebar area is calculated.

    Args:
        example_beam (SRC.beam.Beam): Refer to beam example.
        example_flexure (SRC.flexure.Flexure): Refer to flexure example.
        example_shear (SRC.shear.Shear): Refer to shear example.
    """
    sideface_design = SRC.sideface.Sideface(
        example_beam, example_flexure, example_shear
    )
    sideface_design.get_required_reinforcement()
    sideface_design.get_sideface_clear_space()
    sideface_design.get_sideface_rebar()
    assert sideface_design.sideface_rebar["provided_reinf"] == 0
