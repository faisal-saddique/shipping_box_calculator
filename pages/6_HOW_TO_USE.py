import streamlit as st
from utils import skip_sub_data_frame_loadups

skip_sub_data_frame_loadups(6)

st.subheader("HOW TO USE")

st.markdown('<span style="background-color: #fff4bc; font-size: 20px; font-weight: bold; display: inline-block; width: 100%;">PACK A SHIPMENT USING BOXES IN YOUR LIBRARY</span>', unsafe_allow_html=True)

st.markdown("##### 1. SET UP YOUR LIBRARY\n"
             "- Add your commonly shipped product items and their dimensions\n"
             "- Add your frequently used box sizes and their dimensions")

st.markdown("##### 2. ADJUST YOUR SETTINGS\n"
             "- Enter your preferred padding space between the products and the inner walls of the shipping box - for example: 2 inches of void fill on all sides.\n"
             "- Enter the maximum weight you want each box to hold.")

st.markdown("##### 3. PACK YOUR SHIPMENT\n"
             "- Enter your order number if applicable.\n"
             "- Select your calculation mode.\n"
             "- Select the products from your library that will be packed in the shipment using the dropdown menu in the table.\n"
             "- Select the checkbox if your item is able to be rotated or must remain flat.\n"
             "- Click 'Pack Shipment' to determine the best box size for your shipment from your library of available options.")

st.markdown('<span style="background-color: #fff4bc; font-size: 20px; font-weight: bold; display: inline-block; width: 100%;">FIND A BOX SIZE</span>', unsafe_allow_html=True)
st.markdown("If you need to determine a shipping box size beyond what is available in your box library, use the 'Find a Box Size' calculator.\n"
            "\nREPEAT STEPS 1-3 ABOVE, AND ALSO ADD IN YOUR MAXIMUM DESIRED BOX DIMENSIONS.")
