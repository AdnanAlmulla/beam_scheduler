"""Beam design module for reinforced concrete beams.

This module provides a BeamDesign class that encapsulates the design procedures
for reinforced concrete beams. It handles flexural, shear, and sideface
reinforcement calculations based on given beam properties and design
requirements.

The module integrates with other components (beam, flexure, shear, and sideface)
to perform comprehensive beam design calculations.

Classes:
    BeamDesign: Main class for performing beam design calculations.

Typical usage example:
    beam_data = beam.Beam(...)  # Create a Beam object with necessary properties
    design = BeamDesign(beam_data)
    design.calculate_flexural_design()
    design.calculate_shear_design()
    design.calculate_sideface_design()
"""

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

    def calculate_flexural_design(self) -> None:
        """Undertake flexural design.

        The order of operations for calculating the flexural rebar are as
        follows:
        1) The longitudinal rebar count is calculated based on the width (n-1)
        2) The flexural torsion requirement is split to the top and bottom
        flexural requirement if the depth is <= 700mm.
        3) The optimal flexural rebar schedule is derived.
        4) The flexural rebar feasibility is assessed based on span.
        5) The residual flexural rebar is derived to subtract from sideface
        requirements.
        """
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

    def calculate_shear_design(self) -> None:
        """Undertake shear design.

        The order of operations for calculating shear links are as
        follows:
        1) The shear links count is calculated based on the allowable transverse
        shear spacing.
        2) A check is made to assess if the transverse shear spacing needs to be
        assessed based on codal requirements.
        3) Total shear requirement is calculated based on codal requirements.
        4) The minimum longitudinal shear spacing is obtained based on codal
        requirements.
        5) The optimal shear links schedule is obtained.
        """
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
        """Undertake sideface design.

        The order of operations for calculating sideface rebar are as follows:
        1) The flexural torsion requirement is derived by subtracting the
        requirement by the flexural residual.
        2) The sideface clear space is calculated based on the maximum provided
        flexural and shear diameters.
        3) The optimal sideface schedule is obtained.
        """
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
