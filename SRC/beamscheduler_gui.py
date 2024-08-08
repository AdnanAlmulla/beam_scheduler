"""User interface module for the Beam Scheduler application.

This module defines the user interface components and layout for the Beam
Scheduler v2.0 application. It includes functions to create various UI elements
such as popups, headers, and main content areas for file upload and download
functionality.

The module uses the NiceGUI library to create a responsive web interface with
dark mode enabled and custom styling. It also incorporates Eva Icons for
visual elements.

Functions:
    start_popup: Display an initial popup with application information and
    usage guidelines.
    question_popup: Show a popup with application information, similar to the
    start popup.
    ui_header: Create the header section of the user interface.
    main_row: Display the main content area with file upload functionality.
    download_container: Create a container for the download button.
    add_down_button: Add a download button to the specified container.

Note:
    This module is designed to work with other components of the Beam Scheduler
    application, such as data processing and beam scheduling logic.
"""

from typing import Callable

from nicegui import app, ui

# Turn on dark mode for the website.
ui.dark_mode().enable()

# Call the Eva Icons for icon usage.
ui.add_head_html(
    '<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">'  # noqa: E501
)


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
            ui.tooltip("Github").classes("text-lg rounded-full w-16 h-16 ml-4")


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


def download_container() -> ui.grid:
    """Create download container for download button.

    Returns:
        ui.grid: Download container to store download button.
    """
    return ui.grid(columns=3).classes("w-full mt-64")


def add_down_button(
    grid_container: ui.grid, download_handler: Callable
) -> None:
    """Add the download button to prompt the user to download.

    Args:
        grid_container (ui.grid): The download container to place the button.
        download_handler (Callable): The function to handle the download process
        once the button is clicked.
    """
    with grid_container:
        # Left column - empty
        ui.label("").classes("col-span-1")
        # Middle column - download instructions and file download.
        with ui.column().classes(
            "col-span-1 items-center justify-center space-y-8"
        ):
            ui.button(
                "Download beam schedule",
                on_click=download_handler,
                color="#075985",
            ).classes("text-lg font-bold self-center rounded-full").on(
                "click", lambda: ui.notify("Downloading...")
            )
        # Right column - empty
        ui.label("").classes("col-span-1")
