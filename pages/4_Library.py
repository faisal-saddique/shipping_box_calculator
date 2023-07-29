import streamlit as st
import pandas as pd
from utils import create_products_from_library, create_boxes_from_library, skip_sub_data_frame_loadups

skip_sub_data_frame_loadups(4)

def insert_empty_lines(lines):
   for i in range(0,lines):
      st.write("")

products_df = pd.DataFrame(
    [
       {"SKU": "Planner", "LENGTH (In)": 7.25, "WIDTH (In)":7.25, "HEIGHT (In)": 0.75,"WEIGHT (lbs)": .5},
       {"SKU": "Large Notepad", "LENGTH (In)": 8.5, "WIDTH (In)":11, "HEIGHT (In)": 0.25,"WEIGHT (lbs)": .3},
       {"SKU": "Small Notepad", "LENGTH (In)": 4.25, "WIDTH (In)":5.5, "HEIGHT (In)": .25,"WEIGHT (lbs)": .1},
       {"SKU": "Greeting Card", "LENGTH (In)": 4.25, "WIDTH (In)":5.5, "HEIGHT (In)": 0.03125,"WEIGHT (lbs)": .01},
   ]
)

shipping_boxes_df = pd.DataFrame(
    [
       {"BOX SIZE": "10x10x10", "LENGTH (In)": 10, "WIDTH (In)":10, "HEIGHT (In)": 10, "MAXIMUM WEIGHT":45},
   ]
)

st.header("LIBRARY")

tab1, tab2 = st.tabs(["PRODUCTS", "SHIPPING BOXES"])

with tab1:
    insert_empty_lines(1)
    st.write("ITEMS TO PACK")
    insert_empty_lines(3)
    updated_products_df = st.data_editor(products_df,use_container_width=True,num_rows="dynamic")

    try:
        st.session_state["library_products"] = create_products_from_library(updated_products_df.to_dict())
        st.success(f"Updated the products collection.")
    except Exception as e:
        st.error(f"Please enter the data correctly: {e}")
        

with tab2:
    insert_empty_lines(1)
    st.write("AVAILABLE SHIPPING BOXES SIZES")
    insert_empty_lines(3)
    updated_shipping_boxes_df = st.data_editor(shipping_boxes_df,use_container_width=True,num_rows="dynamic")


    try:
        # st.write(updated_shipping_boxes_df.to_dict())
        st.session_state["library_boxes"] = create_boxes_from_library(updated_shipping_boxes_df.to_dict())
        st.write(st.session_state["library_boxes"])

        st.success(f"Updated the boxes collection.")

    except Exception as e:
        st.error(f"Please enter the data correctly: {e}")
