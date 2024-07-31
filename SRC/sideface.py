"""Holds the sideface class."""
# TODO: update the module docstring.

import itertools
from typing import List

import beam
import flexure
import shear


class Sideface:
    # TODO: provide further information to class docstring.
    """Holds and encapsulates attributes of a sideface object."""

    def __init__(self, beam: beam, flexure: flexure, shear: shear) -> None:
        """Initialises sideface object and inherits beam and shear/flex objects.

        Args:
            beam (beam): Beam dataclass object.
            flexure (flexure): Flexure object.
            shear (shear): Shear object.
        """
        self.beam = beam
        self.flexure = flexure
        self.shear = shear
        self.sideface_dia: List[int] = [16, 20, 25]
        self.sideface_spacing: List[int] = [250, 200, 150]
        self.sideface_clearspace: int = 0
        self.required_torsion_reinforcement: dict = {
            "left": 0,
            "middle": 0,
            "right": 0,
        }
        self.sideface_rebar: dict = {
            "rebar_text": "-",
            "provided_reinf": 0,
            "diameter": 0,
            "spacing": 0,
            "solved": False,
        }

    # TODO: create __repr__ magic method

    def get_required_reinforcement(self) -> None:
        """Calculate the required flexural torsion reinforcement.

        This method checks the condition of the beam and subsequently subtracts
        the residual flexural rebar from the required flexural torsion area
        to provide the total required flexural torsion reinforcement for beams
        with a depth greater than 700mm.
        """
        #! Do not solve if shear and flexure are overstressed. This is done
        #! as the sideface clear space wouldn't be calcualted as a result.
        if (
            not (
                any(self.beam.flex_overstressed)
                or any(self.beam.shear_overstressed)
            )
            and self.beam.depth > 700
        ):
            for index, location in enumerate(
                self.required_torsion_reinforcement
            ):
                self.required_torsion_reinforcement[location] = (
                    self.beam.req_torsion_flex_reinf[index]
                    - self.flexure.residual_rebar[location]
                )

    def get_sideface_clear_space(self) -> None:
        """Calculate the sideface clear face based on maximum beam diameters.

        This method calculates the side face clear space. It takes the sum
        of all rebar diameters in one location (to account for two layers with
        different diameters which are not necessarily the maximum but result
        in the most reduced sideface clearspace)and subtracts them by the
        effective depth of the beam object.
        """
        #! Do not solve if shear and flexure are overstressed. This is done
        #! as the sideface clear space wouldn't be calcualted as a result.
        if (
            not (
                any(self.beam.flex_overstressed)
                or any(self.beam.shear_overstressed)
            )
            and self.beam.depth > 700
        ):
            # Helper function to return a list of the summed up diameters.
            def grab_dia(rebar_dict: dict) -> list:
                rebar_dia = [0]
                for location in rebar_dict:
                    rebar_dia.append(sum(rebar_dict[location]["diameter"]))
                return rebar_dia

            self.sideface_clearspace = (
                self.beam.eff_depth
                - (
                    2
                    * max(
                        self.shear.shear_links[location]["diameter"]
                        for location in self.shear.shear_links
                    )
                )
                - max(grab_dia(self.flexure.top_flex_rebar))
                - max(grab_dia(self.flexure.bot_flex_rebar))
            )

    def get_sideface_rebar(self) -> None:
        """Obtain the sideface rebar.

        This method calculates the side face reinforcement for beam objects with
        a depth greater than 700mm. It utilises the _find_rebar_configuration
        helper method to obtain the most optimal rebar configuration.
        """
        if (
            not (
                any(self.beam.flex_overstressed)
                or any(self.beam.shear_overstressed)
            )
            and self.beam.depth > 700
        ):
            self.sideface_rebar = self._find_rebar_configuration(
                max(
                    self.required_torsion_reinforcement[location]
                    for location in self.required_torsion_reinforcement
                )
            )

    def _find_rebar_configuration(self, requirement: int) -> dict:
        """Find the optimal sideface configuration for the required rebar area.

        Args:
            requirement (int): The maximum sideface area in the beam (mm^2)

        Returns:
            dict: Returns the rebar text, provided reinforcement area, diameter,
            spacing, and whether the beam object was solved or not.
        """
        best_combination = None
        min_excess_area = float("inf")
        all_combinations = list(
            itertools.product(self.sideface_dia, self.sideface_spacing)
        )
        for diameter, spacing in all_combinations:
            provided = (
                beam.provided_reinforcement(diameter)
                * 2
                * (self.sideface_clearspace / spacing)
            )
            if provided >= requirement:
                excess_area = provided - requirement
                if excess_area < min_excess_area:
                    min_excess_area = excess_area
                    best_combination = {
                        "rebar_text": f"T{diameter}@{spacing}EF",
                        "provided_reinf": round(provided),
                        "diameter": diameter,
                        "spacing": spacing,
                        "solved": True,
                    }
        if best_combination:
            return best_combination
        else:
            best_combination = {
                "rebar_text": "Cannot satisfy requirement. Please reassess.",
                "provided_reinf": 0,
                "diameter": 0,
                "spacing": 0,
                "solved": False,
            }
            return best_combination
