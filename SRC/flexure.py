from beam import Beam


class Flexure:
    """This class inherits Beam objects and provides new attributes relating to flexural design.
    This class focusses on providing flexural and sideface reinforcement."""

    def __init__(self, beam: Beam):
        self.beam = beam
        self.flex_rebar_count: int = 0

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
