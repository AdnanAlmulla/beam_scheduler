"""Holds the beam design class.

This module contains the Beam
"""
# TODO: update the module docstring.

import beam
import flexure
import shear
import sideface


class BeamDesign:
    """Inherit the Beam dataclass object and undertake design procedures.

    Attributes:
    flexural_design: Object encompassing flexural schedule attributes.
    shear_design: Object encompassing shear schedule attributes.
    sideface_design: Object encompassing shear schedule attributes.
    """

    def __init__(self, beam: beam) -> None:
        """Initialises the beam design object and inherits the beam dataclass.

        Args:
            beam (beam): Beam dataclass object.
        """
        self.beam = beam
        self.flexural_design: object = None
        self.shear_design: object = None
        self.sideface_design: object = None

    # TODO: update the docstring to reflect the order of operations.
    def calculate_flexural_design(self) -> None:
        """Undertake flexural design."""
        # First instantiate the flexure object.
        self.flexural_design = flexure.Flexure(self.beam)
        # Get the longitudinal rebar count.
        self.flexural_design.get_long_count()
        # Split the torsion reinforcement to the top and bottom rebar
        # if the depth <= 700mm.
        self.flexural_design.flex_torsion_splitting()
        # Obtain the required top and bottom flexural reinforcement.
        self.flexural_design.get_flex_rebar()
        # Check if the calculated rebar is feasible and alter it if not.
        self.flexural_design.assess_feasibility()
        # Calculate the residual rebar obtained from the provided rebar.
        self.flexural_design.get_residual_rebar()

    # TODO: update the docstring to reflect the order of operations.
    def calculate_shear_design(self) -> None:
        """Undertake shear design."""
        # First instantiate the shear object.
        self.shear_design = shear.Shear(self.beam, self.flexural_design)
        # Calculate the required shear links count.
        self.shear_design.get_shear_links_count()
        # Assess if transverse shear spacing needs to be checked.
        self.shear_design.assess_transverse_shear_spacing()
        # Get the total required shear reinforcement.
        self.shear_design.get_total_shear_req()
        # Get the minimum codal longitudinal shear spacing.
        self.shear_design.get_min_shear_spacing()
        # Obtain the shear links reinforcement.
        self.shear_design.get_shear_links()

    def calculate_sideface_design(self) -> None:
        """Undertake sideface design."""
        # First instantiate the sideface object.
        self.sideface_design = sideface.Sideface(
            self.beam, self.flexural_design, self.shear_design
        )
        # Calculate the total required torsion reinforcement after residual.
        self.sideface_design.get_required_reinforcement()
        # Get the sideface clear space.
        self.sideface_design.get_sideface_clear_space()
        # Obtain the sideface reinforcement.
        self.sideface_design.get_sideface_rebar()
