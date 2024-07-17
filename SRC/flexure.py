from Beam import Beam
from dataclasses import field
from typing import List


class Flexure:
    """This class inherits Beam objects and provides new attributes relating to flexural design."""

    def __init__(self, beam: Beam):
        self.beam = beam
        self.flex_rebar_count: int = 0
        self.flex_rebar_dia: List[int] = field(default_factory=lambda: [16, 20, 25, 32])
        self.top_flex_rebar: dict = field(
            default_factory=lambda: {
                "left": {"rebar_text": "", "provided_reinf": 0},
                "middle": {"rebar_text": "", "provided_reinf": 0},
                "right": {"rebar_text": "", "provided_reinf": 0},
            }
        )
        self.bot_flex_rebar: dict = field(
            default_factory=lambda: {
                "left": {"rebar_text": "", "provided_reinf": 0},
                "middle": {"rebar_text": "", "provided_reinf": 0},
                "right": {"rebar_text": "", "provided_reinf": 0},
            }
        )
        self.top_dia: dict = field(
            default_factory=lambda: {
                "left": {
                    "diameter_layer1": 0,
                },
                "middle": {
                    "diameter_layer1": 0,
                },
                "right": {
                    "diameter_layer1": 0,
                },
            }
        )
        self.bot_dia: dict = field(
            default_factory=lambda: {
                "left": {
                    "diameter_layer1": 0,
                },
                "middle": {
                    "diameter_layer1": 0,
                },
                "right": {
                    "diameter_layer1": 0,
                },
            }
        )

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

    def get_top_flex_rebar(self):
        """This method loops through the required top flexural reinforcement and provides the string
        and provided area of reinforcement for each part of the beam."""
        # Index 0 of this list is positive flexure, index 1 is negative flexure.
        if self.beam.flex_overstressed[1] is not True:
            for index, requirement in enumerate(self.beam.req_top_flex_reinf):
                found = False
                for diameter_layer1 in self.flex_rebar_dia:
                    if (
                        (Beam.provided_reinforcement(diameter_layer1))
                        * self.flex_rebar_count
                    ) > requirement:
                        target[index] = f"{self.flex_rebar_count}T{diameter_layer1}"
                        found = True
                        # Assign the computed diameter to the appropriate attributes immediately after determining them
                        if index == 0:
                            self.flex_top_left_dia = diameter_layer1
                        elif index == 1:
                            self.flex_top_middle_dia = diameter_layer1
                        elif index == 2:
                            self.flex_top_right_dia = diameter_layer1
                        break
                if not found:
                    for diameter_layer2 in self.flex_rebar_dia:
                        for diameter_layer1 in self.flex_rebar_dia:
                            if (
                                (Beam.provided_reinforcement(diameter_layer1))
                                * self.flex_rebar_count
                                + (Beam.provided_reinforcement(diameter_layer2))
                                * self.flex_rebar_count
                            ) > requirement:
                                target[index] = (
                                    f"{self.flex_rebar_count}T{diameter_layer1} + {self.flex_rebar_count}T{diameter_layer2}"
                                )
                                found = True
                                # Assign the computed diameters to the appropriate attributes immediately after determining them
                                if index == 0:
                                    self.flex_top_left_dia = diameter_layer1
                                    self.flex_top_left_dia_two = diameter_layer2
                                elif index == 1:
                                    self.flex_top_middle_dia = diameter_layer1
                                    self.flex_top_middle_dia_two = diameter_layer2
                                elif index == 2:
                                    self.flex_top_right_dia = diameter_layer1
                                    self.flex_top_right_dia_two = diameter_layer2
                                break
                        if found:
                            break
                if not found:
                    target[index] = "Increase rebar count or re-assess"
        else:
            target = ["Overstressed"] * len(target)
        self.flex_top_left_rebar_string = target[0]
        self.flex_top_middle_rebar_string = target[1]
        self.flex_top_right_rebar_string = target[2]
