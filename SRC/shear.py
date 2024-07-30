"""Holds the shear class."""
# TODO: update the module docstring.

from typing import List

import beam
import flexure
import numpy as np


class Shear:
    # TODO: provide further information to class docstring.
    """Holds and encapsulates attributes of a shear object."""

    def __init__(self, beam: beam, flexure: flexure) -> None:
        """Initialises shear object and inherits the beam and flexure objects.

        Args:
            beam (beam): Beam dataclass object.
            flexure (flexure): Flexure object.
        """
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

    def __repr__(self) -> str:
        """String representation of shear object.

        Returns:
            str: Shear object string.
        """
        return f"""Total required shear reinforcement: {self.total_req_shear},
Shear links: {self.shear_links}, 
Check transverse shear spacing: {self.check_transverse_shear_spacing}"""

    def get_shear_links_count(self) -> None:
        """Calculate the required shear legs.

        Calculate the required shear legs based on the maximum
        stransverse shear spacing as required in Table 9.7.6.2.2. of ACI 318-19.
        """
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

    def assess_transverse_shear_spacing(self) -> None:
        """Assess whether the transverse shear spacing requires to be checked.

        This method assesses if the required Vs is greater or less than the
        nominal concrete shear capacity as per Table 9.7.6.2.2 of ACI 318.19.
        """
        # Get the maximum shear force from a list of the left, middle,
        # and right section of the beam.
        maximum_shear_force = max(self.beam.shear_force)
        # The maximum shear force is being subtracted by the concrete shear
        # force capacity as found in Table 22.5.5.1 eq (a) of ACI 318-19
        concrete_shear_capacity = (
            0.17
            * np.sqrt(self.beam.comp_conc_grade)
            * self.beam.width
            * self.beam.eff_depth
            * 10**-3
        )
        required_vs = maximum_shear_force - concrete_shear_capacity
        # The nominal shear capacity equation is obtained from
        # Table 9.7.6.2.2 of ACI 318-19.
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

    def get_total_shear_req(self) -> None:
        """Calculate the total required shear area.

        Call the required shear and torsion reinforcement attributes and
        calculate the total shear reinforcement required.
        """
        if True in self.beam.shear_overstressed:
            for properties in self.shear_links.values():
                properties["links_text"] = "Overstressed"
        else:
            self.total_req_shear = [
                round(a + 2 * b)
                for a, b in zip(
                    self.beam.req_shear_reinf, self.beam.req_torsion_reinf
                )
            ]

    def get_min_shear_spacing(self) -> None:
        """Derive the minimum codal longitudinal shear spacing.

        This method follows Clause 18.4.2.4 of ACI 318-19 by ensuring that the
        longitudinal spacing does not exceed its codal maximum for the
        left/right and middle shear links.
        """
        # ! By writing this conditional, an overstressed condition in top or
        # ! bottom reinforcement will not solve for shear reinforcement.
        if True not in (
            self.beam.flex_overstressed,
            self.beam.shear_overstressed,
        ):

            def get_min_diameter(rebar_dict: dict) -> int:
                return min(
                    min(
                        properties["diameter"]
                        for properties in rebar_dict.values()
                    )
                )

            smallest_long_dia = min(
                get_min_diameter(self.flexure.top_flex_rebar),
                get_min_diameter(self.flexure.bot_flex_rebar),
            )
            # Assume worst case diameter for shear as it's not been derived yet.
            smallest_shear_dia = 12
            min_shear_spacing = min(
                [
                    (self.beam.eff_depth / 4),
                    (smallest_long_dia * 8),
                    (smallest_shear_dia * 24),
                    250,
                ]
            )
            min_shear_center_spacing = min([(self.beam.eff_depth / 2), 250])
            spacing_thresholds = [
                (200, 250, 200),
                (150, 200, 150),
                (125, 150, 125),
                (100, 125, 100),
            ]

            def update_spacing(spacing_list: list, min_spacing: int) -> list:
                for lower, upper, value in spacing_thresholds:
                    if lower <= min_spacing < upper:
                        spacing_list.append(value)
                        return [s for s in spacing_list if s <= value]
                spacing_list.append(min_spacing)
                return [s for s in spacing_list if s <= min_spacing]

            self.shear_spacing = update_spacing(
                self.shear_spacing, min_shear_spacing
            )
            self.shear_center_spacing = update_spacing(
                self.shear_center_spacing, min_shear_center_spacing
            )
            self.shear_spacing = list(set(self.shear_spacing))
            self.shear_center_spacing = list(set(self.shear_center_spacing))
            self.shear_spacing.sort(reverse=True)
            self.shear_center_spacing.sort(reverse=True)
