import streamlit as st
import pandas as pd
import json
from utils import skip_sub_data_frame_loadups

skip_sub_data_frame_loadups(5)

pass_key = True

def rename_key(json_obj, old_key, new_key):
    if isinstance(json_obj, dict):
        new_obj = {}
        for key, value in json_obj.items():
            if key == old_key:
                new_obj[new_key] = value
            else:
                new_obj[key] = rename_key(value, old_key, new_key)
        return new_obj
    elif isinstance(json_obj, list):
        new_obj = []
        for item in json_obj:
            new_obj.append(rename_key(item, old_key, new_key))
        return new_obj
    else:
        return json_obj

if "settings" in st.session_state and st.session_state["settings"] and pass_key:
    pass_key = False
    # st.success("yes")
    df = pd.DataFrame(
        [
        {
            "PADDING ON TOP (in)": st.session_state["settings"]["top_padding"], 
            "PADDING ON BOTTOM (in)": st.session_state["settings"]["bottom_padding"], 
            "PADDING ON SIDES (in)": st.session_state["settings"]["sides_padding"], 
            "MAX BOX WEIGHT (lbs)":st.session_state["settings"]["max_box_weight"]
            },
        ]
    )
else:
    df = pd.DataFrame(
        [
        {
            "PADDING ON TOP (in)": 0, 
            "PADDING ON BOTTOM (in)": 0, 
            "PADDING ON SIDES (in)": 0, 
            "MAX BOX WEIGHT (lbs)":45
            },
        ]
    )

st.header("SETTINGS")

st.write("APPLIES TO ALL SHIPMENTS")

edited_df = st.data_editor(df)

data_json = edited_df.to_json()

data = {}
for key, value in json.loads(data_json).items():
    data[key] = value["0"]

# Apply rename_key() function to the Python object
data = rename_key(data, "PADDING ON TOP (in)", "top_padding")
data = rename_key(data, "PADDING ON BOTTOM (in)", "bottom_padding")
data = rename_key(data, "PADDING ON SIDES (in)", "sides_padding")
data = rename_key(data, "MAX BOX WEIGHT (lbs)", "max_box_weight")

st.session_state["settings"] = data

st.json(st.session_state["settings"])
