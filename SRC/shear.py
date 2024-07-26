import Beam
import Flexure
from typing import List
import numpy as np


class Shear:
    """This class inherits Beam objects and provides new attributes relating to shear design."""

    def __init__(self, beam: Beam, flexure: Flexure):
        self.beam = beam
        self.flexure = flexure
        self.total_req_shear: List[int] = [0, 0, 0]
        self.shear_dia: List[int] = [12, 16]
        self.shear_spacing: List[int] = [250, 200, 150, 125, 100]
        self.shear_center_spacing: List[int] = [250, 200, 150, 125, 100]
        self.shear_links_count: list = []
        self.shear_links: dict = {
            "left": {
                "links_text": "",
                "provided_reinf": 0,
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            },
            "middle": {
                "links_text": "",
                "provided_reinf": 0,
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            },
            "right": {
                "links_text": "",
                "provided_reinf": 0,
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            },
        }
        self.check_transverse_shear_spacing: bool = False

    def __repr__(self):
        return f"""Shear links count: {self.shear_links_count}, \nTotal required shear reinforcement: {self.total_req_shear},
        Shear links: {self.shear_links}, \n Check transverse shear spacing: {self.check_transverse_shear_spacing}"""

    def get_shear_links_count(self):
        """This method calculates the required shear legs based on the maximum transverse shear spacing as required
        in Table 9.7.6.2.2. of ACI 318-19."""
        if True not in self.beam.shear_overstressed:
            max_transverse_spacing = min(self.beam.eff_depth, 600)
            req_legs = (self.beam.width - 80) / max_transverse_spacing
            if req_legs < 2:
                if self.flexure.flex_rebar_count == 2:
                    self.shear_links_count.append(2)
                elif self.flexure.flex_rebar_count == 3:
                    self.shear_links_count = self.shear_links_count + [2, 3]
                else:
                    self.shear_links_count = self.shear_links_count + [2, 3, 4]
            else:
                self.shear_links_count = self.shear_links_count + [2, 3, 4]

    def assess_transverse_shear_spacing(self):
        """This method assesses if the required Vs is greater or less than the nominal concrete shear capacity.
        as per Table 9.7.6.2.2 of ACI 318.19."""
        # Get the maximum shear force from a list of the left, middle, and right section of the beam.
        maximum_shear_force = max(self.beam.shear_force)
        # The maximum shear force is being subtracted by the concrete shear force capacity as found in Table 22.5.5.1 eq (a) of ACI 318-19
        concrete_shear_capacity = (
            0.17
            * np.sqrt(self.beam.comp_conc_grade)
            * self.beam.width
            * self.beam.eff_depth
            * 10**-3
        )
        required_vs = maximum_shear_force - concrete_shear_capacity
        # The nominal shear capacity equation is obtained from Table 9.7.6.2.2 of ACI 318-19.
        nominal_shear_capacity = (
            0.33
            * np.sqrt(self.beam.comp_conc_grade)
            * self.beam.width
            * self.beam.eff_depth
            * 10**-3
        )
        if nominal_shear_capacity >= required_vs:
            self.check_transverse_shear_spacing = False
        else:
            self.check_transverse_shear_spacing = True

    def get_total_shear_req(self):
        """This method calls the required shear and torsion reinforcement attributes and calculates
        the total shear reinforcement required."""
        if True in self.beam.shear_overstressed:
            for properties in self.shear_links.values():
                properties["links_text"] = "Overstressed"
        else:
            self.total_req_shear = [
                round(a + 2 * b)
                for a, b in zip(self.beam.req_shear_reinf, self.beam.req_torsion_reinf)
            ]

    # TODO: refactor get_min_shear_spacing method to be easier to read and maintain

    # def get_min_shear_spacing(self):
    #     """This method follows Clause 18.4.2.4 of ACI 318-19 by ensuring that the longitudinal spacing of shear links
    #     does not exceed its codal maximum."""
    #     # ! By writing this conditional, an overstressed condition in top or bottom reinforcement will
    #     # ! not solve for shear reinforcement.
    #     def get_min_diameter(rebar_dict):
    #         return min(min(properties["diameter"] for properties in rebar_dict.values()))

    #     if True not in (self.beam.flex_overstressed, self.beam.shear_overstressed):

    #     if True not in (self.beam.flex_overstressed, self.beam.shear_overstressed):
    #         smallest_top_long_dia = min(
    #             min(properties["diameter"])
    #             for properties in self.flexure.top_flex_rebar.values()
    #         )
    #         smallest_bot_long_dia = min(
    #             min(properties["diameter"])
    #             for properties in self.flexure.bot_flex_rebar.values()
    #         )
    #         smallest_long_dia = min(smallest_top_long_dia, smallest_bot_long_dia)
    #         # Assume the worst case diameter for shear as its not been derived yet.
    #         smallest_shear_dia = 12

    #         min_shear_spacing = min(
    #             [
    #                 (self.beam.eff_depth / 4),
    #                 (smallest_long_dia * 8),
    #                 (smallest_shear_dia * 24),
    #                 250,
    #             ]
    #         )
    #         min_shear_center_spacing = min([(self.beam.eff_depth / 2), 250])
    #         spacing_threshhold = [
    #             (200, 250, 200),
    #             (150, 200, 150),
    #             (125, 150, 125),
    #             (100, 125, 100),
    #         ]

    #         for lower, upper, value in spacing_threshhold:
    #             if lower <= min_shear_spacing < upper:
    #                 self.shear_spacing.append(value)
    #                 self.shear_spacing = list(
    #                     set(
    #                         spacing
    #                         for spacing in self.shear_spacing
    #                         if spacing <= value
    #                     )
    #                 )
    #                 break
    #             else:
    #                 self.shear_spacing.append(min_shear_spacing)
    #                 self.shear_spacing = list(
    #                     set(
    #                         spacing
    #                         for spacing in self.shear_spacing
    #                         if spacing <= value
    #                     )
    #                 )

    #         for lower, upper, value in spacing_threshhold:
    #             if lower <= min_shear_center_spacing < upper:
    #                 self.shear_center_spacing.append(value)
    #                 self.shear_center_spacing = list(
    #                     set(
    #                         spacing
    #                         for spacing in self.shear_center_spacing
    #                         if spacing <= value
    #                     )
    #                 )
    #                 break
    #             else:
    #                 self.shear_center_spacing.append(min_shear_center_spacing)
    #                 self.shear_center_spacing = list(
    #                     set(
    #                         spacing
    #                         for spacing in self.shear_center_spacing
    #                         if spacing <= value
    #                     )
    #                 )
    #         self.shear_spacing.sort(reverse=True)
    #         self.shear_center_spacing.sort(reverse=True)
