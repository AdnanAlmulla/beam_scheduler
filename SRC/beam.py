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


#     def get_side_face_clear_space(self):
#         """This method calculates the side face clear space. It assumes a cover of 40mm.
#         It takes the maximum first layer flexural diameter from both the top and bottom. It also
#         takes the maximum shear diameter. All of these are subtracted by the depth of the instanced
#         beam to acquire the allowable side face clear space.
#         """
#         dia_one_top_list = [
#             self.flex_top_left_dia,
#             self.flex_top_middle_dia,
#             self.flex_top_right_dia,
#         ]
#         dia_two_top_list = [
#             self.flex_top_left_dia_two,
#             self.flex_top_middle_dia_two,
#             self.flex_top_right_dia_two,
#         ]
#         dia_one_bot_list = [
#             self.flex_bot_left_dia,
#             self.flex_bot_middle_dia,
#             self.flex_bot_right_dia,
#         ]
#         dia_two_bot_list = [
#             self.flex_bot_left_dia_two,
#             self.flex_bot_middle_dia_two,
#             self.flex_bot_right_dia_two,
#         ]
#         dia_shear_list = [
#             self.shear_left_dia,
#             self.shear_middle_dia,
#             self.shear_right_dia,
#         ]
#         if self.depth > 700:
#             if (
#                 self.neg_flex_combo == "False"
#                 and self.pos_flex_combo == "False"
#                 and self.shear_combo == "False"
#                 and self.torsion_combo == "False"
#             ):
#                 max_top_dia_one = max(dia_one_top_list)
#                 max_top_dia_two = max(dia_two_top_list)
#                 max_bot_dia_one = max(dia_one_bot_list)
#                 max_bot_dia_two = max(dia_two_bot_list)
#                 max_shear_dia = max(dia_shear_list)
#                 self.side_face_clear_space = (
#                     self.depth
#                     - (2 * 40)
#                     - (2 * max_shear_dia)
#                     - max_top_dia_one
#                     - max_top_dia_two
#                     - max_bot_dia_one
#                     - max_bot_dia_two
#                 )
#             else:
#                 self.side_face_clear_space = "Overstressed. Please reassess"
#         else:
#             self.side_face_clear_space = "Not needed"

#     def get_side_face_string(self):
#         """This method calculates the side face reinforcement string for beam instances with a depth greater
#         than 700mm. It subtracts the required torsion from the residual calculated from the flexural reinforcement.
#         It also checks if the combos are overstressed or not. It also provides the minimum side face reinforcement
#         if the depth is greater than 900 and the flexural torsion requirement is 0."""
#         spacing_list = [250, 200, 150]
#         dia_list = [12, 16, 20, 25, 32]
#         combined_residual = [
#             self.left_residual_rebar,
#             self.middle_residual_rebar,
#             self.right_residual_rebar,
#         ]
#         if None not in combined_residual:
#             target_torsion = [
#                 a - b for a, b in zip(self.req_flex_torsion_reinf, combined_residual)
#             ]  # type: ignore
#             if (
#                 self.neg_flex_combo == "False"
#                 and self.pos_flex_combo == "False"
#                 and self.shear_combo == "False"
#                 and self.torsion_combo == "False"
#             ):
#                 if self.depth > 700:
#                     for index, req in enumerate(target_torsion):
#                         found = False
#                         for dia in dia_list:
#                             if found:
#                                 break
#                             for spacing in spacing_list:
#                                 if (
#                                     np.floor((self.side_face_clear_space / spacing))  # type: ignore
#                                     * 2
#                                     * Beam.provided_reinforcement(dia)
#                                     > req
#                                 ):
#                                     target_torsion[index] = f"T{dia}@{spacing} EF"
#                                     found = True
#                                     break
#                 else:
#                     target_torsion = ["Not needed"] * len(target_torsion)
#             else:
#                 target_torsion = ["Overstressed. Please reassess"] * len(target_torsion)
#         else:
#             target_torsion = ["Overstressed. Please reassess"] * len(combined_residual)
#         self.side_face_left_string = target_torsion[0]
#         self.side_face_middle_string = target_torsion[1]
#         self.side_face_right_string = target_torsion[2]

#     def get_side_face_area(self):
#         """This method calculates the side face reinforcement area for beam instances with a depth greater
#         than 700mm. It subtracts the required torsion from the residual calculated from the flexural reinforcement.
#         It also checks if the combos are overstressed or not. It also provides the minimum side face reinforcement
#         if the depth is greater than 900 and the flexural torsion requirement is 0."""
#         spacing_list = [250, 200, 150]
#         dia_list = [12, 16, 20, 25, 32]
#         combined_residual = [
#             self.left_residual_rebar,
#             self.middle_residual_rebar,
#             self.right_residual_rebar,
#         ]
#         if None not in combined_residual:
#             target_torsion = [
#                 a - b for a, b in zip(self.req_flex_torsion_reinf, combined_residual)
#             ]  # type: ignore
#             if (
#                 self.neg_flex_combo == "False"
#                 and self.pos_flex_combo == "False"
#                 and self.shear_combo == "False"
#                 and self.torsion_combo == "False"
#             ):
#                 if self.depth > 700:
#                     for index, req in enumerate(target_torsion):
#                         found = False
#                         for dia in dia_list:
#                             if found:
#                                 break
#                             for spacing in spacing_list:
#                                 if (
#                                     np.floor((self.side_face_clear_space / spacing))  # type: ignore
#                                     * 2
#                                     * Beam.provided_reinforcement(dia)
#                                     > req
#                                 ):
#                                     target_torsion[index] = (
#                                         np.floor(
#                                             (
#                                                 self.side_face_clear_space / spacing  # type: ignore
#                                             )
#                                         )
#                                         * 2
#                                         * Beam.provided_reinforcement(dia)
#                                     )
#                                     found = True
#                                     break
#                 else:
#                     target_torsion = ["Not needed"] * len(target_torsion)
#             else:
#                 target_torsion = ["Overstressed. Please reassess"] * len(target_torsion)
#         else:
#             target_torsion = ["Overstressed. Please reassess"] * len(combined_residual)
#         self.side_face_left_area = target_torsion[0]
#         self.side_face_middle_area = target_torsion[1]
#         self.side_face_right_area = target_torsion[2]

#     def get_index_for_side_face_reinf(self):
#         """This method gets the index of the side face reinforcement with the highest area.
#         It then takes this index and selects the side face reinforcement with the highest area as the overall
#         beam side face reinforcement.
#         """
#         side_reinf_area_list = [
#             self.side_face_left_area,
#             self.side_face_middle_area,
#             self.side_face_right_area,
#         ]
#         side_reinf_string_list = [
#             self.side_face_left_string,
#             self.side_face_middle_string,
#             self.side_face_right_string,
#         ]
#         if "Not needed" in side_reinf_area_list:
#             self.selected_side_face_reinforcement_area = 0
#             self.selected_side_face_reinforcement_string = "Not needed"
#         elif "Overstressed. Please reassess" not in side_reinf_string_list:
#             max_side_reinf_index, max_area = max(
#                 enumerate(side_reinf_area_list),
#                 key=lambda x: x[1],  # type: ignore
#             )
#             self.selected_side_face_reinforcement_area = side_reinf_area_list[
#                 max_side_reinf_index
#             ]
#             self.selected_side_face_reinforcement_string = side_reinf_string_list[
#                 max_side_reinf_index
#             ]
#         else:
#             self.selected_side_face_reinforcement_area = 0
#             self.selected_side_face_reinforcement_string = (
#                 "Rebar needs to be increased or re-assessed"
#             )
