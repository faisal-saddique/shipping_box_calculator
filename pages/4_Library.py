import streamlit as st
import pandas as pd
from utils import create_products_from_library, create_boxes_from_library
from uuid import uuid4
def insert_empty_lines(lines):
   for i in range(0,lines):
      st.write("")

products_df = pd.DataFrame(
    [
       {"SKU": "Planner", "LENGTH (in)": 7.25, "WIDTH":7.25, "HEIGHT": 0.75,"WEIGHT (lbs)": .5},
       {"SKU": "Large Notepad", "LENGTH (in)": 8.5, "WIDTH":11, "HEIGHT": 0.25,"WEIGHT (lbs)": .3},
       {"SKU": "Small Notepad", "LENGTH (in)": 4.25, "WIDTH":5.5, "HEIGHT": .25,"WEIGHT (lbs)": .1},
       {"SKU": "Greeting Card", "LENGTH (in)": 4.25, "WIDTH":5.5, "HEIGHT": 0.03125,"WEIGHT (lbs)": .01},
   ]
)

shipping_boxes_df = pd.DataFrame(
    [
       {"BOX SIZE": "10x10x10", "LENGTH (in)": 10, "WIDTH":10, "HEIGHT": 10, "MAXIMUM WEIGHT":45},
       {"BOX SIZE": "10x10x10", "LENGTH (in)": 20, "WIDTH":20, "HEIGHT": 20, "MAXIMUM WEIGHT":45},
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


        st.success(f"Updated the boxes collection.")

    except Exception as e:
        st.error(f"Please enter the data correctly: {e}")
