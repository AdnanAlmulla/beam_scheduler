import numpy as np
from dataclasses import dataclass, field
from typing import List


@dataclass
class Beam:
    """This class encapsulates the necessary attributes to return a solved beam reinforcement object."""

    storey: str = "No storey provided."
    etabs_id: str = "No ETABS ID."
    width: int = 0  # in mm
    depth: int = 0  # in mm
    span: int = 0  # in mm
    comp_conc_grade: int = 0  # in MPa (n/mm^2)
    # Index 0 of this list is positive flexure, index 1 is negative flexure.
    flex_overstressed: List[bool] = field(default_factory=lambda: [False, False])
    # Index 0 of this list is shear, index 1 is torsion.
    req_top_flex_reinf: List[int] = field(default_factory=lambda: [0, 0, 0])  # in mm^2
    req_bot_flex_reinf: List[int] = field(default_factory=lambda: [0, 0, 0])  # in mm^2
    req_torsion_flex_reinf: List[int] = field(
        default_factory=lambda: [0, 0, 0]
    )  # in mm^2
    shear_force: List[int] = field(default_factory=lambda: [0, 0, 0])  # in kN
    shear_overstressed: List[bool] = field(default_factory=lambda: [False, False])
    req_shear_reinf: List[int] = field(default_factory=lambda: [0, 0, 0])  # in mm^2
    req_torsion_reinf: List[int] = field(default_factory=lambda: [0, 0, 0])  # in mm^2
    eff_depth: int = field(init=False)  # in mm

    def __post_init__(self):
        self.eff_depth = 0.8 * self.depth

    @staticmethod
    def get_width(width: str) -> int:
        """This function cleans and retrieves the width of the beam.
        Args:
            width (str): Width in column of dataframe.
        Returns:
            int: Width of beam.
        """
        width_list = list(width)
        width_list = [el.lower() for el in width_list]
        excluded_values = ["p", "t", "b", "-", "_", "c", "/", "s", "w"]
        cleaned_width_list = [ex for ex in width_list if ex not in excluded_values]
        index_list = cleaned_width_list.index("x")
        width_list = cleaned_width_list[:index_list]
        true_width = "".join(width_list)
        return int(true_width)

    @staticmethod
    def get_depth(depth: str) -> int:
        """This function cleans and retrieves the depth of the beam.

        Args:
            depth (str): Depth in column of dataframe.

        Returns:
            int: Depth of beam.
        """
        depth_list = list(depth)
        depth_list = [el.lower() for el in depth_list]
        excluded_values = ["p", "t", "b", "-", "_", "c", "/", "s", "w"]
        cleaned_depth_list = [ex for ex in depth_list if ex not in excluded_values]
        index_list = cleaned_depth_list.index("x")
        depth_list = cleaned_depth_list[1 + index_list : -4]
        true_depth = "".join(depth_list)
        return int(true_depth)

    @staticmethod
    def get_comp_conc_grade(comp_conc_grade: str) -> int:
        """This function cleans and retrieves the cylinderical concrete compressive strength, fc'.

        Args:
            comp_conc_grade (str): the section string to clean and get the compressive strength of the beam from.

        Returns:
            int: the cylincderial concrete compressive strength, fc'.
        """
        section_list = list(comp_conc_grade)
        section_list = [el.lower() for el in section_list]
        excluded_values = ["p", "t", "b", "-", "_", "x", "s", "w"]
        excluded_section_list = [ex for ex in section_list if ex not in excluded_values]
        index_c = excluded_section_list.index("c")
        index_slash = excluded_section_list.index("/")
        retrieved_value = excluded_section_list[1 + index_c : index_slash]
        conc_grade = "".join(retrieved_value)
        return int(conc_grade)

    @staticmethod
    def provided_reinforcement(diameter: int) -> float:
        """This is the main function to provide reinforcement and is utilised for clarity purposes.

        Args:
            diameter (int): The selected diameter to provide.

        Returns:
            float: An integer representing the provided reinforcement area in mm^2.
        """
        return np.pi * (diameter / 2) ** 2


# class Beam:
#     """This class encapsulates the necessary attributes to return a solved beam reinforcement object."""

#     def __init__(
#         self,
#         story,
#         id,
#         width,
#         depth,
#         span,
#         comp_conc_grade,
#         pos_flex_combo,
#         neg_flex_combo,
#         req_top_flex_reinf,
#         req_bot_flex_reinf,
#         req_flex_torsion_reinf,
#         shear_force,
#         shear_combo,
#         torsion_combo,
#         req_shear_reinf,
#         req_torsion_reinf,
#     ):
#         """Begin by initializing attributes that define the makeup of a reinforced
#         concrete beam.
#         """
#         self.story = story
#         self.id = id
#         self.width = width
#         self.depth = depth
#         self.span = span
#         self.comp_conc_grade = comp_conc_grade
#         self.eff_depth = 0
#         self.pos_flex_combo = pos_flex_combo
#         self.neg_flex_combo = neg_flex_combo
#         self.req_top_flex_reinf = req_top_flex_reinf
#         self.req_bot_flex_reinf = req_bot_flex_reinf
#         self.req_flex_torsion_reinf = req_flex_torsion_reinf
#         self.shear_force = shear_force
#         self.shear_combo = shear_combo
#         self.torsion_combo = torsion_combo
#         self.req_shear_reinf = req_shear_reinf
#         self.req_torsion_reinf = req_torsion_reinf
#         self.flex_rebar_count = None
#         self.flex_top_left_dia = 0
#         self.flex_top_left_dia_two = 0
#         self.flex_top_middle_dia = 0
#         self.flex_top_middle_dia_two = 0
#         self.flex_top_right_dia = 0
#         self.flex_top_right_dia_two = 0
#         self.flex_bot_left_dia = 0
#         self.flex_bot_left_dia_two = 0
#         self.flex_bot_middle_dia = 0
#         self.flex_bot_middle_dia_two = 0
#         self.flex_bot_right_dia = 0
#         self.flex_bot_right_dia_two = 0
#         self.flex_top_left_rebar_string = None
#         self.flex_top_left_rebar_area = None
#         self.flex_top_middle_rebar_string = None
#         self.flex_top_middle_rebar_area = None
#         self.flex_top_right_rebar_string = None
#         self.flex_top_right_rebar_area = None
#         self.flex_bot_left_rebar_string = None
#         self.flex_bot_left_rebar_area = None
#         self.flex_bot_middle_rebar_string = None
#         self.flex_bot_middle_rebar_area = None
#         self.flex_bot_right_rebar_string = None
#         self.flex_bot_right_rebar_area = None
#         self.left_residual_rebar = 0
#         self.middle_residual_rebar = 0
#         self.right_residual_rebar = 0
#         self.req_total_left_shear_reinf = 0
#         self.req_total_middle_shear_reinf = 0
#         self.req_total_right_shear_reinf = 0
#         self.req_shear_legs = 0
#         self.shear_left_dia = 0
#         self.shear_middle_dia = 0
#         self.shear_right_dia = 0
#         self.min_shear_long_spacing = 0
#         self.min_shear_centre_long_spacing = 0
#         self.shear_left_string = None
#         self.shear_left_area = None
#         self.shear_middle_string = None
#         self.shear_middle_area = None
#         self.shear_right_string = None
#         self.shear_right_area = None
#         self.selected_shear_left_string = None
#         self.selected_shear_left_area = None
#         self.selected_shear_middle_string = None
#         self.selected_shear_middle_area = None
#         self.selected_shear_right_string = None
#         self.selected_shear_right_area = None
#         self.side_face_clear_space = None
#         self.side_face_left_string = None
#         self.side_face_left_area = None
#         self.side_face_middle_string = None
#         self.side_face_middle_area = None
#         self.side_face_right_string = None
#         self.side_face_right_area = None
#         self.selected_side_face_reinforcement_string = None
#         self.selected_side_face_reinforcement_area = None
#         self.req_bot_left_flex_reinf = 0
#         self.req_bot_middle_flex_reinf = 0
#         self.req_bot_right_flex_reinf = 0
#         self.transverse_space_check = None
#         self.final_shear_legs = 0

#     def get_top_flex_rebar_string(self):
#         """This method loops through the required top flexural reinforcement and provides a string
#         containing the schedule for each part of the beam. Once the string has been made, the schedule
#         for each section of the beam is indexed to its relevant attribute."""
#         dia_list = [16, 20, 25, 32]
#         target = self.req_top_flex_reinf.copy()
#         if self.neg_flex_combo == "False":
#             for index, req in enumerate(target):
#                 found = False
#                 for dia_1 in dia_list:
#                     if (
#                         (Beam.provided_reinforcement(dia_1)) * self.flex_rebar_count  # type: ignore
#                     ) > req:
#                         target[index] = f"{self.flex_rebar_count}T{dia_1}"
#                         found = True
#                         # Assign the computed diameter to the appropriate attributes immediately after determining them
#                         if index == 0:
#                             self.flex_top_left_dia = dia_1
#                         elif index == 1:
#                             self.flex_top_middle_dia = dia_1
#                         elif index == 2:
#                             self.flex_top_right_dia = dia_1
#                         break
#                 if not found:
#                     for dia_2 in dia_list:
#                         for dia_1 in dia_list:
#                             if (
#                                 (Beam.provided_reinforcement(dia_1))  # type: ignore
#                                 * self.flex_rebar_count
#                                 + (Beam.provided_reinforcement(dia_2))  # type: ignore
#                                 * self.flex_rebar_count
#                             ) > req:
#                                 target[index] = (
#                                     f"{self.flex_rebar_count}T{dia_1} + {self.flex_rebar_count}T{dia_2}"
#                                 )
#                                 found = True
#                                 # Assign the computed diameters to the appropriate attributes immediately after determining them
#                                 if index == 0:
#                                     self.flex_top_left_dia = dia_1
#                                     self.flex_top_left_dia_two = dia_2
#                                 elif index == 1:
#                                     self.flex_top_middle_dia = dia_1
#                                     self.flex_top_middle_dia_two = dia_2
#                                 elif index == 2:
#                                     self.flex_top_right_dia = dia_1
#                                     self.flex_top_right_dia_two = dia_2
#                                 break
#                         if found:
#                             break
#                 if not found:
#                     target[index] = "Increase rebar count or re-assess"
#         else:
#             target = ["Overstressed. Please re-assess"] * len(target)
#         self.flex_top_left_rebar_string = target[0]
#         self.flex_top_middle_rebar_string = target[1]
#         self.flex_top_right_rebar_string = target[2]

#     def get_top_flex_rebar_area(self):
#         """This method loops through the required top flexural reinforcement and provides the calculated area
#         for each beam schedule. Once calculated, the value
#         for each section of the beam is indexed to its relevant attribute.
#         """
#         dia_list = [16, 20, 25, 32]
#         target = self.req_top_flex_reinf.copy()
#         if self.neg_flex_combo == "False":
#             for index, req in enumerate(target):
#                 found = False
#                 for dia_1 in dia_list:
#                     if Beam.provided_reinforcement(dia_1) * self.flex_rebar_count > req:  # type: ignore
#                         target[index] = (
#                             Beam.provided_reinforcement(dia_1) * self.flex_rebar_count  # type: ignore
#                         )
#                         found = True
#                         break
#                 if not found:
#                     for dia_2 in dia_list:
#                         for dia_1 in dia_list:
#                             if (
#                                 Beam.provided_reinforcement(dia_1)  # type: ignore
#                                 * self.flex_rebar_count
#                             ) + (
#                                 Beam.provided_reinforcement(dia_2)  # type: ignore
#                                 * self.flex_rebar_count
#                             ) > req:
#                                 target[index] = (
#                                     Beam.provided_reinforcement(dia_1)  # type: ignore
#                                     * self.flex_rebar_count
#                                 ) + (
#                                     Beam.provided_reinforcement(dia_2)  # type: ignore
#                                     * self.flex_rebar_count
#                                 )
#                                 found = True
#                                 break
#                         if found:
#                             break
#                 if not found:
#                     target[index] = "Increase rebar count or re-assess"
#         else:
#             target = ["Overstressed. Please re-assess"] * len(target)
#         self.flex_top_left_rebar_area = target[0]
#         self.flex_top_middle_rebar_area = target[1]
#         self.flex_top_right_rebar_area = target[2]

#     def get_bot_flex_rebar_string(self):
#         """This method loops through the required bottom flexural reinforcement and provides a string
#         containing the schedule for each part of the beam. Once the string has been made, the schedule
#         for each section of the beam is indexed to its relevant attribute.
#         """
#         dia_list = [16, 20, 25, 32]
#         target = self.req_bot_flex_reinf.copy()

#         if self.pos_flex_combo == "False":
#             for index, req in enumerate(target):
#                 found = False
#                 for dia_1 in dia_list:
#                     if Beam.provided_reinforcement(dia_1) * self.flex_rebar_count > req:  # type: ignore
#                         target[index] = f"{self.flex_rebar_count}T{dia_1}"
#                         found = True
#                         # Assign the computed diameter to appropriate attributes after determining them
#                         if index == 0:
#                             self.flex_bot_left_dia = dia_1
#                         elif index == 1:
#                             self.flex_bot_middle_dia = dia_1
#                         elif index == 2:
#                             self.flex_bot_right_dia = dia_1
#                         break
#                 if not found:
#                     for dia_2 in dia_list:
#                         for dia_1 in dia_list:
#                             if (
#                                 Beam.provided_reinforcement(dia_1)  # type: ignore
#                                 * self.flex_rebar_count
#                                 + Beam.provided_reinforcement(dia_2)  # type: ignore
#                                 * self.flex_rebar_count
#                                 > req
#                             ):
#                                 target[index] = (
#                                     f"{self.flex_rebar_count}T{dia_1} + {self.flex_rebar_count}T{dia_2}"
#                                 )
#                                 found = True
#                                 # Assign the computed diameter to appropriate attributes after determining them
#                                 if index == 0:
#                                     self.flex_bot_left_dia = dia_1
#                                     self.flex_bot_left_dia_two = dia_2
#                                 elif index == 1:
#                                     self.flex_bot_middle_dia = dia_1
#                                     self.flex_bot_middle_dia_two = dia_2
#                                 elif index == 2:
#                                     self.flex_bot_right_dia = dia_1
#                                     self.flex_bot_right_dia_two = dia_2
#                                 break
#                         if found:
#                             break
#                 if not found:
#                     target[index] = "Increase rebar count or re-assess"
#         else:
#             target = ["Overstressed. Please re-assess"] * len(target)
#         self.flex_bot_left_rebar_string = target[0]
#         self.flex_bot_middle_rebar_string = target[1]
#         self.flex_bot_right_rebar_string = target[2]

#     def get_bot_flex_rebar_area(self):
#         """This method loops through the required bottom flexural reinforcement and provides the calculated area
#         for each beam schedule. Once calculated, the value
#         for each section of the beam is indexed to its relevant attribute.
#         """
#         dia_list = [16, 20, 25, 32]
#         target = self.req_bot_flex_reinf.copy()
#         if self.pos_flex_combo == "False":
#             for index, req in enumerate(target):
#                 found = False
#                 for dia_1 in dia_list:
#                     if Beam.provided_reinforcement(dia_1) * self.flex_rebar_count > req:  # type: ignore
#                         target[index] = (
#                             Beam.provided_reinforcement(dia_1) * self.flex_rebar_count  # type: ignore
#                         )
#                         found = True
#                         break
#                 if not found:
#                     for dia_2 in dia_list:
#                         for dia_1 in dia_list:
#                             if (
#                                 Beam.provided_reinforcement(dia_1)  # type: ignore
#                                 * self.flex_rebar_count
#                             ) + (
#                                 Beam.provided_reinforcement(dia_2)  # type: ignore
#                                 * self.flex_rebar_count
#                             ) > req:
#                                 target[index] = (
#                                     Beam.provided_reinforcement(dia_1)  # type: ignore
#                                     * self.flex_rebar_count
#                                 ) + (
#                                     Beam.provided_reinforcement(dia_2)  # type: ignore
#                                     * self.flex_rebar_count
#                                 )
#                                 found = True
#                                 break
#                         if found:
#                             break
#                 if not found:
#                     target[index] = "Increase rebar count or re-assess"
#         else:
#             target = ["Overstressed. Please re-assess"] * len(target)
#         self.flex_bot_left_rebar_area = target[0]
#         self.flex_bot_middle_rebar_area = target[1]
#         self.flex_bot_right_rebar_area = target[2]

#     def get_residual_rebar(self):
#         """This method takes the obtained flexural rebar area in both the top and bottom and subtracts them by
#         their relevant required area. It then adds the remaining top and bottom residual together.
#         """
#         top_combined = [
#             self.flex_top_left_rebar_area,
#             self.flex_top_middle_rebar_area,
#             self.flex_top_right_rebar_area,
#         ]
#         bot_combined = [
#             self.flex_bot_left_rebar_area,
#             self.flex_bot_middle_rebar_area,
#             self.flex_bot_right_rebar_area,
#         ]
#         if all(isinstance(x, (float, int)) for x in top_combined) and all(
#             isinstance(x, (float, int)) for x in bot_combined
#         ):
#             top_left_residual = (
#                 self.flex_top_left_rebar_area - self.req_top_flex_reinf[0]
#             )
#             top_middle_residual = (
#                 self.flex_top_middle_rebar_area - self.req_top_flex_reinf[1]
#             )
#             top_right_residual = (
#                 self.flex_top_right_rebar_area - self.req_top_flex_reinf[2]
#             )
#             bot_left_residual = (
#                 self.flex_bot_left_rebar_area - self.req_bot_flex_reinf[0]
#             )
#             bot_middle_residual = (
#                 self.flex_bot_middle_rebar_area - self.req_bot_flex_reinf[1]
#             )
#             bot_right_residual = (
#                 self.flex_bot_right_rebar_area - self.req_bot_flex_reinf[2]
#             )
#             self.left_residual_rebar = top_left_residual + bot_left_residual
#             self.middle_residual_rebar = top_middle_residual + bot_middle_residual
#             self.right_residual_rebar = top_right_residual + bot_right_residual
#         else:
#             self.left_residual_rebar = None
#             self.middle_residual_rebar = None
#             self.right_residual_rebar = None

#     def get_total_shear_req(self):
#         """This method calls the required shear and torsion reinforcement attributes and calculates
#         the total shear reinforcement required. It also checks against the combos and returns whether
#         it is O/S or not.
#         """
#         if self.shear_combo == "False" and self.torsion_combo == "False":
#             shear_list = [
#                 a + 2 * b for a, b in zip(self.req_shear_reinf, self.req_torsion_reinf)
#             ]
#             self.req_total_left_shear_reinf = shear_list[0]
#             self.req_total_middle_shear_reinf = shear_list[1]
#             self.req_total_right_shear_reinf = shear_list[2]
#         elif self.shear_combo == "False" and self.torsion_combo == "True":
#             self.req_total_left_shear_reinf = "O/S in Torsion"
#             self.req_total_middle_shear_reinf = "O/S in Torsion"
#             self.req_total_right_shear_reinf = "O/S in Torsion"
#         elif self.shear_combo == "True" and self.torsion_combo == "False":
#             self.req_total_left_shear_reinf = "O/S in Shear"
#             self.req_total_middle_shear_reinf = "O/S in Shear"
#             self.req_total_right_shear_reinf = "O/S in Shear"
#         else:
#             self.req_total_left_shear_reinf = "O/S in Shear and Torsion"
#             self.req_total_middle_shear_reinf = "O/S in Shear and Torsion"
#             self.req_total_right_shear_reinf = "O/S in Shear and Torsion"

#     def get_shear_legs(self):
#         """This method calculates the required shear legs based on the maximum transverse shear spacing as required
#         in Table 9.7.6.2.2. of ACI 318-19.
#         """
#         max_transverse_spacing = min(self.eff_depth, 600)
#         req_legs = (max_transverse_spacing - 80) / self.width
#         if req_legs < 2:
#             self.req_shear_legs = 2
#         else:
#             self.req_shear_legs = np.ceil(req_legs)

#     def get_shear_string(self):
#         """This method calculates the required shear reinforcement string.
#         It defines two lists: one diameter list, ranging from 12 to 25mm dia, and another spacing
#         list from 250 to 100mm. It utilises a truthy statement to ensure that the right
#         diameter and spacing combination is found for the shear reinforcement."""
#         shear_dia_list = [12, 16, 20, 25]
#         shear_spacing_list = [250, 200, 150, 125, 100, self.min_shear_long_spacing]
#         shear_spacing_list = list(
#             set(
#                 spacing
#                 for spacing in shear_spacing_list
#                 if spacing <= self.min_shear_long_spacing
#             )
#         )
#         shear_spacing_list.sort(reverse=True)
#         shear_legs_list = list(range(self.req_shear_legs, self.flex_rebar_count + 1, 2))
#         target = [
#             self.req_total_left_shear_reinf,
#             self.req_total_middle_shear_reinf,
#             self.req_total_right_shear_reinf,
#         ]
#         if self.shear_combo == "False" and self.torsion_combo == "False":
#             for index, (req, tor_req) in enumerate(zip(target, self.req_torsion_reinf)):
#                 found = False
#                 for dia in shear_dia_list:
#                     if found:
#                         break
#                     for spacing in shear_spacing_list:
#                         if found:
#                             break
#                         for legs in shear_legs_list:
#                             if found:
#                                 break
#                             if (1000 / spacing) * (
#                                 Beam.provided_reinforcement(dia)
#                             ) * legs > req and (  # type: ignore
#                                 1000 / spacing
#                             ) * (Beam.provided_reinforcement(dia)) * 2 > tor_req:  # type: ignore
#                                 target[index] = f"{legs}L-T{dia}@{spacing}"
#                                 found = True
#                                 if index == 0:
#                                     self.shear_left_dia = dia
#                                 elif index == 1:
#                                     self.shear_middle_dia = dia
#                                 elif index == 2:
#                                     self.shear_right_dia = dia
#                                 break
#         else:
#             target = ["Overstressed. Please re-assess"] * len(target)
#         self.shear_left_string = target[0]
#         self.shear_middle_string = target[1]
#         self.shear_right_string = target[2]

#     def get_shear_area(self):
#         """This method calculates the required shear reinforcement area.
#         It defines two lists: one diameter list, ranging from 12 to 25mm dia, and another spacing
#         list from 250 to 100mm. It utilises a truthy statement to ensure that the right
#         diameter and spacing combination is found for the shear reinforcement."""
#         shear_dia_list = [12, 16, 20, 25]
#         shear_spacing_list = [250, 200, 150, 125, 100, self.min_shear_long_spacing]
#         shear_spacing_list = list(
#             set(
#                 spacing
#                 for spacing in shear_spacing_list
#                 if spacing <= self.min_shear_long_spacing
#             )
#         )
#         shear_spacing_list.sort(reverse=True)
#         shear_legs_list = list(range(self.req_shear_legs, self.flex_rebar_count + 1, 2))
#         target = [
#             self.req_total_left_shear_reinf,
#             self.req_total_middle_shear_reinf,
#             self.req_total_right_shear_reinf,
#         ]
#         if self.shear_combo == "False" and self.torsion_combo == "False":
#             for index, (req, tor_req) in enumerate(zip(target, self.req_torsion_reinf)):
#                 found = False
#                 for dia in shear_dia_list:
#                     if found:
#                         break
#                     for spacing in shear_spacing_list:
#                         if found:
#                             break
#                         for legs in shear_legs_list:
#                             if found:
#                                 break
#                             if (1000 / spacing) * Beam.provided_reinforcement(
#                                 dia
#                             ) * legs > req and (
#                                 1000 / spacing
#                             ) * Beam.provided_reinforcement(dia) * 2 > tor_req:  # type: ignore
#                                 target[index] = (
#                                     (1000 / spacing)
#                                     * Beam.provided_reinforcement(dia)
#                                     * legs
#                                 )
#                                 found = True
#                                 break
#         else:
#             target = ["Overstressed. Please re-assess"] * len(target)
#         self.shear_left_area = target[0]
#         self.shear_middle_area = target[1]
#         self.shear_right_area = target[2]

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

#     def get_index_for_shear_reinf(self):
#         """This method gets the index of the shear reinforcement with the highest area.
#         If the middle index has the highest area, then all the shear reinforcement in the beam (left, middle, right)
#         are copied from the middle shear reinforcement. Otherwise, the middle shear reinforcement retains what it has
#         and the left and right reinforcement take the absolute maximum (if left is max, then right copies it and vice versa.)
#         """
#         shear_reinf_area_list = [
#             self.shear_left_area,
#             self.shear_middle_area,
#             self.shear_right_area,
#         ]
#         shear_reinf_string_list = [
#             self.shear_left_string,
#             self.shear_middle_string,
#             self.shear_right_string,
#         ]
#         max_shear_reinf_index, max_area = max(
#             enumerate(shear_reinf_area_list),
#             key=lambda x: x[1],  # type: ignore
#         )
#         if shear_reinf_area_list[1] > shear_reinf_area_list[max_shear_reinf_index]:
#             self.selected_shear_left_area = shear_reinf_area_list[1]
#             self.selected_shear_left_string = shear_reinf_string_list[1]
#             self.selected_shear_middle_area = shear_reinf_area_list[1]
#             self.selected_shear_middle_string = shear_reinf_string_list[1]
#             self.selected_shear_right_area = shear_reinf_area_list[1]
#             self.selected_shear_right_string = shear_reinf_string_list[1]
#         else:
#             self.selected_shear_left_area = shear_reinf_area_list[max_shear_reinf_index]
#             self.selected_shear_left_string = shear_reinf_string_list[
#                 max_shear_reinf_index
#             ]
#             self.selected_shear_middle_area = shear_reinf_area_list[1]
#             self.selected_shear_middle_string = shear_reinf_string_list[1]
#             self.selected_shear_right_area = shear_reinf_area_list[
#                 max_shear_reinf_index
#             ]
#             self.selected_shear_right_string = shear_reinf_string_list[
#                 max_shear_reinf_index
#             ]

#     def get_min_shear_long_spacing(self):
#         """This method follows Clause 18.4.2.4 of ACI 318-19 by ensuring that the longitudinal spacing of shear links is
#         not exceeded. This value is inputted into the spacing list found in shear string and area methods.
#         This method has been updated to follow Table 18.4.2.4, which grabs the minimum middle shear longitudinal spacing.
#         """
#         combined_long_dia_list = [
#             self.flex_top_left_dia,
#             self.flex_top_left_dia_two,
#             self.flex_top_middle_dia,
#             self.flex_top_middle_dia_two,
#             self.flex_top_right_dia,
#             self.flex_top_right_dia_two,
#             self.flex_bot_left_dia,
#             self.flex_bot_left_dia_two,
#             self.flex_bot_middle_dia,
#             self.flex_bot_middle_dia_two,
#             self.flex_bot_right_dia,
#             self.flex_bot_right_dia_two,
#         ]
#         combined_shear_dia_list = [20]

#         if (
#             self.pos_flex_combo == "False"
#             and self.neg_flex_combo == "False"
#             and "Increase rebar count or re-assess" not in combined_long_dia_list
#         ):
#             filtered_long_dia_list = [i for i in combined_long_dia_list if i != 0]
#         else:
#             filtered_long_dia_list = []

#         if self.shear_combo == "False" and self.torsion_combo == "False":
#             filtered_shear_dia_list = [i for i in combined_shear_dia_list if i != 0]
#         else:
#             filtered_shear_dia_list = []

#         if (
#             filtered_long_dia_list
#             and filtered_shear_dia_list
#             and "Overstressed. Please re-assess" not in combined_long_dia_list
#         ):
#             smallest_long_dia = min(filtered_long_dia_list)
#             smallest_shear_dia = min(filtered_shear_dia_list)
#             min_shear_long_spacing = min(
#                 [
#                     (self.eff_depth / 4),
#                     (smallest_long_dia * 8),
#                     (smallest_shear_dia * 24),
#                     300,
#                 ]
#             )
#             if min_shear_long_spacing >= 200 and min_shear_long_spacing < 250:
#                 min_shear_long_spacing = 200
#             elif min_shear_long_spacing >= 150 and min_shear_long_spacing < 200:
#                 min_shear_long_spacing = 150
#             elif min_shear_long_spacing >= 125 and min_shear_long_spacing < 150:
#                 min_shear_long_spacing = 125
#             elif min_shear_long_spacing < 125:
#                 min_shear_long_spacing = 100

#             self.min_shear_long_spacing = min_shear_long_spacing

#             self.min_shear_centre_long_spacing = min([(self.eff_depth / 2), 250])
#             if (
#                 self.min_shear_centre_long_spacing >= 200
#                 and self.min_shear_centre_long_spacing < 250
#             ):
#                 self.min_shear_centre_long_spacing = 200
#             elif (
#                 self.min_shear_centre_long_spacing >= 150
#                 and self.min_shear_centre_long_spacing < 200
#             ):
#                 self.min_shear_centre_long_spacing = 150
#             elif (
#                 self.min_shear_centre_long_spacing >= 125
#                 and self.min_shear_centre_long_spacing < 150
#             ):
#                 self.min_shear_centre_long_spacing = 125
#             elif self.min_shear_centre_long_spacing < 125:
#                 self.min_shear_centre_long_spacing = 100

#     def modify_shear_reinf(self):
#         """This method overrides the middle shear spacing to assess if the codal maximum is met. If it isn't, it sets it to the codal maximum and then iterates through
#         the design. For the left and right shear portions, the legs and spacing are set to be the same and recalculated to assess if a smaller dia is achievable.
#         """
#         shear_dia_list = [12, 16, 20, 25]

#         paired_values = []

#         shear_spacing_list = [
#             250,
#             200,
#             150,
#             125,
#             100,
#             self.min_shear_centre_long_spacing,
#         ]
#         check_shear = [
#             self.shear_left_string,
#             self.shear_middle_string,
#             self.shear_right_string,
#         ]
#         shear_spacing_list = list(
#             set(
#                 spacing
#                 for spacing in shear_spacing_list
#                 if spacing <= self.min_shear_centre_long_spacing
#             )
#         )
#         shear_spacing_list.sort(reverse=True)

#         if (
#             "Overstressed. Please re-assess" not in check_shear
#             and self.min_shear_centre_long_spacing != 0
#             and self.min_shear_long_spacing != 0
#         ):
#             left_legs = self.shear_left_string[0]
#             middle_legs = self.shear_middle_string[0]
#             right_legs = self.shear_right_string[0]
#             left_legs = int(left_legs)
#             middle_legs = int(middle_legs)
#             right_legs = int(right_legs)
#             self.final_shear_legs = max(left_legs, middle_legs, right_legs)

#             left_spacing = self.shear_left_string[-3:]
#             right_spacing = self.shear_right_string[-3:]
#             left_spacing = int(left_spacing)
#             right_spacing = int(right_spacing)
#             final_spacing = min([left_spacing, right_spacing])

#             target = [self.req_total_left_shear_reinf, self.req_total_right_shear_reinf]
#             tor_target = [self.req_torsion_reinf[0], self.req_torsion_reinf[2]]

#         if (
#             "Overstressed. Please re-assess" not in check_shear
#             and self.min_shear_centre_long_spacing != 0
#             and self.min_shear_long_spacing != 0
#         ):
#             for index, (req, tor_req) in enumerate(zip(target, tor_target)):
#                 found = False
#                 for dia in shear_dia_list:
#                     if found:
#                         break
#                     if (
#                         (1000 / final_spacing)
#                         * Beam.provided_reinforcement(dia)
#                         * self.final_shear_legs
#                     ) > req and (
#                         (1000 / final_spacing) * Beam.provided_reinforcement(dia) * 2
#                     ) > tor_req:  # type: ignore
#                         paired_values.append(
#                             [
#                                 (1000 / final_spacing)
#                                 * Beam.provided_reinforcement(dia)
#                                 * self.final_shear_legs,
#                                 f"{self.final_shear_legs}L-T{dia}@{final_spacing}",
#                             ]
#                         )
#                         if index == 0:
#                             self.shear_left_dia = dia
#                         else:
#                             self.shear_right_dia = dia
#                         found = True

#             self.shear_left_area = paired_values[0][0]
#             self.shear_right_area = paired_values[1][0]

#             self.shear_left_string = paired_values[0][1]
#             self.shear_right_string = paired_values[1][1]

#             shear_middle_spacing = int(self.shear_middle_string[-3:])  # type: ignore
#             if shear_middle_spacing < self.min_shear_centre_long_spacing:
#                 found = False
#                 for dia in shear_dia_list:
#                     if found:
#                         break
#                     for spacing in shear_spacing_list:
#                         if found:
#                             break
#                         if (
#                             (1000 / spacing)
#                             * Beam.provided_reinforcement(dia)
#                             * self.final_shear_legs
#                         ) > self.req_total_middle_shear_reinf and (
#                             (1000 / spacing) * Beam.provided_reinforcement(dia) * 2
#                         ) > self.req_torsion_reinf[1]:  # type: ignore
#                             self.shear_middle_area = (
#                                 (1000 / spacing)
#                                 * Beam.provided_reinforcement(dia)
#                                 * self.final_shear_legs
#                             )
#                             self.shear_middle_string = (
#                                 f"{self.final_shear_legs}L-T{dia}@{spacing}"
#                             )
#                             self.shear_middle_dia = dia
#                             found = True
#                             break

#     def check_transverse_shear_spacing(self):
#         """This method assesses if the required Vs is greater or less than the nominal concrete shear capacity.
#         as per Table 9.7.6.2.2 of ACI 318.19. If this is the case, the method returns a 'Yes', and if it isn't
#         it returns a 'No'.
#         """

#         # Get the maximum shear force from a list of the left, middle, and right section of the beam.
#         maximum_shear_force = max(self.shear_force)

#         # The maximum shear force is being subtracted by the concrete shear force capacity as found in Table 22.5.5.1 eq (a) of ACI 318-19
#         concrete_shear_capacity = (
#             0.17 * np.sqrt(self.comp_conc_grade) * self.width * self.eff_depth * 10**-3
#         )
#         required_vs = maximum_shear_force - concrete_shear_capacity

#         # The nominal shear capacity equation is obtained from Table 9.7.6.2.2 of ACI 318-19.
#         nominal_shear_capacity = (
#             0.33 * np.sqrt(self.comp_conc_grade) * self.width * self.eff_depth * 10**-3
#         )

#         if nominal_shear_capacity >= required_vs:
#             self.transverse_space_check = "No"
#         else:
#             self.transverse_space_check = "Yes"
