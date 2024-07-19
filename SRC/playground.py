import pandas as pd
from Beam import Beam
from BeamDesign import BeamDesign


excel_file = r"assets\run_2.xlsx"

flexural_df = pd.read_excel(excel_file, sheet_name=0, header=1)
shear_df = pd.read_excel(excel_file, sheet_name=1, header=1)
span_df = pd.read_excel(excel_file, sheet_name=2, header=1)

# Remove the first row of each dataframes.
flexural_df = flexural_df.drop([0])
shear_df = shear_df.drop([0])
span_df = span_df.drop([0])
# Fetch the beam stories from the span df.
stories = span_df["Story"].tolist()
# Slice through the flexural df and get the etabs id.
etabs_ids = span_df["Label"].tolist()

# Slice through the flexural df and get the cleaned width, depth, and concrete comp strength.
dimension_error_check = False
try:
    beam_widths = [Beam.get_width(sections) for sections in flexural_df["Section"][::3]]
    beam_depths = [Beam.get_depth(sections) for sections in flexural_df["Section"][::3]]
    concrete_grade = [
        Beam.get_comp_conc_grade(sections) for sections in flexural_df["Section"][::3]
    ]
except ValueError:
    # True means section definitions have not been titled correctly as per requirements.
    dimension_error_check = True

if dimension_error_check is False:
    # Take each beam's span and convert it from m to mm.
    spans = span_df["Length"].tolist()
    spans = [round(span * 1000) for span in spans]

    # Take each beam's flexural combo and put it in a list within a list.
    pos_combo_list = flexural_df["+ve Moment Combo"].tolist()
    nested_pos_combo_list = [
        pos_combo_list[i : i + 3] for i in range(0, len(pos_combo_list), 3)
    ]
    neg_combo_list = flexural_df["-ve Moment Combo"].tolist()
    nested_neg_combo_list = [
        neg_combo_list[i : i + 3] for i in range(0, len(neg_combo_list), 3)
    ]
    # Take the nested lists and return True if any of the combos are overstressed.
    checked_pos_combo_list = [
        True
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else False
        for sublist in nested_pos_combo_list
    ]
    checked_neg_combo_list = [
        True
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else False
        for sublist in nested_neg_combo_list
    ]
    # Zip the positive and negative combos together. Index 0 is positive, Index 1 is negative.
    flexural_combo = [
        [pos, neg] for pos, neg in zip(checked_pos_combo_list, checked_neg_combo_list)
    ]
    # Take the required top flexural reinforcement and put it in a nested list.
    # Index 0 is left, Index 1 is middle, and Index 2 is right.
    top_flex_reinf_needed = flexural_df["As Top"].tolist()
    top_flex_reinf_needed = [
        top_flex_reinf_needed[i : i + 3]
        for i in range(0, len(top_flex_reinf_needed), 3)
    ]
    # Check if any of the beams are overstressed. If they are, the values get replaced with O/S.
    top_flex_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in top_flex_reinf_needed
    ]
    # Repeat the same as above but for required bottom flexural reinforcement.
    bot_flex_reinf_needed = flexural_df["As Bot"].tolist()
    bot_flex_reinf_needed = [
        bot_flex_reinf_needed[i : i + 3]
        for i in range(0, len(bot_flex_reinf_needed), 3)
    ]
    bot_flex_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in bot_flex_reinf_needed
    ]
    # Take the required flexural torsion reinforcement and put it in a nested list.
    # Index 0 is left, Index 1 is middle, and Index 2 is right.
    flex_torsion_reinf_needed = shear_df["TLngRebar (Al)"].tolist()
    flex_torsion_reinf_needed = [
        flex_torsion_reinf_needed[i : i + 3]
        for i in range(0, len(flex_torsion_reinf_needed), 3)
    ]
    # Check if any of the beams are overstressed in torsion. If they are, values get replaced with O/S.
    flex_torsion_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in flex_torsion_reinf_needed
    ]
    # Take each beams shear force (kN) and put it in a nested list.
    shear_force_list = shear_df["Shear Force"].tolist()
    nested_shear_force = [
        shear_force_list[i : i + 3] for i in range(0, len(shear_force_list), 3)
    ]
    # Take each beam's shear combo and put it in a nested list.
    shear_combo_list = shear_df["Shear Design Combo"].tolist()
    nested_shear_combo = [
        shear_combo_list[i : i + 3] for i in range(0, len(shear_combo_list), 3)
    ]
    # Take the nested list and return OK or OS as a string in a list.
    checked_shear_combo = [
        True
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else False
        for sublist in nested_shear_combo
    ]
    # Repeat the same as shear combo, except for torsion combo.
    torsion_combo_list = shear_df["TTrnCombo"].tolist()
    nested_torsion_combo = [
        torsion_combo_list[i : i + 3] for i in range(0, len(torsion_combo_list), 3)
    ]
    checked_torsion_combo = [
        True
        if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
        else False
        for sublist in nested_torsion_combo
    ]
    shear_combo = [
        [shear, torsion]
        for shear, torsion in zip(checked_shear_combo, checked_torsion_combo)
    ]
    # Take the required shear reinforcement and put it in a nested list.
    # Index 0 is left, Index 1 is middle, and Index 2 is right.
    shear_reinf_needed = shear_df["VRebar (Av/s)"].tolist()
    shear_reinf_needed = [
        shear_reinf_needed[i : i + 3] for i in range(0, len(shear_reinf_needed), 3)
    ]
    # Check if any of the beams are overstressed in shear. If they are, values get replaced with O/S.
    shear_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in shear_reinf_needed
    ]
    # Repeat the same as required shear reinforcement but for required torsion reinforcement.
    torsion_reinf_needed = shear_df["TTrnRebar (At/s)"].tolist()
    torsion_reinf_needed = [
        torsion_reinf_needed[i : i + 3] for i in range(0, len(torsion_reinf_needed), 3)
    ]
    torsion_reinf_needed = [
        [
            "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
            for element in sublist
        ]
        for sublist in torsion_reinf_needed
    ]

    # Create beam_instances list and store all the Beam objects.
    beam_instances = [
        Beam(
            stories,
            etabs_id,
            width,
            depth,
            span,
            concrete_grade,
            flexural_combo,
            req_top_flex_reinf,
            req_bot_flex_reinf,
            req_flex_torsion_reinf,
            shear_force,
            shear_overstressed,
            req_shear_reinf,
            req_torsion_reinf,
        )
        for stories, etabs_id, width, depth, span, concrete_grade, flexural_combo, req_top_flex_reinf, req_bot_flex_reinf, req_flex_torsion_reinf, shear_force, shear_overstressed, req_shear_reinf, req_torsion_reinf in zip(
            stories,
            etabs_ids,
            beam_widths,
            beam_depths,
            spans,
            concrete_grade,
            flexural_combo,
            top_flex_reinf_needed,
            bot_flex_reinf_needed,
            flex_torsion_reinf_needed,
            nested_shear_force,
            shear_combo,
            shear_reinf_needed,
            torsion_reinf_needed,
        )
    ]
    designed_beams = []  # List to hold all the designed beams.
    # Begin with for loop and create attributes for each beam instance to undertake calculations.
    for beam in beam_instances:
        # Instantiate the Beam Design object.
        beam_design = BeamDesign(beam)
        # Undertake the process of flexural design.
        beam_design.calculate_flexural_design()
        # Append all the designed beams to the designed beams list.
        designed_beams.append(beam_design)
        # # Calculate the required shear legs based on the beams width.
        # beam.get_shear_legs()

        # # Assess if the transverse shear spacing needs to be checked.
        # beam.check_transverse_shear_spacing()

        # # Calculate the total required shear reinforcement including shear and torsion.
        # beam.get_total_shear_req()

        # # Calculate the provided shear reinforcement string and area.
        # beam.get_min_shear_long_spacing()
        # beam.get_shear_string()
        # beam.get_shear_area()

        # # Check and replace if necessary the maximum longitudinal shear spacing against Clause 18.4.2.4 of ACI 318-19.
        # beam.modify_shear_reinf()

        # # Calculate the allowable side face clear space in beams which have a depth greater than 600mm.
        # beam.get_side_face_clear_space()

        # # Calculate the provided side face reinforcement string and area.
        # beam.get_side_face_string()
        # beam.get_side_face_area()

        # # Grab the index of the side face reinforcement with the highest area.
        # beam.get_index_for_side_face_reinf()

# print(designed_beams[4].beam.req_top_flex_reinf)
# print(designed_beams[4].flexural_design.top_flex_rebar["left"]["rebar_text"])
# print(designed_beams[4].flexural_design.top_flex_rebar["left"]["provided_reinf"])
# print(designed_beams[4].flexural_design.top_flex_rebar["left"]["diameter"])

# print(designed_beams[5].beam.req_top_flex_reinf)
# print(designed_beams[5].beam.req_bot_flex_reinf)
# print(designed_beams[5].flexural_design)

print(designed_beams[5].flexural_design.residual_rebar)
