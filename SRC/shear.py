"""Shear design module for reinforced concrete beams.

This module provides a Shear class that handles the calculation and design of
shear reinforcement for reinforced concrete beams. It works in conjunction with
the beam and flexure modules to determine optimal shear link configurations,
considering both shear and torsional requirements.

The module includes methods for calculating shear link counts, assessing
transverse shear spacing requirements, determining total shear reinforcement
needs, calculating minimum shear spacing, and designing shear links.

Classes:
    Shear: Main class for shear reinforcement calculations and design.

Typical usage example:
    beam_data = beam.Beam(...)  # Create a Beam object
    flexure_design = flexure.Flexure(...)  # Create a Flexure object
    shear_design = Shear(beam_data, flexure_design)
    shear_design.get_shear_links_count()
    shear_design.get_total_shear_req()
    shear_design.get_min_shear_spacing()
    shear_design.get_shear_links()
"""

import itertools

import numpy as np

from SRC import beam, flexure


class Shear:
    """Encapsulates attributes and methods related to shear reinforcement.

    The Shear class holds information about the beam shear reinforcement.
    It includes attributes for the diameters and spacing of shear rebars,
    total required shear reinforcement in different sections (left, middle,
    right) of the beam, and detailed information about the provided shear
    reinforcement.

    Attributes:
        beam (beam): The beam object that the shear attributes belong to.
        flexure (flexure): The flexure object related to the beam.
        total_req_shear (List[int]): List of total required shear
        reinforcement for left, middle, and right sections.
        shear_dia (List[int]): List of diameters for shear rebars.
        shear_spacing (List[int]): List of spacing values for shear rebars.
        shear_center_spacing (List[int]): List of center spacing values for
        shear rebars.
        shear_links_count (list): List containing the count of shear links.
        shear_links (dict): Dictionary containing information about the
            provided shear reinforcement in the left, middle, and right
            sections of the beam.
    """

    def __init__(self, beam: beam.Beam, flexure: flexure.Flexure) -> None:
        """Initialises shear object and inherits the beam and flexure objects.

        Args:
            beam (beam): Beam dataclass object.
            flexure (flexure): Flexure object.
        """
        self.beam = beam
        self.flexure = flexure
        self.total_req_shear: list[int] = [0, 0, 0]
        self.shear_dia: list[int] = [12, 16]
        self.shear_spacing: list[int] = [250, 200, 150, 125, 100]
        self.shear_center_spacing: list[int] = [250, 200, 150, 125, 100]
        self.shear_links_count: list = []
        self.shear_links: dict = {
            "left": {
                "links_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            },
            "middle": {
                "links_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            },
            "right": {
                "links_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            },
        }

    def __repr__(self) -> str:
        """String representation of shear object.

        Returns:
            str: Shear object string.
        """
        return f"""Total required shear reinforcement: {self.total_req_shear},
Shear links: {self.shear_links}"""

    def get_shear_links_count(self) -> None:
        """Calculate the required shear legs.

        Calculate the required shear legs based on the maximum
        stransverse shear spacing as required in Table 9.7.6.2.2. of ACI 318-19.
        """
        if True not in self.beam.shear_overstressed:
            max_transverse_spacing = min(
                self._assess_transverse_shear_spacing()
            )
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

    def _assess_transverse_shear_spacing(self) -> list[int | float]:
        """Assess whether the transverse shear spacing requires to be checked.

        This method assesses if the required Vs is greater or less than the
        nominal concrete shear capacity as per Table 9.7.6.2.2 of ACI 318.19.

        Returns:
            list[int | float]: A list containing the effective depth per codal
            requirements and the other minimum value.
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
            return [self.beam.eff_depth, 600]
        else:
            return [(self.beam.eff_depth / 2), 300]

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
        #! By writing this conditional, an overstressed condition in top or
        #! bottom flex reinforcement will not solve for shear reinforcement.
        if (
            not (
                any(self.beam.flex_overstressed)
                or any(self.beam.shear_overstressed)
            )
            and all(
                [
                    self.flexure.top_flex_rebar["left"]["solved"],
                    self.flexure.top_flex_rebar["middle"]["solved"],
                    self.flexure.top_flex_rebar["right"]["solved"],
                ]
            )
            and all(
                [
                    self.flexure.bot_flex_rebar["left"]["solved"],
                    self.flexure.bot_flex_rebar["middle"]["solved"],
                    self.flexure.bot_flex_rebar["right"]["solved"],
                ]
            )
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

            def update_spacing(spacing_list: list, min_spacing: float) -> list:
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

    def get_shear_links(self) -> None:
        """Solve for the shear rebar.

        Takes the shear object and modifies the shear links attributes to
        signify whether the object has been solved or not. Utilises
        find_rebar_configuration private method to find the optimal rebar
        configuration.
        """
        locations = ["left", "middle", "right"]
        #! Flex overstressed is checked as minimum shear spacing is not solved.
        if not (
            any(self.beam.flex_overstressed)
            or any(self.beam.shear_overstressed)
        ):
            for location, requirement, torsion_requirement in zip(
                locations, self.total_req_shear, self.beam.req_torsion_reinf
            ):
                # Solve for left and right shear spacings.
                if location == "left" or location == "right":
                    result = self._find_links_configuration(
                        requirement, torsion_requirement, self.shear_spacing
                    )
                    self.shear_links[location] = {
                        "links_text": result["links_text"],
                        "provided_reinf": result["provided_reinf"],
                        "utilization": result["utilization"],
                        "diameter": result["diameter"],
                        "spacing": result["spacing"],
                        "solved": result["solved"],
                    }
                    # Copy the highest provided to the left or right.
                    self._copy_highest_provided(self.shear_links)
                else:
                    result = self._find_links_configuration(
                        requirement,
                        torsion_requirement,
                        self.shear_center_spacing,
                    )
                    self.shear_links[location] = {
                        "links_text": result["links_text"],
                        "provided_reinf": result["provided_reinf"],
                        "utilization": result["utilization"],
                        "diameter": result["diameter"],
                        "spacing": result["spacing"],
                        "solved": result["solved"],
                    }
        else:
            for location in self.shear_links:
                self.shear_links[location]["links_text"] = "Overstressed"

    def _find_links_configuration(
        self, requirement: int, torsion_requirement: int, spacings: list[int]
    ) -> dict:
        """Find the optimal links configuration for the required rebar area.

        Args:
            requirement (int): The required rebar area (mm^2)
            torsion_requirement(int): The required torsion rebar area (mm^2)
            spacings(list): The required spacing list.

        Returns:
            dict: Returns the link text, provided reinforcement area, diameter,
            spacing, and whether the beam object was solved or not.
        """
        best_combination = None
        min_excess_area = float("inf")
        # Consider all combinations of diameter, spacing, and count.
        all_combinations = list(
            itertools.product(self.shear_dia, self.shear_links_count, spacings)
        )
        for diameter, count, spacing in all_combinations:
            provided = (
                beam.provided_reinforcement(diameter) * count * (1000 / spacing)
            )
            # torsion_provided checks that the outer two layers is
            # satisfactory against torsional shear requirements.
            torsion_provided = (
                beam.provided_reinforcement(diameter) * 2 * (1000 / spacing)
            )
            if (
                provided >= requirement
                and torsion_provided >= torsion_requirement
            ):
                excess_area = provided - requirement
                if excess_area < min_excess_area:
                    min_excess_area = excess_area
                    best_combination = {
                        "links_text": f"{count}L-T{diameter}@{spacing}",
                        "provided_reinf": round(provided),
                        "utilization": round((requirement / provided) * 100, 1),
                        "diameter": diameter,
                        "spacing": spacing,
                        "solved": True,
                    }
        if best_combination:
            return best_combination
        else:
            best_combination = {
                "links_text": "Cannot satisfy requirement. Please reassess",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            }
            return best_combination

    def _copy_highest_provided(self, shear_links: dict) -> dict:
        """Copy the highest reinforcement of either the left or right.

        Args:
            shear_links (dict): The shear links dictionary.

        Returns:
            dict: The updated shear links dictionary with both sides identical.
        """
        left, right = shear_links["left"], shear_links["right"]
        max_side = max([left, right], key=lambda x: x["provided_reinf"])
        min_side = left if max_side == right else right

        min_side.update(max_side)
        return shear_links
