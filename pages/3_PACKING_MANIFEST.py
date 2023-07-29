import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import copy
import pandas as pd
from utils import skip_sub_data_frame_loadups, pack_items

skip_sub_data_frame_loadups(3)
    
if "items_selected" in st.session_state and st.session_state["items_selected"]:
    
    st.header("PACKING MANIFEST")

    option = st.checkbox("Select the best fit box size irrespective of the boxes in library", value=False,
                         help="Choose whether to select only from available boxes or any box that is under the maximum dimensions specified.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_boxes = []
        st.write("Selected boxes:")
        for box in st.session_state["library_boxes"]:
            b_obj = {
                "BOX NAME":f"{box.dimensions[0]}x{box.dimensions[1]}x{box.dimensions[2]}",
                "MAXIMUM WEIGHT":box.max_weight
            }
            sel_boxes.append(b_obj)
        st.dataframe(pd.DataFrame(sel_boxes),use_container_width=True)
    with col2:
        sel_items = []

        st.write("Selected Items:")
        for product in st.session_state["final_items"]:
            it_obj = {
                "ITEM NAME":product.sku,
                "QUANTITY":product.quantity
            }
            sel_items.append(it_obj)
        st.dataframe(pd.DataFrame(sel_items),use_container_width=True)

    if "settings" in st.session_state:
        padding = (st.session_state["settings"]["top_padding"], st.session_state["settings"]["bottom_padding"], st.session_state["settings"]["sides_padding"])  # padding (top, bottom, 4 sides)
    else:
        st.session_state["settings"] = {
            "top_padding":0,
            "bottom_padding":0,
            "sides_padding":0,
            "max_box_weight":45
        }
        padding = (st.session_state["settings"]["top_padding"], st.session_state["settings"]["bottom_padding"], st.session_state["settings"]["sides_padding"])  # padding (top, bottom, 4 sides)

    pack_items(st.session_state["final_items"], st.session_state["library_boxes"],padding=padding,consider_maximum_dimensions=option)

else:
    st.warning("Please select the items and boxes first.")
