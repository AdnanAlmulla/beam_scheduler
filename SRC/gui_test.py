import asyncio  # noqa: D100
import io
import tempfile
from typing import Callable

import beamscheduler_gui as gui
import data_extraction
import data_processing
import pandas as pd
from nicegui import app, events, ui

ui.dark_mode().enable()


def main() -> None:
    start_popup()
    ui_header()
    get_design_code()
    download_container = gui.download_container()
    ui.run(reload=False, title="Beam Scheduler", native=True)


def start_popup() -> None:
    """Display start popup which highlights the title and functionality."""
    with ui.dialog() as dialog, ui.card().classes("w-fit"):
        app.on_startup(dialog)
        ui.label("Beam Scheduler v2.0").classes(
            "self-center font-bold text-4xl -my-2"
        )
        ui.label("Made by Adnan Almulla @ Killa Design").classes(
            "self-center text-2xl"
        )
        ui.label(
            """To utilise this script appropriately, please consider and abide
            by the following:"""
        ).classes("text-lg text-red-500 flex-nowrap")
        with ui.row().classes("text-lg w-full"):
            ui.label(
                """1. When exporting design results from ETABS, flexure,
                shear, and frame assignments - summary must be exported in the
                same spreadsheet."""
            )
            ui.label(
                """2. All facade and superimposed beam elements must not be
                included in the exported spreadsheet."""
            )
            ui.label(
                """3. Beam section definitions in ETABS must follow a naming
                convention such as ''B400X600-C45/55'', where 400 is width and
                600 is depth."""
            )
            ui.label("4. This script adheres to ACI 318-19 for beam design.")
            ui.label(
                """5. Do not filter or alter the exported design results from
                ETABS. Leave it as it was obtained, as filtering or
                shifting columns / rows will cause incorrect results."""
            )
        ui.button("Understood", on_click=dialog.close).classes(
            "self-center text-lg mt-4"
        )


def main_row(upload_handler: Callable) -> None:
    """Display the main row to showcase upload and download button."""
    with ui.grid(columns=3).classes("w-full mt-64"):
        # Left column - empty
        ui.label("").classes("col-span-1")
        # Middle column - upload instructions and file upload
        with ui.column().classes(
            "col-span-1 items-center justify-center space-y-8"
        ):
            with ui.card().classes(
                "no-shadow border-[1px] rounded-full bg-sky-900 p-6"
            ):
                ui.label(
                    "Please upload the extracted ETABS spreadsheet:" ""
                ).classes("text-xl font-bold text-center")
            ui.upload(
                label="",
                on_upload=upload_handler,
                auto_upload=True,
                on_rejected=lambda: ui.notify(
                    "Please only upload an excel spreadsheet (.xlsx)",
                    type="warning",
                ),
            ).classes("w-96 text-lg").props('accept=".xlsx"')
        # Right column - empty
        ui.label("").classes("col-span-1")


def get_design_code() -> str:
    """Prompt the user to select a design code.

    Returns:
        str: The design code the engineer wishes to design to (currently
        supports only ACI 318-19 or Eurocode 2).
    """
    selected_code = ""
    with ui.grid(columns=3).classes("w-full mt-64"):
        # Left column - empty
        ui.label("").classes("col-span-1")
        # Middle column - selection of design code and submission button.
        with ui.column().classes(
            "col-span-1 items-center justify-center space-y-8"
        ):
            with ui.card().classes(
                "no-shadow border-[1px] rounded-full bg-sky-900 p-6"
            ):
                ui.label("Please select the design code to utilize:").classes(
                    "text-xl font-bold text-center"
                )
            # Store the select element in a variable
            design_code_selection = ui.select(
                ["ACI 318-19", "Eurocode 2"], value="ACI 318-19"
            ).classes("w-96 text-lg")

            # Create a function to handle the button click
            def handle_selection(selected_code: str) -> str:
                selected_code = str(
                    design_code_selection.value
                )  # Convert to string explicitly
                ui.notify(
                    f"Selected design code: {selected_code}", type="positive"
                )
                return selected_code

            ui.button("Confirm selection").on(
                "click", handle_selection
            ).classes("no-shadow border-[1px] rounded-full bg-sky-900 p-6")
        # Right column - empty
        ui.label("").classes("col-span-1")
    return selected_code


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


def ui_header() -> None:
    """This function holds the upper row which carries the title and logos."""
    with ui.grid(columns=3).classes("w-full pt-8 pb-6 pr-6 pl-10"):
        with ui.button(
            icon="question_mark", on_click=question_popup, color="#075985"
        ).classes("rounded-full w-16 h-16 ml-4 self-start"):
            ui.tooltip("Context").classes("text-lg rounded-full")

        with ui.column().classes("items-center justify-center h-full"):
            ui.label(
                "Beam Scheduler v2.0 - Made by Adnan Almulla @ Killa Design"
            ).classes(
                """text-2xl font-bold text-center bg-sky-900 py-8 px-8 
                rounded-full"""
            )

        with ui.link(
            target="https://github.com/Circa-Hobbes/beam-scheduler",
            new_tab=True,
        ).classes("self-end justify-self-end"):
            ui.element("i").classes("eva eva-github").classes("text-7xl")
            ui.tooltip("Github").classes("text-lg rounded-full")


async def question_popup() -> None:
    """Display popup that replicates start popup."""
    with ui.dialog() as dialog, ui.card().classes("w-fit"):
        ui.label("Beam Scheduler v2.0").classes(
            "self-center font-bold text-4xl -my-2"
        )
        ui.label("Made by Adnan Almulla @ Killa Design").classes(
            "self-center text-2xl"
        )
        ui.label(
            """To utilise this script appropriately, please consider and abide 
            by the following:"""
        ).classes("text-lg text-red-500 flex-nowrap")
        with ui.row().classes("text-lg w-full"):
            ui.label(
                """1. When exporting design results from ETABS, flexure, 
                shear, and frame assigns - summary must be exported in the same 
                spreadsheet."""
            )
            ui.label(
                """2. All facade and superimposed beam elements must not be 
                included in the exported spreadsheet."""
            )
            ui.label(
                """3. Beam section definitions in ETABS must follow a naming 
                convention such as ''B400X600-C45/55'', where 400 is width and 
                600 is depth."""
            )
            ui.label("6. This script adheres to ACI 318-19 for beam design.")
            ui.label(
                """7. Do not filter or alter the exported design results from 
                ETABS. Leave it as it was obtained, as filtering or shifting 
                columns / rows will cause incorrect results."""
            )
        ui.button("Understood", on_click=dialog.close).classes(
            "self-center text-lg mt-4"
        )
    await dialog


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
