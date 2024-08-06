"""Module for displaying beam design information.

This module provides a class for organizing and displaying the design
details of a beam, including its geometry, reinforcement, and design criteria.
"""

import beam_design


class BeamDisplayer:
    """A class to organize and display beam design information.

    This class takes a BeamDesign object and extracts relevant information
    for display purposes, including beam geometry, reinforcement details,
    and design criteria.
    """

    def __init__(self, designed_beam: beam_design.BeamDesign) -> None:
        """Initialize the BeamDisplayer with a designed beam.

        Args:
            designed_beam (beam_design.BeamDesign): The designed beam object
                containing all the necessary design information.
        """
        self.designed_beam = designed_beam
        self.storey = self.designed_beam.beam.storey
        self.etabs_id = self.designed_beam.beam.etabs_id
        self.width = self.designed_beam.beam.width
        self.depth = self.designed_beam.beam.depth
        self.span = self.designed_beam.beam.span
        self.flex_bot_left_string = (
            self.designed_beam.flexural_design.bot_flex_rebar["left"][
                "rebar_text"
            ]
        )
        self.flex_bot_middle_string = (
            self.designed_beam.flexural_design.bot_flex_rebar["middle"][
                "rebar_text"
            ]
        )
        self.flex_bot_right_string = (
            self.designed_beam.flexural_design.bot_flex_rebar["right"][
                "rebar_text"
            ]
        )
        self.flex_top_left_string = (
            self.designed_beam.flexural_design.top_flex_rebar["left"][
                "rebar_text"
            ]
        )
        self.flex_top_middle_string = (
            self.designed_beam.flexural_design.top_flex_rebar["middle"][
                "rebar_text"
            ]
        )
        self.flex_top_right_string = (
            self.designed_beam.flexural_design.top_flex_rebar["right"][
                "rebar_text"
            ]
        )
        self.sideface_string = (
            self.designed_beam.sideface_design.sideface_rebar["rebar_text"]
        )
        self.shear_links_left_string = (
            self.designed_beam.shear_design.shear_links["left"]["links_text"]
        )
        self.shear_links_middle_string = (
            self.designed_beam.shear_design.shear_links["middle"]["links_text"]
        )
        self.shear_links_right_string = (
            self.designed_beam.shear_design.shear_links["right"]["links_text"]
        )
        self.check_transverse_shear_spacing = (
            self.designed_beam.shear_design.check_transverse_shear_spacing
        )
        self.req_bot_flex_left = self.designed_beam.beam.req_bot_flex_reinf[0]
        self.req_bot_flex_middle = self.designed_beam.beam.req_bot_flex_reinf[1]
        self.req_bot_flex_right = self.designed_beam.beam.req_bot_flex_reinf[2]
        self.req_top_flex_left = self.designed_beam.beam.req_top_flex_reinf[0]
        self.req_top_flex_middle = self.designed_beam.beam.req_top_flex_reinf[1]
        self.req_top_flex_right = self.designed_beam.beam.req_top_flex_reinf[2]
        self.req_shear_left = self.designed_beam.shear_design.total_req_shear[0]
        self.req_shear_middle = self.designed_beam.shear_design.total_req_shear[
            1
        ]
        self.req_shear_right = self.designed_beam.shear_design.total_req_shear[
            2
        ]
        self.prov_bot_flex_left = (
            self.designed_beam.flexural_design.bot_flex_rebar["left"][
                "provided_reinf"
            ]
        )
        self.prov_bot_flex_middle = (
            self.designed_beam.flexural_design.bot_flex_rebar["middle"][
                "provided_reinf"
            ]
        )
        self.prov_bot_flex_right = (
            self.designed_beam.flexural_design.bot_flex_rebar["right"][
                "provided_reinf"
            ]
        )
        self.prov_top_flex_left = (
            self.designed_beam.flexural_design.top_flex_rebar["left"][
                "provided_reinf"
            ]
        )
        self.prov_top_flex_middle = (
            self.designed_beam.flexural_design.top_flex_rebar["middle"][
                "provided_reinf"
            ]
        )
        self.prov_top_flex_right = (
            self.designed_beam.flexural_design.top_flex_rebar["right"][
                "provided_reinf"
            ]
        )
        self.prov_shear_left = self.designed_beam.shear_design.shear_links[
            "left"
        ]["provided_reinf"]
        self.prov_shear_middle = self.designed_beam.shear_design.shear_links[
            "middle"
        ]["provided_reinf"]
        self.prov_shear_right = self.designed_beam.shear_design.shear_links[
            "right"
        ]["provided_reinf"]
        self.util_bot_flex_left = (
            self.designed_beam.flexural_design.bot_flex_rebar["left"][
                "utilization"
            ]
        )
        self.util_bot_flex_middle = (
            self.designed_beam.flexural_design.bot_flex_rebar["middle"][
                "utilization"
            ]
        )
        self.util_bot_flex_right = (
            self.designed_beam.flexural_design.bot_flex_rebar["right"][
                "utilization"
            ]
        )
        self.util_top_flex_left = (
            self.designed_beam.flexural_design.top_flex_rebar["left"][
                "utilization"
            ]
        )
        self.util_top_flex_middle = (
            self.designed_beam.flexural_design.top_flex_rebar["middle"][
                "utilization"
            ]
        )
        self.util_top_flex_right = (
            self.designed_beam.flexural_design.top_flex_rebar["right"][
                "utilization"
            ]
        )
        self.util_shear_left = self.designed_beam.shear_design.shear_links[
            "left"
        ]["utilization"]
        self.util_shear_middle = self.designed_beam.shear_design.shear_links[
            "middle"
        ]["utilization"]
        self.util_shear_right = self.designed_beam.shear_design.shear_links[
            "right"
        ]["utilization"]
