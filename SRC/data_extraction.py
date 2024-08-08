"""Module for extracting beam data from Excel sheets.

This module provides functionality to read beam design data from Excel sheets
and extract various parameters needed for beam analysis and design.
"""

from typing import Any, BinaryIO

import beam
import pandas as pd


def extract_data(excel_file: str | BinaryIO) -> list[list[Any]]:
    """Extracts beam data from an Excel file.

    This function reads beam design data from different sheets of an Excel file
    and processes it to extract various parameters needed for beam analysis and
    design.

    Args:
        excel_file (str): Path to the Excel file containing beam design data.

    Returns:
        list[list[Any]]: A list of lists containing extracted beam parameters.
        Each inner list represents a different parameter for all beams.

    Note:
        The function assumes a specific structure for the Excel file, with three
        sheets containing flexural, shear, and span data respectively.
    """
    # Seperate each sheet into unique dataframes.
    flexural_df = pd.read_excel(excel_file, sheet_name=0, header=1)
    shear_df = pd.read_excel(excel_file, sheet_name=1, header=1)
    span_df = pd.read_excel(excel_file, sheet_name=2, header=1)

    # Remove the first row of each dataframes.
    flexural_df = flexural_df.drop([0])
    shear_df = shear_df.drop([0])
    span_df = span_df.drop([0])

    def get_stories(dataframe: pd.DataFrame) -> list[str]:
        """Get the storey definitions for each beam.

        Args:
            dataframe (pd.DataFrame): Dataframe to get stories from.

        Returns:
            list[int]: List of stories for each beam.
        """
        return dataframe["Story"].tolist()

    def get_etabs_ids(dataframe: pd.DataFrame) -> list[str]:
        """Get the etabs ids for each beam.

        Args:
            dataframe (pd.DataFrame): Dataframe to get etabs ids from.

        Returns:
            list[str]: List of etabs ids for each beam.
        """
        return dataframe["Label"].tolist()

    def get_width(dataframe: pd.DataFrame) -> list[int]:
        """Get the width of the beam section.

        Args:
            dataframe (pd.DataFrame): Dataframe to get section from.

        Returns:
            list[int]: List of beam widths.
        """
        return [
            beam.get_width(sections) for sections in dataframe["Section"][::3]
        ]

    def get_depth(dataframe: pd.DataFrame) -> list[int]:
        """Get the depth of the beam section.

        Args:
            dataframe (pd.DataFrame): Dataframe to get section definition from.

        Returns:
            list[int]: List of beam depths.
        """
        return [
            beam.get_depth(sections) for sections in dataframe["Section"][::3]
        ]

    def get_span(dataframe: pd.DataFrame) -> list[int]:
        """Get the span for each beam section.

        Args:
            dataframe (pd.DataFrame): Dataframe to get span from.

        Returns:
            list[int]: List of spans for each beam.
        """
        spans = dataframe["Length"].tolist()
        return [round(span * 1000) for span in spans]

    def get_conc_grade(dataframe: pd.DataFrame) -> list[int]:
        """Get the concrete compressive grade, fc'.

        Args:
            dataframe (pd.DataFrame): Dataframe to get section definition from.

        Returns:
            list[int]: List of beam concrete compressive grades.
        """
        return [
            beam.get_comp_conc_grade(sections)
            for sections in dataframe["Section"][::3]
        ]

    def get_flexural_combo(dataframe: pd.DataFrame) -> list[list[bool]]:
        """Get the flexural combination condition for each beam.

        Args:
            dataframe (pd.DataFrame): Dataframe to get combination from.

        Returns:
            list[list[bool]]: Nested list containing booleans [pos, neg].
        """
        # Take each beam's flexural combo and put it in a list within a list.
        pos_combo_list = dataframe["+ve Moment Combo"].tolist()
        nested_pos_combo_list = [
            pos_combo_list[i : i + 3] for i in range(0, len(pos_combo_list), 3)
        ]
        neg_combo_list = dataframe["-ve Moment Combo"].tolist()
        nested_neg_combo_list = [
            neg_combo_list[i : i + 3] for i in range(0, len(neg_combo_list), 3)
        ]
        # Return True if any of the combos in the list are overstressed.
        checked_pos_combo_list = [
            bool(
                any(
                    str(element).strip().lower() in ["o/s", "nan"]
                    for element in sublist
                )
            )
            for sublist in nested_pos_combo_list
        ]
        checked_neg_combo_list = [
            bool(
                any(
                    str(element).strip().lower() in ["o/s", "nan"]
                    for element in sublist
                )
            )
            for sublist in nested_neg_combo_list
        ]
        # Zip the positive and negative combos together. Index 0 is positive and
        # Index 1 is negative.
        return [
            [pos, neg]
            for pos, neg in zip(checked_pos_combo_list, checked_neg_combo_list)
        ]

    def get_top_flex_area(dataframe: pd.DataFrame) -> list[list[int]]:
        """Get the top required area of reinforcement.

        Args:
            dataframe (pd.DataFrame): Dataframe to get area of reinforcement.

        Returns:
            list[list[int]]: Nested list containing area of top reinforcement:
            [left, middle, right]
        """
        top_flex_reinf_needed = dataframe["As Top"].tolist()
        return [
            top_flex_reinf_needed[i : i + 3]
            for i in range(0, len(top_flex_reinf_needed), 3)
        ]

    def get_bot_flex_area(dataframe: pd.DataFrame) -> list[list[int]]:
        """Get the bottom required area of reinforcement.

        Args:
            dataframe (pd.DataFrame): Dataframe to get area of reinforcement.

        Returns:
            list[list[int]]: List containing area of bottom reinforcement:
            [left, middle, right]
        """
        bot_flex_reinf_needed = dataframe["As Bot"].tolist()
        return [
            bot_flex_reinf_needed[i : i + 3]
            for i in range(0, len(bot_flex_reinf_needed), 3)
        ]

    def get_flex_torsion_area(dataframe: pd.DataFrame) -> list[list[int]]:
        """Get the required flexural torsion area of reinforcement.

        Args:
            dataframe (pd.DataFrame): Dataframe to get area of flextorsion from.

        Returns:
            list[list[int]]: Nested list containing area of flexural torsion:
            [left, middle, right]
        """
        flex_torsion_reinf_needed = dataframe["TLngRebar (Al)"].tolist()
        return [
            flex_torsion_reinf_needed[i : i + 3]
            for i in range(0, len(flex_torsion_reinf_needed), 3)
        ]

    def get_shear_force(dataframe: pd.DataFrame) -> list[list[int]]:
        """Get the shear force of each beam.

        Args:
            dataframe (pd.DataFrame): Dataframe to get shear force from.

        Returns:
            list[list[int]]: Nested list cotaining shear force:
            [left, middle, right]
        """
        shear_force_list = dataframe["Shear Force"].tolist()
        return [
            shear_force_list[i : i + 3]
            for i in range(0, len(shear_force_list), 3)
        ]

    def get_shear_combo(dataframe: pd.DataFrame) -> list[list[bool]]:
        """Get the shear combination condition for each beam.

        Args:
            dataframe (pd.DataFrame): Dataframe to get combination from.

        Returns:
            list[list[bool]]: Nested list containing booleans [shear, torsion].
        """
        shear_combo_list = dataframe["Shear Design Combo"].tolist()
        nested_shear_combo = [
            shear_combo_list[i : i + 3]
            for i in range(0, len(shear_combo_list), 3)
        ]
        # Take the nested list and return OK or OS as a string in a list.
        checked_shear_combo = [
            bool(
                any(
                    str(element).strip().lower() in ["o/s", "nan"]
                    for element in sublist
                )
            )
            for sublist in nested_shear_combo
        ]
        # Repeat the same as shear combo, except for torsion combo.
        torsion_combo_list = dataframe["TTrnCombo"].tolist()
        nested_torsion_combo = [
            torsion_combo_list[i : i + 3]
            for i in range(0, len(torsion_combo_list), 3)
        ]
        checked_torsion_combo = [
            bool(
                any(
                    str(element).strip().lower() in ["o/s", "nan"]
                    for element in sublist
                )
            )
            for sublist in nested_torsion_combo
        ]
        return [
            [shear, torsion]
            for shear, torsion in zip(
                checked_shear_combo, checked_torsion_combo
            )
        ]

    def get_shear_area(dataframe: pd.DataFrame) -> list[list[int]]:
        """Get the shear required area of reinforcement.

        Args:
            dataframe (pd.DataFrame): Dataframe to get area of reinforcement.

        Returns:
            list[list[int]]: Nested list containing shear area of reinforcement:
            [left, middle, right]
        """
        shear_reinf_needed = dataframe["VRebar (Av/s)"].tolist()
        return [
            shear_reinf_needed[i : i + 3]
            for i in range(0, len(shear_reinf_needed), 3)
        ]

    def get_torsion_area(dataframe: pd.DataFrame) -> list[list[int]]:
        """Get the torsion required area of reinforcement.

        Args:
            dataframe (pd.DataFrame): Dataframe to get area of reinforcement.

        Returns:
            list[list[int]]: List containing torsion area of reinforcement:
            [left, middle, right]
        """
        torsion_reinf_needed = dataframe["TTrnRebar (At/s)"].tolist()
        return [
            torsion_reinf_needed[i : i + 3]
            for i in range(0, len(torsion_reinf_needed), 3)
        ]

    beam_parameters = [
        get_stories(span_df),
        get_etabs_ids(span_df),
        get_width(flexural_df),
        get_depth(flexural_df),
        get_span(span_df),
        get_conc_grade(flexural_df),
        get_flexural_combo(flexural_df),
        get_top_flex_area(flexural_df),
        get_bot_flex_area(flexural_df),
        get_flex_torsion_area(shear_df),
        get_shear_force(shear_df),
        get_shear_combo(shear_df),
        get_shear_area(shear_df),
        get_torsion_area(shear_df),
    ]

    return beam_parameters
