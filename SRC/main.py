"""Main module for the Beam Scheduler application.

This module serves as the entry point for the Beam Scheduler application. It
handles the file upload process, data processing, and file download
functionality. The module integrates with the user interface components defined
in the beamscheduler_gui module and utilizes data extraction and processing
functions from other modules.

The application allows users to upload an Excel spreadsheet containing beam
data, processes this data to create a beam schedule, and provides the option to
download the resulting schedule.

Functions:
    main: Initialize the user interface and run the application.
    excel_handler: Handle the uploaded Excel spreadsheet and initiate
    processing.
    process_content: Process the uploaded spreadsheet data and create the beam
    schedule.
    download_handler: Handle the download request for the processed beam
    schedule.
    export_file: Export the processed beam schedule to an Excel file.
"""

import asyncio
import io
import tempfile

import beamscheduler_gui as gui
import data_extraction
import data_processing
import pandas as pd
from nicegui import events, ui

processed_beam_schedule_df = None
quantities_schedule_df = None


def main() -> None:  # noqa: D103
    gui.start_popup()
    gui.ui_header()
    gui.main_row(lambda e: excel_handler(e, download_container))
    download_container = gui.download_container()
    ui.run(reload=False, title="Beam Scheduler", native=True)


# Handle and utilise the excel spreadsheet for processing.
def excel_handler(
    excel_string: events.UploadEventArguments, container: ui.grid
) -> None:
    """Handle and deploy the uploaded spreadsheet and container.

    Args:
        excel_string (events.UploadEventArguments): The uploaded excel sheet.
        container (ui.grid): The download button container.
    """
    excel = pd.ExcelFile(excel_string.content)
    if len(excel.sheet_names) == 4:
        ui.notify(
            f"""{excel_string.name} successfully uploaded! Please await 
            processing.""",
            type="positive",
        )
        # Schedule the processing of the content asynchronously
        asyncio.create_task(process_content(excel_string, container))
    else:
        ui.notify(
            f"""{excel_string.name} does not contain the correct number of 
            sheets. Are you sure flexure and shear are in the same 
            spreadsheet?""",
            type="warning",
        )


async def process_content(
    excel_string: events.UploadEventArguments, container: ui.grid
) -> None:
    """Process the uploaded spreadsheet and container. Undertake design.

    Args:
        excel_string (events.UploadEventArguments): The uploaded excel sheet.
        container (ui.grid): The download button container.
    """
    global processed_beam_schedule_df
    global quantities_schedule_df
    excel_file = excel_string.content
    checking_flex = pd.read_excel(excel_file, sheet_name=3)
    checking_shear = pd.read_excel(excel_file, sheet_name=2)
    checking_span = pd.read_excel(excel_file, sheet_name=1)
    if (
        checking_flex.columns[0]
        == "TABLE:  Concrete Beam Flexure Envelope - ACI 318-19"
        and checking_shear.columns[0]
        == "TABLE:  Concrete Beam Shear Envelope - ACI 318-19"
        and checking_span.columns[0] == "TABLE:  Frame Assignments - Summary"
    ):
        beam_parameters = data_extraction.extract_data(excel_string.content)
        if not beam_parameters:
            with container:
                ui.notify(
                    """The ETABS ids do not match in each spreadsheet.
                    Please ensure that the rows are not sorted or
                    filtered.""",
                    type="negative",
                )
        else:
            (
                processed_beam_schedule_df,
                quantities_schedule_df,
            ) = await asyncio.to_thread(
                data_processing.process_data, beam_parameters
            )
            with container:
                if processed_beam_schedule_df.empty:
                    ui.notify(
                        """The section definitions as exported in the 
                        spreadsheet do not abide with the syntax required. 
                        Please update and try again.""",
                        type="negative",
                    )
                elif processed_beam_schedule_df is None:
                    ui.notify(
                        """No data available for download or uploaded file does 
                        not adhere to considerations. Please try again.""",
                        type="negative",
                    )
                elif isinstance(processed_beam_schedule_df, pd.DataFrame):
                    if processed_beam_schedule_df.empty:
                        ui.notify(
                            """Processing did not go through and spreadsheet is 
                            empty. Please revise and consider context then try 
                            again""",
                            type="warning",
                        )
                    else:
                        ui.notify(
                            """Processing complete. Please download the 
                            completed beam schedule.""",
                            type="positive",
                        )
                        gui.add_down_button(container, download_handler)
    else:
        with container:
            ui.notify(
                f"""{excel_string.name} does not contain the correct sheets. Are
                you sure flexure and shear are in the this spreadsheet?""",
                type="warning",
            )


def download_handler() -> None:
    """Handle the download button. Calls the export file functon."""
    global processed_beam_schedule_df
    global quantities_schedule_df
    # Call export_file to get the in-memory Excel file
    excel_content = export_file(
        processed_beam_schedule_df,  # type: ignore
        quantities_schedule_df,  # type: ignore
    )
    # Write the content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(excel_content)
        tmp_path = tmp.name  # Store the file path
    # Initiate the download using the file path
    ui.download(tmp_path, "beam_schedule.xlsx")


# Create the relevant functions to export the excel file
def export_file(
    beam_schedule_df: pd.DataFrame, quantities_schedule_df: pd.DataFrame
) -> bytes:
    """Take the beam schedule and export it into an excel spreadsheet.

    Args:
        beam_schedule_df (pd.DataFrame): The processed beam schedule dataframe.
        quantities_schedule_df (pd.DataFrame): The quantity schedule dataframe.

    Returns:
        bytes: The finalised excel spreadsheet in bytes.
    """
    # Use BytesIO as an in-memory buffer
    output = io.BytesIO()
    # Create an Excel writer object with the BytesIO object
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:  # pyright: ignore abstract-class-instantiated
        # Write the entire DataFrame to the first sheet
        beam_schedule_df.to_excel(
            writer, sheet_name="Beam Reinforcement Schedule"
        )
        quantities_schedule_df.to_excel(
            writer, sheet_name="Quantities Schedule"
        )
        # Group by the 'Storey' column
        grouped = beam_schedule_df.groupby("Storey", sort=False)
        # Iterate through the groups and write to separate sheets
        for name, group in grouped:
            sheet_name = f"{name}"
            group.to_excel(writer, sheet_name=sheet_name)

    # Return the Excel file content from the in-memory buffer
    return output.getvalue()


if __name__ in {"__main__", "__mp_main__"}:
    main()
