import asyncio
import io
import tempfile

import beamscheduler_gui as gui
import df_processing as pr
import pandas as pd
from nicegui import events, ui

# Global variable to store the processed DataFrame
processed_beam_schedule_df = None


def main() -> None:
    gui.start_popup()
    gui.ui_header()
    gui.main_row(lambda e: excel_handler(e, main_container))
    main_container = gui.download_button()
    ui.run(reload=False, title="Beam Scheduler", native=True)


# Handle and utilise the excel spreadsheet for processing.
def excel_handler(e: events.UploadEventArguments, container):
    global processed_beam_schedule_df
    xl = pd.ExcelFile(e.content)
    if len(xl.sheet_names) == 4:
        ui.notify(
            f"{e.name} successfully uploaded! Please await processing.",
            type="positive",
        )
        # Schedule the processing of the content asynchronously
        asyncio.create_task(process_content(e, container))
    else:
        ui.notify(
            f"{e.name} does not contain the correct number of sheets. Are you sure flexure and shear are in the same spreadsheet?",
            type="warning",
        )


async def process_content(e: events.UploadEventArguments, container):
    global processed_beam_schedule_df
    excel_file = e.content
    checking_span = pd.read_excel(excel_file, sheet_name=0)
    checking_flex = pd.read_excel(excel_file, sheet_name=1)
    checking_shear = pd.read_excel(excel_file, sheet_name=2)
    if (
        checking_flex.columns[0]
        == "TABLE:  Concrete Beam Flexure Envelope - ACI 318-19"
        and checking_shear.columns[0]
        == "TABLE:  Concrete Beam Shear Envelope - ACI 318-19"
        and checking_span.columns[0] == "TABLE:  Beam Object Connectivity"
    ):
        initial_flexural_df = pd.read_excel(excel_file, sheet_name=1)
        initial_shear_df = pd.read_excel(excel_file, sheet_name=2)
        initial_span_df = pd.read_excel(excel_file, sheet_name=0)
        processed_beam_schedule_df = await asyncio.to_thread(
            pr.process_dataframes,
            initial_flexural_df,
            initial_shear_df,
            initial_span_df,
        )
        with container:
            if isinstance(processed_beam_schedule_df, str):
                if (
                    processed_beam_schedule_df
                    == "Incorrect section definitions"
                ):
                    ui.notify(
                        "The section definitions as exported in the spreadsheet do not abide with the syntax required. Please update and try again.",
                        type="negative",
                    )
            elif processed_beam_schedule_df is None:
                ui.notify(
                    "No data available for download or uploaded file does not adhere to considerations. Please try again.",
                    type="negative",
                )
            elif isinstance(processed_beam_schedule_df, pd.DataFrame):
                if processed_beam_schedule_df.empty:
                    ui.notify(
                        "Processing did not go through and spreadsheet is empty. Please revise and consider context then try again",
                        type="warning",
                    )
                else:
                    ui.notify(
                        "Processing complete. Please download the completed beam schedule.",
                        type="positive",
                    )
                    add_down_button()
    else:
        with container:
            ui.notify(
                f"{e.name} does not contain the correct sheets. Are you sure flexure, shear, and beam object connectivity are in the this spreadsheet?",
                type="warning",
            )


def add_down_button() -> None:
    with ui.grid(columns=3).classes("w-full no-wrap mt-5"):
        with ui.row().classes("pt-8 pb-6 pr-6 pl-10 justify-start items-start"):
            pass
        with ui.row().classes(
            "pt-6 pb-6 pr-6 pl-6 justify-center items-center"
        ):
            ui.button(
                "download beam schedule",
                on_click=download_handler,
                color="#075985",
            ).classes("text-lg font-bold self-center rounded-full").on(
                "click", lambda: ui.notify("Downloading...")
            )
        with ui.row().classes("pt-8 pb-6 pr-6 pl-10 justify-start items-start"):
            pass


# Create the relevant functions to export the excel file
def export_file(beam_schedule_df: pd.DataFrame) -> bytes:
    # Use BytesIO as an in-memory buffer
    output = io.BytesIO()
    # Create an Excel writer object with the BytesIO object
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Write the entire DataFrame to the first sheet
        beam_schedule_df.to_excel(
            writer, sheet_name="Beam Reinforcement Schedule"
        )
        # Group by the 'Storey' column
        grouped = beam_schedule_df.groupby("Storey", sort=False)
        # Iterate through the groups and write to separate sheets
        for name, group in grouped:
            sheet_name = f"{name}"
            group.to_excel(writer, sheet_name=sheet_name)
    # Return the Excel file content from the in-memory buffer
    return output.getvalue()


def download_handler() -> None:
    global processed_beam_schedule_df
    # Call export_file to get the in-memory Excel file
    excel_content = export_file(processed_beam_schedule_df)
    # Write the content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(excel_content)
        tmp_path = tmp.name  # Store the file path
    # Initiate the download using the file path
    ui.download(tmp_path, "beam_schedule.xlsx")


if __name__ in {"__main__", "__mp_main__"}:
    main()
