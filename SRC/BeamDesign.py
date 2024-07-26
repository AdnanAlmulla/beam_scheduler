import Beam
import Flexure
import Shear


class BeamDesign:
    """This class inherits all objects relating to Beam and undertakes the necessary design steps.
    This class holds multiple objects with their own attributes. To access their attributes, invoke
    the relevant object explicitly."""

    def __init__(self, beam: Beam):
        self.beam = beam
        self.flexural_design: object = None
        self.shear_design: object = None
        self.sideface_desgin: object = None

    def __repr__(self):
        return f"{self.beam}"

    def calculate_flexural_design(self):
        """This method undertakes the flexural design."""
        # First instantiate the flexure object.
        self.flexural_design = Flexure.Flexure(self.beam)
        # Get the longitudinal rebar count.
        self.flexural_design.get_long_count()
        # Split the torsion reinforcement to the top and bottom rebar if the depth <= 700mm.
        self.flexural_design.flex_torsion_splitting()
        # Obtain the required top and bottom flexural reinforcement.
        self.flexural_design.get_flex_rebar()
        # Check if the calculated rebar is feasible and alter it if not.abs
        self.flexural_design.assess_feasibility()
        # Calculate the residual rebar obtained from the provided rebar.
        self.flexural_design.get_residual_rebar()

    def calculate_shear_design(self):
        """This method undertakes the shear design."""
        # First instantiate the shear object.
        self.shear_design = Shear.Shear(self.beam, self.flexural_design)
        # Calculate the required shear links count.
        self.shear_design.get_shear_links_count()
        # Assess if transverse shear spacing needs to be checked.
        self.shear_design.assess_transverse_shear_spacing()
        # Get the total required shear reinforcement.
        self.shear_design.get_total_shear_req()
        # self.shear_design.get_min_shear_spacing()
