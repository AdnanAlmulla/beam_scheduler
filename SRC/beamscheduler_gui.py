from nicegui import app, ui

# Turn on dark mode for the website.
ui.dark_mode().enable()

# Call the Eva Icons for icon usage.
ui.add_head_html(
    '<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet">'
)


# Create function which describes limitations and requirements of beam scheduler.
def start_popup():
    """This function aims to clarify what the beam scheduler does and what it requires
    to run properly."""
    with ui.dialog() as dialog, ui.card().classes("w-fit"):
        app.on_startup(dialog)
        ui.label("Beam Scheduler v1.0").classes(
            "self-center font-bold text-4xl -my-2"
        )
        ui.label("Made by Adnan Almulla @ Killa Design").classes(
            "self-center text-2xl"
        )
        ui.label(
            "To utilise this script appropriately, please consider and abide by the following:"
        ).classes("text-lg text-red-500 flex-nowrap")
        with ui.row().classes("text-lg w-full"):
            ui.label(
                "1. When exporting design results from ETABS, flexure and shear must be exported in the same spreadsheet."
            )
            ui.label(
                "2. All facade and superimposed beam elements must not be included in the exported spreadsheet."
            )
            ui.label(
                "3. Beam section definitions in ETABS must follow a naming convention such as ''B400X600-C45/55'', where 400 is width and 600 is depth."
            )
            ui.label(
                "4. The engineer must account for the fact that flexural design first prioritises an increase of rebar diameter up to 32mm, then proceeds to add an additional layer."
            )
            ui.label(
                "5. The engineer must account for the fact that shear design first prioritises an increase of spacing down to 100mm, then proceeds to increase the rebar diameter."
            )
            ui.label("6. This script adheres to ACI 318-19 for beam design.")
            ui.label(
                "7. Do not filter or alter the exported design results from ETABS. Leave it as it was obtained, as filtering or shifting columns / rows will cause incorrect results."
            )
        ui.button("Understood", on_click=dialog.close).classes(
            "self-center text-lg mt-4"
        )


# Create a copy function of start_popup to enable the question button to have a dialog popup
async def question_popup():
    """This function mimics start-popup, except it does not come up on start and only comes up when the question
    button is clicked"""
    with ui.dialog() as dialog, ui.card().classes("w-fit"):
        ui.label("Beam Scheduler v1.0").classes(
            "self-center font-bold text-4xl -my-2"
        )
        ui.label("Made by Adnan Almulla @ Killa Design").classes(
            "self-center text-2xl"
        )
        ui.label(
            "To utilise this script appropriately, please consider and abide by the following:"
        ).classes("text-lg text-red-500 flex-nowrap")
        with ui.row().classes("text-lg w-full"):
            ui.label(
                "1. When exporting design results from ETABS, flexure and shear must be exported in the same spreadsheet."
            )
            ui.label(
                "2. All facade and superimposed beam elements must not be included in the exported spreadsheet."
            )
            ui.label(
                "3. Beam section definitions in ETABS must follow a naming convention such as ''B400X600-C45/55'', where 400 is width and 600 is depth."
            )
            ui.label(
                "4. The engineer must account for the fact that flexural design first prioritises an increase of rebar diameter up to 32mm, then proceeds to add an additional layer."
            )
            ui.label(
                "5. The engineer must account for the fact that shear design first prioritises an increase of spacing down to 100mm, then proceeds to increase the rebar diameter."
            )
            ui.label("6. This script adheres to ACI 318-19 for beam design.")
            ui.label(
                "7. Do not filter or alter the exported design results from ETABS. Leave it as it was obtained, as filtering or shifting columns / rows will cause incorrect results."
            )
        ui.button("Understood", on_click=dialog.close).classes(
            "self-center text-lg mt-4"
        )
    await dialog


# Create upper row containing script name, KLD logo, github logo, and question mark for popup.
def ui_header():
    """This function holds the upper row which carries the title and logos."""
    with ui.grid(columns=3).classes("w-full no-wrap"):
        with ui.row().classes("pt-8 pb-6 pr-6 pl-10 justify-start items-start"):
            with ui.button(
                icon="question_mark", on_click=question_popup, color="#075985"
            ).classes("rounded-full w-16 h-16 ml-4"):
                ui.tooltip("Context").classes("text-lg rounded-full")
        with ui.row().classes(
            "bg-sky-900 pt-6 pb-6 pr-6 pl-6 rounded-full justify-center items-center"
        ):
            ui.label(
                "Beam Scheduler v1.0 - Made by Adnan Almulla @ Killa Design"
            ).classes("text-2xl font-bold pr-1")
        with ui.row().classes("pt-7 pb-6 pr-10 pl-6 justify-end items-end"):
            with ui.link(
                "",
                target="https://github.com/Circa-Hobbes/beam-scheduler",
                new_tab=True,
            ):
                ui.element("i").classes("eva eva-github").classes("text-7xl")
                ui.tooltip("Github").classes("text-lg rounded-full")


# Create main row in the centre of the page which contains the upload and download functionality.
def main_row(upload_handler):
    """This function holds the main row which carries the upload and download functionality."""
    with ui.grid(columns=3).classes("w-full no-wrap mt-64"):
        with ui.row().classes("pt-8 pb-6 pr-6 pl-10 justify-start items-start"):
            pass
        with ui.row().classes("mt-8 ml-4 pt-6 pr-6 pl-6 justify-center"):
            with ui.card().classes(
                "no-shadow border-[1px] rounded-full bg-sky-900"
            ):
                ui.label(
                    "Please upload the extracted flexure and shear excel spreadsheet:"
                ).classes("text-xl font-bold self-center")
        with ui.row().classes("pt-8 pb-6 pr-6 pl-10 justify-start items-start"):
            pass
    ###############################################################################################
    with ui.grid(columns=3).classes("w-full no-wrap"):
        with ui.row().classes("pt-8 pb-6 pr-6 pl-10 justify-start items-start"):
            pass
        with ui.row().classes(
            "mt-8 pt-6 pb-6 pr-6 pl-6 justify-center items-center"
        ):
            ui.upload(
                label="",
                on_upload=upload_handler,
                auto_upload=True,
                on_rejected=lambda: ui.notify(
                    "Please only upload an excel spreadsheet (.xlsx)",
                    type="warning",
                ),
            ).classes("w-96 text-lg self-center").props('accept=".xlsx"')
        with ui.row().classes("pt-8 pb-6 pr-6 pl-10 justify-start items-start"):
            pass


@ui.refreshable
def download_button():
    main_container = ui.grid(columns=1).classes("w-full no-wrap")
    return main_container
