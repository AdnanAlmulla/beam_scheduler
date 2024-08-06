"""Module for mapping beam attributes to a pandas DataFrame.

This module provides functionality to map attributes from BeamDisplayer
instances to a structured DataFrame, facilitating the creation of beam
schedules or reports.
"""

import beam_display
import pandas as pd


def map_beam_attributes(
    beam_instances: list[beam_display.BeamDisplayer], dataframe: pd.DataFrame
) -> pd.DataFrame:
    """Maps attributes from BeamDisplayer instances to a pandas DataFrame.

    This function takes a list of BeamDisplayer instances and a pre-structured
    DataFrame, then populates the DataFrame with the beam attributes. It uses
    a predefined mapping to match beam attributes to DataFrame columns.

    Args:
        beam_instances (list[beam_display.BeamDisplayer]): A list of
        BeamDisplayer instances containing the beam design information.
        dataframe (pd.DataFrame): A pre-structured pandas DataFrame with
        appropriate columns for beam attributes.

    Returns:
        pd.DataFrame: The input DataFrame populated with beam attribute values.

    Note:
        The function assumes that the input DataFrame has a MultiIndex column
        structure that matches the keys in the beam_mapping dictionary.
    """
    beam_mapping = {
        "storey": ("Storey", ""),
        "etabs_id": ("Etabs ID", ""),
        "width": ("Dimensions", "Width (mm)"),
        "depth": ("Dimensions", "Depth (mm)"),
        "span": ("Span (mm)", ""),
        "flex_bot_left_string": ("Bottom Reinforcement", "Left (BL)"),
        "flex_bot_middle_string": ("Bottom Reinforcement", "Middle (B)"),
        "flex_bot_right_string": ("Bottom Reinforcement", "Right (BR)"),
        "flex_top_left_string": ("Top Reinforcement", "Left (TL)"),
        "flex_top_middle_string": ("Top Reinforcement", "Middle (T)"),
        "flex_top_right_string": ("Top Reinforcement", "Right (TR)"),
        "sideface_string": ("Side Face Reinforcement", ""),
        "shear_links_left_string": ("Shear links", "Left (H)"),
        "shear_links_middle_string": ("Shear links", "Middle (J)"),
        "shear_links_right_string": ("Shear links", "Right (K)"),
        "check_transverse_shear_spacing": (
            "Check Transverse Shear Spacing?",
            "",
        ),
        "req_bot_flex_left": ("Flexural BL Criteria", "Required (mm^2)"),
        "prov_bot_flex_left": ("Flexural BL Criteria", "Provided (mm^2)"),
        "util_bot_flex_left": ("Flexural BL Criteria", "Utilization (%)"),
        "req_bot_flex_middle": ("Flexural BM Criteria", "Required (mm^2)"),
        "prov_bot_flex_middle": ("Flexural BM Criteria", "Provided (mm^2)"),
        "util_bot_flex_middle": ("Flexural BM Criteria", "Utilization (%)"),
        "req_bot_flex_right": ("Flexural BR Criteria", "Required (mm^2)"),
        "prov_bot_flex_right": ("Flexural BR Criteria", "Provided (mm^2)"),
        "util_bot_flex_right": ("Flexural BR Criteria", "Utilization (%)"),
        "req_top_flex_left": ("Flexural TL Criteria", "Required (mm^2)"),
        "prov_top_flex_left": ("Flexural TL Criteria", "Provided (mm^2)"),
        "util_top_flex_left": ("Flexural TL Criteria", "Utilization (%)"),
        "req_top_flex_middle": ("Flexural TM Criteria", "Required (mm^2)"),
        "prov_top_flex_middle": ("Flexural TM Criteria", "Provided (mm^2)"),
        "util_top_flex_middle": ("Flexural TM Criteria", "Utilization (%)"),
        "req_top_flex_right": ("Flexural TR Criteria", "Required (mm^2)"),
        "prov_top_flex_right": ("Flexural TR Criteria", "Provided (mm^2)"),
        "util_top_flex_right": ("Flexural TR Criteria", "Utilization (%)"),
        "req_shear_left": ("Shear L Criteria", "Required (mm^2)"),
        "prov_shear_left": ("Shear L Criteria", "Provided (mm^2)"),
        "util_shear_left": ("Shear L Criteria", "Utilization (%)"),
        "req_shear_middle": ("Shear M Criteria", "Required (mm^2)"),
        "prov_shear_middle": ("Shear M Criteria", "Provided (mm^2)"),
        "util_shear_middle": ("Shear M Criteria", "Utilization (%)"),
        "req_shear_right": ("Shear R Criteria", "Required (mm^2)"),
        "prov_shear_right": ("Shear R Criteria", "Provided (mm^2)"),
        "util_shear_right": ("Shear R Criteria", "Utilization (%)"),
    }
    # Loop through all the beam instances and populate the beam schedule
    # dataframe with relevant information.
    for idx, beams in enumerate(beam_instances):
        for attr, col in beam_mapping.items():
            value = getattr(beams, attr)
            if isinstance(value, str):
                dataframe[col] = dataframe[col].astype(object)
            dataframe.loc[idx, col] = value
    return dataframe
