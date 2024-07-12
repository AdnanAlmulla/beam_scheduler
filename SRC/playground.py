import pandas as pd
from beam import Beam

excel_file = r"assets\test run.xlsx"


# Create all instances of Beam class.
def create_instance(
    storey,
    etabs_id,
    width,
    depth,
    span,
    comp_conc_grade,
    pos_flex_combo,
    neg_flex_combo,
    req_top_flex_reinf,
    req_bot_flex_reinf,
    req_flex_torsion_reinf,
    shear_force,
    shear_combo,
    torsion_combo,
    req_shear_reinf,
    req_torsion_reinf,
):
    beam = Beam(
        storey,
        etabs_id,
        width,
        depth,
        span,
        comp_conc_grade,
        pos_flex_combo,
        neg_flex_combo,
        req_top_flex_reinf,
        req_bot_flex_reinf,
        req_flex_torsion_reinf,
        shear_force,
        shear_combo,
        torsion_combo,
        req_shear_reinf,
        req_torsion_reinf,
    )
    return beam


flexural_df = pd.read_excel(excel_file, sheet_name=1, header=1)
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

    # Take each beam's positive flexural combo and put it in a list within a list.
    positive_combo_list = flexural_df["Unnamed: 8"].tolist()
    nested_pos_combo_list = [
        positive_combo_list[i : i + 3] for i in range(0, len(positive_combo_list), 3)
    ]
    # Repeat same process as positive flexural combo for negative flexural combo.
    negative_combo_list = flexural_df["Unnamed: 5"].tolist()
    nested_neg_combo_list = [
        negative_combo_list[i : i + 3] for i in range(0, len(negative_combo_list), 3)
    ]

    # # Take the nested list and return OK or O/S as a string in a list.
    # nested_pos_combo_list = [
    #     "O/S"
    #     if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
    #     else "OK"
    #     for sublist in nested_pos_combo_list
    # ]
    # nested_neg_combo_list = [
    #     "O/S"
    #     if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
    #     else "OK"
    #     for sublist in nested_neg_combo_list
    # ]

#     # Slice through the flexural df and retrieve whether is it overstressed in positive combo.
#     positive_flex_combo = Beam.check_combo(nested_pos_combo_list)

#     # Slice through the flexural df and retrieve whether it is overstressed in negative combo.
#     negative_flex_combo = Beam.check_combo(nested_neg_combo_list)

#     # Take the required top flexural reinforcement and put it in a nested list.
#     # Index 0 is left, Index 1 is middle, and Index 2 is right.
#     top_flex_reinf_needed = flexural_df["Unnamed: 7"].tolist()
#     top_flex_reinf_needed = [
#         top_flex_reinf_needed[i : i + 3]
#         for i in range(0, len(top_flex_reinf_needed), 3)
#     ]
#     # Check if any of the beams are overstressed. If they are, the values get replaced with O/S.
#     top_flex_reinf_needed = [
#         [
#             "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
#             for element in sublist
#         ]
#         for sublist in top_flex_reinf_needed
#     ]

#     # Repeat the same as above but for required bottom flexural reinforcement.
#     bot_flex_reinf_needed = flexural_df["Unnamed: 10"].tolist()
#     bot_flex_reinf_needed = [
#         bot_flex_reinf_needed[i : i + 3]
#         for i in range(0, len(bot_flex_reinf_needed), 3)
#     ]
#     bot_flex_reinf_needed = [
#         [
#             "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
#             for element in sublist
#         ]
#         for sublist in bot_flex_reinf_needed
#     ]

#     # Take the required flexural torsion reinforcement and put it in a nested list.
#     # Index 0 is left, Index 1 is middle, and Index 2 is right.
#     flex_torsion_reinf_needed = shear_df["Unnamed: 14"].tolist()
#     flex_torsion_reinf_needed = [
#         flex_torsion_reinf_needed[i : i + 3]
#         for i in range(0, len(flex_torsion_reinf_needed), 3)
#     ]

#     # Check if any of the beams are overstressed in torsion. If they are, values get replaced with O/S.
#     flex_torsion_reinf_needed = [
#         [
#             "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
#             for element in sublist
#         ]
#         for sublist in flex_torsion_reinf_needed
#     ]

#     # Take each beams shear force (kN) and put it in a nested list.
#     shear_force_list = shear_df["Unnamed: 6"].tolist()
#     nested_shear_force = [
#         shear_force_list[i : i + 3] for i in range(0, len(shear_force_list), 3)
#     ]

#     # Take each beam's shear combo and put it in a nested list.
#     shear_combo_list = shear_df["Unnamed: 5"].tolist()
#     nested_shear_combo = [
#         shear_combo_list[i : i + 3] for i in range(0, len(shear_combo_list), 3)
#     ]

#     # Take the nested list and return OK or OS as a string in a list.
#     nested_shear_combo = [
#         "O/S"
#         if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
#         else "OK"
#         for sublist in nested_shear_combo
#     ]

#     # Apply the Beam class method to retrieve whether it is overstressed in shear.
#     shear_combo_check = Beam.check_combo(nested_shear_combo)

#     # Repeat the same as shear combo, except for torsion combo.
#     torsion_combo_list = shear_df["Unnamed: 9"].tolist()
#     nested_torsion_combo = [
#         torsion_combo_list[i : i + 3] for i in range(0, len(torsion_combo_list), 3)
#     ]

#     nested_torsion_combo = [
#         "O/S"
#         if any(str(element).strip().lower() in ["o/s", "nan"] for element in sublist)
#         else "OK"
#         for sublist in nested_torsion_combo
#     ]

#     torsion_combo_check = Beam.check_combo(nested_torsion_combo)

#     # Take the required shear reinforcement and put it in a nested list.
#     # Index 0 is left, Index 1 is middle, and Index 2 is right.
#     shear_reinf_needed = shear_df["Unnamed: 8"].tolist()
#     shear_reinf_needed = [
#         shear_reinf_needed[i : i + 3] for i in range(0, len(shear_reinf_needed), 3)
#     ]

#     # Check if any of the beams are overstressed in shear. If they are, values get replaced with O/S.
#     shear_reinf_needed = [
#         [
#             "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
#             for element in sublist
#         ]
#         for sublist in shear_reinf_needed
#     ]

#     # Repeat the same as required shear reinforcement but for required torsion reinforcement.
#     torsion_reinf_needed = shear_df["Unnamed: 11"].tolist()
#     torsion_reinf_needed = [
#         torsion_reinf_needed[i : i + 3] for i in range(0, len(torsion_reinf_needed), 3)
#     ]
#     torsion_reinf_needed = [
#         [
#             "O/S" if str(element).strip().lower() in ["o/s", "nan"] else element
#             for element in sublist
#         ]
#         for sublist in torsion_reinf_needed
#     ]

#     # Call create_instance function and create instances of all beams.
#     beam_instances = [
#         create_instance(
#             stories,
#             e_id,
#             width,
#             depth,
#             span,
#             concrete_grade,
#             pos_flex_combo,
#             neg_flex_combo,
#             req_top_flex_reinf,
#             req_bot_flex_reinf,
#             req_flex_torsion_reinf,
#             shear_force,
#             shear_combo,
#             torsion_combo,
#             req_shear_reinf,
#             req_torsion_reinf,
#         )
#         for stories, e_id, width, depth, span, concrete_grade, pos_flex_combo, neg_flex_combo, req_top_flex_reinf, req_bot_flex_reinf, req_flex_torsion_reinf, shear_force, shear_combo, torsion_combo, req_shear_reinf, req_torsion_reinf in zip(
#             stories,
#             e_ids,
#             beam_widths,
#             beam_depths,
#             spans,
#             concrete_grade,
#             positive_flex_combo,
#             negative_flex_combo,
#             top_flex_reinf_needed,
#             bot_flex_reinf_needed,
#             flex_torsion_reinf_needed,
#             nested_shear_force,
#             shear_combo_check,
#             torsion_combo_check,
#             shear_reinf_needed,
#             torsion_reinf_needed,
#         )
#     ]
