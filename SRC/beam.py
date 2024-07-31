"""Holds the beam dataclass and additional functions."""
# TODO: update the module docstring.

from dataclasses import dataclass, field
from typing import List

import numpy as np


@dataclass
class Beam:
    # TODO: provide further information to class docstring.
    """Holds and encapsulates attributes of a beam object."""

    storey: str = "No storey provided."
    etabs_id: str = "No ETABS ID."
    width: int = 0  # in mm
    depth: int = 0  # in mm
    span: int = 0  # in mm
    comp_conc_grade: int = 0  # in MPa (n/mm^2)
    # * Index 0 of this list is positive flexure, index 1 is negative flexure.
    flex_overstressed: List[bool] = field(
        default_factory=lambda: [False, False]
    )
    req_top_flex_reinf: List[int] = field(
        default_factory=lambda: [0, 0, 0]
    )  # in mm^2
    req_bot_flex_reinf: List[int] = field(
        default_factory=lambda: [0, 0, 0]
    )  # in mm^2
    req_torsion_flex_reinf: List[int] = field(
        default_factory=lambda: [0, 0, 0]
    )  # in mm^2
    shear_force: List[int] = field(default_factory=lambda: [0, 0, 0])  # in kN
    # * Index 0 of this list is shear, index 1 is torsion.
    shear_overstressed: List[bool] = field(
        default_factory=lambda: [False, False]
    )
    req_shear_reinf: List[int] = field(
        default_factory=lambda: [0, 0, 0]
    )  # in mm^2
    req_torsion_reinf: List[int] = field(
        default_factory=lambda: [0, 0, 0]
    )  # in mm^2
    eff_depth: int = field(init=False)  # in mm

    def __post_init__(self) -> None:
        """Initialises effective depth once the depth attribute is provided."""
        self.eff_depth = 0.8 * self.depth


def get_width(section: str) -> int:
    """Clean and retrieve the width of the beam.

    Args:
        section (str): Section of beam as defined in ETABS.

    Returns:
        int: Width of beam.
    """
    width_list = list(section)
    width_list = [el.lower() for el in width_list]
    excluded_values = ["p", "t", "b", "-", "_", "c", "/", "s", "w"]
    cleaned_width_list = [ex for ex in width_list if ex not in excluded_values]
    index_list = cleaned_width_list.index("x")
    width_list = cleaned_width_list[:index_list]
    true_width = "".join(width_list)
    return int(true_width)


def get_depth(section: str) -> int:
    """Clean and retrieve the depth of the beam.

    Args:
        section (str): Section of beam as defined in ETABS.

    Returns:
        int: Depth of beam.
    """
    depth_list = list(section)
    depth_list = [el.lower() for el in depth_list]
    excluded_values = ["p", "t", "b", "-", "_", "c", "/", "s", "w"]
    cleaned_depth_list = [ex for ex in depth_list if ex not in excluded_values]
    index_list = cleaned_depth_list.index("x")
    depth_list = cleaned_depth_list[1 + index_list : -4]
    true_depth = "".join(depth_list)
    return int(true_depth)


def get_comp_conc_grade(section: str) -> int:
    """Clean and retrieve the cylinderical concrete compressive strength, fc'.

    Args:
        section (str): Section of beam as defined in ETABS.

    Returns:
        int: The cylincderial concrete compressive strength, fc'.
    """
    section_list = list(section)
    section_list = [el.lower() for el in section_list]
    excluded_values = ["p", "t", "b", "-", "_", "x", "s", "w"]
    excluded_section_list = [
        ex for ex in section_list if ex not in excluded_values
    ]
    index_c = excluded_section_list.index("c")
    index_slash = excluded_section_list.index("/")
    retrieved_value = excluded_section_list[1 + index_c : index_slash]
    conc_grade = "".join(retrieved_value)
    return int(conc_grade)


def provided_reinforcement(diameter: int) -> float:
    """A static function which calculates the area of a circle.

    Args:
        diameter (int): The selected diameter to calculate the area of a circle.

    Returns:
        float: The provided reinforcement area in mm^2.
    """
    return np.pi * (diameter / 2) ** 2
