from Beam import Beam
from typing import List


class Flexure:
    """This class inherits Beam objects and provides new attributes relating to flexural design."""

    def __init__(self, beam: Beam):
        self.beam = beam
        self.flex_rebar_count: int = 0
        self.flex_rebar_dia: List[int] = [16, 20, 25, 32]
        self.top_flex_rebar: dict = {
            "left": {
                "rebar_text": "",
                "provided_reinf": 0,
                "diameter": [],
                "solved": False,
            },
            "middle": {
                "rebar_text": "",
                "provided_reinf": 0,
                "diameter": [],
                "solved": False,
            },
            "right": {
                "rebar_text": "",
                "provided_reinf": 0,
                "diameter": [],
                "solved": False,
            },
        }
        self.bot_flex_rebar: dict = {
            "left": {
                "rebar_text": "",
                "provided_reinf": 0,
                "diameter": [],
                "solved": False,
            },
            "middle": {
                "rebar_text": "",
                "provided_reinf": 0,
                "diameter": [],
                "solved": False,
            },
            "right": {
                "rebar_text": "",
                "provided_reinf": 0,
                "diameter": [],
                "solved": False,
            },
        }

    def get_long_count(self):
        """This method takes a defined instance and calculates the required longitudinal rebar count based on its width."""
        self.flex_rebar_count = self.beam.width // 100
        if self.flex_rebar_count > 2:
            self.flex_rebar_count = self.flex_rebar_count - 1
        else:
            self.flex_rebar_count = 2

    def flex_torsion_splitting(self):
        """This method splits the longitudinal torsional reinforcement requirement between the top and bottom
        reinforcement requirements if the depth of the beam <= 700mm. It then modifies the Beam objects
        longitudinal torsion reinforcement requirements to 0."""
        if True not in self.beam.flex_overstressed and self.beam.depth <= 700:
            divided_torsion_list = [i / 2 for i in self.beam.req_torsion_flex_reinf]
            self.beam.req_top_flex_reinf = [
                a + b
                for a, b in zip(divided_torsion_list, self.beam.req_top_flex_reinf)
            ]
            self.beam.req_bot_flex_reinf = [
                a + b
                for a, b in zip(divided_torsion_list, self.beam.req_bot_flex_reinf)
            ]
            self.beam.req_torsion_flex_reinf = [0, 0, 0]

    def __find_rebar_configuration(self, requirement: int) -> dict:
        """This method finds the required rebar configuration for flexural design.

        Args:
            requirement (int): The required rebar area (mm^2)

        Returns:
            dict: A dictionary containing the rebar text, provided reinforcement area, diameter of each layer,
            and whether the beam was solved or not.
        """
        for diameter_layer1 in self.flex_rebar_dia:
            provided = (
                Beam.provided_reinforcement(diameter_layer1) * self.flex_rebar_count
            )
            if provided > requirement:
                return {
                    "rebar_text": f"{self.flex_rebar_count}T{diameter_layer1}",
                    "provided_reinf": provided,
                    "diameter": [diameter_layer1],
                    "solved": True,
                }
        for diameter_layer2 in self.flex_rebar_dia:
            for diameter_layer1 in self.flex_rebar_dia:
                provided = (
                    Beam.provided_reinforcement(diameter_layer1) * self.flex_rebar_count
                ) + (
                    Beam.provided_reinforcement(diameter_layer2) * self.flex_rebar_count
                )
                if provided > requirement:
                    return {
                        "rebar_text": f"{self.flex_rebar_count}T{diameter_layer1} + {self.flex_rebar_count}T{diameter_layer2}",
                        "provided_reinf": provided,
                        "diameter": [diameter_layer1, diameter_layer2],
                        "solved": True,
                    }
        return {
            "rebar_text": "Required rebar exceeds two layers. Please assess.",
            "provided_reinf": 0,
            "diameter": [],
            "solved": False,
        }

    def get_top_flex_rebar(self):
        """This method loops through the required top flexural reinforcement and provides the string,
        provided area of reinforcement, and diameter for each part of the beam."""
        locations = ["left", "middle", "right"]
        # Index 0 of this list is positive flexure, index 1 is negative flexure.
        for index, (location, requirement) in enumerate(
            zip(locations, self.beam.req_top_flex_reinf)
        ):
            if self.beam.flex_overstressed[1] is True:
                self.top_flex_rebar[location]["rebar_text"] = "Overstressed"
            else:
                result = self.__find_rebar_configuration(requirement)
                self.top_flex_rebar[location]["rebar_text"] = result["rebar_text"]
                self.top_flex_rebar[location]["provided_reinf"] = result[
                    "provided_reinf"
                ]
                self.top_flex_rebar[location]["diameter"] = result["diameter"]
                self.top_flex_rebar[location]["solved"] = result["solved"]
