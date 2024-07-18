from Beam import Beam
from Flexure import Flexure


class BeamDesign:
    """This class inherits all objects relating to Beam and undertakes the necessary design steps.
    This class holds multiple objects with their own attributes. To access their attributes, invoke
    the relevant object explicitly."""

    def __init__(self, beam: Beam):
        self.beam = beam
        self.flexural_design: object = None
        self.shear_design: object = None
        self.sideface_desgin: object = None

    def calculate_flexural_design(self):
        """This method undertakes the flexural design."""
        # First instantiate the flexure object.
        self.flexural_design = Flexure(self.beam)
        # Get the longitudinal rebar count.
        self.flexural_design.get_long_count()
        # Split the torsion reinforcement to the top and bottom rebar if the depth <= 700mm.
        self.flexural_design.flex_torsion_splitting()
        # Obtain the required top and bottom flexural reinforcement.
        self.flexural_design.get_flex_rebar()
