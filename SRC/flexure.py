"""Flexural design module for reinforced concrete beams.

This module provides a Flexure class that handles the calculation and design of
flexural reinforcement for reinforced concrete beams. It works in conjunction
with the beam module to determine optimal rebar configurations for top and
bottom reinforcement, considering torsional requirements and beam geometry.

The module includes methods for calculating longitudinal rebar count, splitting
torsional requirements, determining rebar configurations, assessing feasibility
based on beam span, and calculating residual rebar for sideface reinforcement.

Classes:
    Flexure: Main class for flexural reinforcement calculations and design.

Typical usage example:
    beam_data = beam.Beam(...)  # Create a Beam object
    flexure_design = Flexure(beam_data)
    flexure_design.get_long_count()
    flexure_design.flex_torsion_splitting()
    flexure_design.get_flex_rebar()
    flexure_design.assess_feasibility()
    flexure_design.get_residual_rebar()
"""

import itertools

import beam


class Flexure:
    """Encapsulates attributes and methods related to the flexure of a beam.

    The Flexure class is responsible for holding information about the flexural
    reinforcement in a beam. It includes attributes for the number and diameter
    of flexural rebars, as well as detailed information about the top and
    bottom flexural reinforcement at different sections (left, middle, right) of
    the beam.

    Attributes:
        beam (beam): The beam object that the flexural attributes belong to.
        flex_rebar_count (int): The count of flexural reinforcement bars.
        flex_rebar_dia (List[int]): List of diameters for flexural rebars.
        top_flex_rebar (dict): Dictionary containing the top flex reinforcement
            in the left, middle, and right sections of the beam.
        bot_flex_rebar (dict): Dictionary containing the bot flex reinforcement
            in the left, middle, and right sections of the beam.
        residual_rebar (dict): Dictionary containing the count of residual
            rebars in the left, middle, and right sections of the beam.
    """

    def __init__(self, beam: beam.Beam) -> None:
        """Initialises the flexural object and inherits the beam dataclass.

        Args:
            beam (beam): Beam dataclass object.
        """
        self.beam = beam
        self.flex_rebar_count: int = 0
        self.flex_rebar_dia: list[int] = [16, 20, 25, 32]
        self.top_flex_rebar: dict = {
            "left": {
                "rebar_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": [],
                "solved": False,
            },
            "middle": {
                "rebar_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": [],
                "solved": False,
            },
            "right": {
                "rebar_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": [],
                "solved": False,
            },
        }
        self.bot_flex_rebar: dict = {
            "left": {
                "rebar_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": [],
                "solved": False,
            },
            "middle": {
                "rebar_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": [],
                "solved": False,
            },
            "right": {
                "rebar_text": "",
                "provided_reinf": 0,
                "utilization": "-",
                "diameter": [],
                "solved": False,
            },
        }
        self.residual_rebar: dict = {"left": 0, "middle": 0, "right": 0}

    def __repr__(self) -> str:
        """String representation of flexure object.

        Returns:
            str: Flexure object string.
        """
        return f"""Longitudinal rebar count: {self.flex_rebar_count}, 
Top flexural rebar: {self.top_flex_rebar}, 
Bottom flexural rebar: {self.bot_flex_rebar}, 
Residual flexural rebar: {self.residual_rebar}"""

    def get_long_count(self) -> None:
        """Calculate the longitudinal rebar count based on beam width."""
        self.flex_rebar_count = self.beam.width // 100
        if self.flex_rebar_count > 2:
            self.flex_rebar_count = self.flex_rebar_count - 1
        else:
            self.flex_rebar_count = 2

    def flex_torsion_splitting(self) -> None:
        """Split flexural torsion requirement based on beam depth.

        Splits the longitudinal torsional reinforcement requirement between the
        top and bottom if the depth of the beam <= 700mm. It then modifies the
        Beam objects longitudinal torsion reinforcement requirements to 0.
        """
        if True not in self.beam.flex_overstressed and self.beam.depth <= 700:
            divided_torsion_list = [
                flex_torsion_area / 2
                for flex_torsion_area in self.beam.req_torsion_flex_reinf
            ]
            self.beam.req_top_flex_reinf = [  # pyright: ignore reportAttributeAccessIssue
                divided_flex_tor_area + top_flex_area
                for divided_flex_tor_area, top_flex_area in zip(
                    divided_torsion_list, self.beam.req_top_flex_reinf
                )
            ]
            self.beam.req_bot_flex_reinf = [  # pyright: ignore reportAttributeAccessIssue
                divided_flex_tor_area + bot_flex_area
                for divided_flex_tor_area, bot_flex_area in zip(
                    divided_torsion_list, self.beam.req_bot_flex_reinf
                )
            ]
            self.beam.req_torsion_flex_reinf = [0, 0, 0]

    def get_flex_rebar(self) -> None:
        """Solve for the flexural rebar.

        Takes the flexural object and modifies the top and bottom
        flexural attributes to signify whether the object has been
        solved or not. Utilises find_rebar_configuration private
        method to find the optimal rebar configuration.
        """
        locations = ["left", "middle", "right"]
        # Loop and obtain the top flexural rebar:
        for location, requirement in zip(
            locations, self.beam.req_top_flex_reinf
        ):
            # Index 0 is positive flexure, index 1 is negative flexure.
            if any(self.beam.flex_overstressed):
                self.top_flex_rebar[location]["rebar_text"] = "Overstressed"
            else:
                result = self._find_rebar_configuration(requirement)
                self.top_flex_rebar[location] = {
                    "rebar_text": result["rebar_text"],
                    "provided_reinf": result["provided_reinf"],
                    "utilization": result["utilization"],
                    "diameter": result["diameter"],
                    "solved": result["solved"],
                }

        # Loop and obtain the bottom flexural rebar:
        for location, requirement in zip(
            locations, self.beam.req_bot_flex_reinf
        ):
            # Index 0 is positive flexure, index 1 is negative flexure.
            if any(self.beam.flex_overstressed):
                self.bot_flex_rebar[location]["rebar_text"] = "Overstressed"
            else:
                result = self._find_rebar_configuration(requirement)
                self.bot_flex_rebar[location] = {
                    "rebar_text": result["rebar_text"],
                    "provided_reinf": result["provided_reinf"],
                    "utilization": result["utilization"],
                    "diameter": result["diameter"],
                    "solved": result["solved"],
                }
        if any(
            self.top_flex_rebar[location]["rebar_text"]
            == "Required rebar exceeds two layers. Please assess."
            for location in self.top_flex_rebar
        ) or any(
            self.bot_flex_rebar[location]["rebar_text"]
            == "Required rebar exceeds two layers. Please assess."
            for location in self.bot_flex_rebar
        ):
            self.beam.flex_overstressed.append(True)

    def _find_rebar_configuration(self, requirement: int) -> dict:
        """Find the optimal rebar configuration for the required rebar area.

        Args:
            requirement (int): The required rebar area (mm^2)

        Returns:
            dict: Returns the rebar text, provided reinforcement area, diameter
            of each layer, and whether the beam object was solved or not.
        """
        best_combination = None
        min_excess_area = float("inf")
        # Consider all combinations of one and two layers
        all_combinations = [
            (diameter,) for diameter in self.flex_rebar_dia
        ] + list(itertools.product(self.flex_rebar_dia, repeat=2))
        for combination in all_combinations:
            provided = sum(
                beam.provided_reinforcement(diameter) * self.flex_rebar_count
                for diameter in combination
            )
            if provided >= requirement:
                excess_area = provided - requirement
                if excess_area < min_excess_area:
                    min_excess_area = excess_area
                    best_combination = combination

        if best_combination:
            sorted_combination = sorted(best_combination, reverse=True)
            rebar_text = " + ".join(
                f"{self.flex_rebar_count}T{diameter}"
                for diameter in sorted_combination
            )
            provided = sum(
                beam.provided_reinforcement(diameter) * self.flex_rebar_count
                for diameter in sorted_combination
            )
            utilization = requirement / provided
            return {
                "rebar_text": rebar_text,
                "provided_reinf": round(provided),
                "utilization": round(utilization * 100, 1),
                "diameter": sorted_combination,
                "solved": True,
            }
        return {
            "rebar_text": "Required rebar exceeds two layers. Please assess.",
            "provided_reinf": 0,
            "utilization": "-",
            "diameter": [float("inf")],
            "solved": False,
        }

    def assess_feasibility(self) -> None:
        """Determine the feasibility of flexure schedule based on beam span.

        This method determines the feasibility of the beam flexural rebar based
        on its span. Beams with a span of 3 metres or less will have its
        reinforcement continous based on the highest provided value.
        """
        # Process top flexural reinforcement:
        largest_area_provided = float("-inf")
        selected_combination = None
        # Index 0 of this list is positive flexure, index 1 is negative flexure.
        if (
            self.beam.flex_overstressed[1] is not True
            and self.beam.span <= 3000
        ):
            for location, properties in self.top_flex_rebar.items():
                if (
                    properties["solved"]
                    and properties["provided_reinf"] > largest_area_provided
                ):
                    largest_area_provided = properties["provided_reinf"]
                    selected_combination = location
            for location, properties in self.top_flex_rebar.items():
                if properties["solved"]:
                    self.top_flex_rebar[location] = self.top_flex_rebar[
                        selected_combination
                    ]

        # Process bottom flexural reinforcement:
        # Reset largest_area_provided and selected_combination for bottom
        # reinforcement
        largest_area_provided = float("-inf")
        selected_combination = None
        # Index 0 of this list is positive flexure, index 1 is negative flexure.
        if (
            self.beam.flex_overstressed[0] is not True
            and self.beam.span <= 3000
        ):
            for location, properties in self.bot_flex_rebar.items():
                if (
                    properties["solved"]
                    and properties["provided_reinf"] > largest_area_provided
                ):
                    largest_area_provided = properties["provided_reinf"]
                    selected_combination = location
            for location, properties in self.bot_flex_rebar.items():
                if properties["solved"]:
                    self.bot_flex_rebar[location] = self.bot_flex_rebar[
                        selected_combination
                    ]

    def get_residual_rebar(self) -> None:
        """Calculate the residual rebar for sideface reinforcement.

        This method takes the obtained flexural rebar area in both the top and
        bottom and subtracts them by their relevant required area.
        It then adds the remaining top and bottom residual together.
        """
        if self.beam.depth > 700 and True not in self.beam.flex_overstressed:
            for index, location in enumerate(self.residual_rebar):
                top_residual = (
                    self.top_flex_rebar[location]["provided_reinf"]
                    - self.beam.req_top_flex_reinf[index]
                    if self.top_flex_rebar[location]["solved"]
                    else 0
                )
                bot_residual = (
                    self.bot_flex_rebar[location]["provided_reinf"]
                    - self.beam.req_bot_flex_reinf[index]
                    if self.bot_flex_rebar[location]["solved"]
                    else 0
                )
                self.residual_rebar[location] = top_residual + bot_residual
