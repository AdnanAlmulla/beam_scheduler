"""Beam Processing and Design Module.

This module provides functionality for processing beam parameters, designing
beams, and generating a beam schedule dataframe. It utilizes various
beam-related modules to create, design, and display beam instances.

The main function, process_data, takes beam parameters as input and returns a
pandas DataFrame containing the designed beams and their attributes.

Modules:
    beam: Defines the Beam class.
    beam_design: Provides beam design calculations.
    beam_display: Handles the display of beam information.
    beam_mapping: Maps beam attributes to the schedule.
    beam_table: Generates the initial beam schedule table.

Dependencies:
    pandas: Used for creating and manipulating DataFrames.
"""

from typing import Any

import beam
import beam_design
import beam_display
import beam_mapping
import beam_table
import pandas as pd


def process_data(beam_parameters: list[list[Any]]) -> pd.DataFrame:
    """Take the beam instances, design them, and populate dataframe.

    Args:
        beam_parameters(list[beam.Beam]): The beam instances in a list.

    Returns:
        pd.DataFrame: Dataframe containing all designed beams and their
        attributes.
    """

    def create_beam_instances(data: list[list[Any]]) -> list[beam.Beam]:
        return [beam.Beam(*args) for args in zip(*data)]

    beam_instances = create_beam_instances(beam_parameters)
    # List to hold all the designed beams.
    designed_beams = []
    # Loop through beam instances and undertake beam design.
    for beams in beam_instances:
        # Instantiate the Beam Design object.
        beam_design_instance = beam_design.BeamDesign(beams)
        # Undertake the process of flexural design.
        beam_design_instance.calculate_flexural_design()
        # Undertake the process of shear design.
        beam_design_instance.calculate_shear_design()
        # Undertake the process of sideface design.
        beam_design_instance.calculate_sideface_design()
        # Append all the designed beams to the designed beams list.
        designed_beams.append(beam_design_instance)
    # Take the designed beams and initialise beam display object.
    beam_output = [
        beam_display.BeamDisplayer(designed_beam)
        for designed_beam in designed_beams
    ]

    # Get the empty beam schedule df
    beam_schedule_df = beam_table.get_beam_table()
    # Map the attributes of the beam display object to beam schedule.
    beam_schedule_df = beam_mapping.map_beam_attributes(
        beam_output, beam_schedule_df
    )

    return beam_schedule_df
