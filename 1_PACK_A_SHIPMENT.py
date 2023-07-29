import streamlit as st
import pandas as pd
from utils import convert_data_to_products, get_selected_items, skip_sub_data_frame_loadups
from streamlit_extras.switch_page_button import switch_page
from random import randint
import json

if "allow_first_time_load_page_1" not in st.session_state:
    st.session_state["allow_first_time_load_page_1"] = True

skip_sub_data_frame_loadups(1)

with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.header("PACK A SHIPMENT")

    st.markdown("*Box sizes are determined from your library of available boxes*")

    col1, col2 = st.columns([0.3,0.7])
    with col1:
        length = st.text_input(f"ORDER NUMBER")
    with col2:
        orient_choice = st.selectbox("CALCULATION MODE",["EQUALIZE WEIGHT (lbs) IF MULTIPLE BOXES NEEDED","UTILIZE ALL SPACE IN FIRST BOX IF MULTIPLE BOXES ARE NEEDED"])

    if "library_products" in st.session_state:
        library_products = st.session_state["library_products"]

        # for products in library_products:
        #     st.write(products)

        if "final_items" in st.session_state and st.session_state["final_items"] and st.session_state["allow_first_time_load_page_1"]:
            # st.error(f"inside {randint(0,45)}")
            
            st.session_state["allow_first_time_load_page_1"] = False

            products = []
            for product in st.session_state["final_items"]:
                # st.write(product)
                obj = {}
                obj["SKU"]=product.sku
                obj["QTY"]=product.quantity
                obj["ROTATION OK"]=product.rotation
                products.append(obj)
            st.session_state["items_df"] = pd.DataFrame(products)
            # st.write(items_df)
        if "items_df" not in st.session_state:      
            st.session_state["items_df"] = pd.DataFrame(
                [
                    {
                        "SKU": "",
                        "QTY": None,
                        "ROTATION OK": False,
                    },
                ],
            )
    
        st.markdown("**ITEMS TO PACK**")
        st.markdown("*Select the items from your library to be included in the shipment.*")
        items_df_edited = st.data_editor(
            st.session_state["items_df"],
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "SKU": st.column_config.SelectboxColumn(
                    "SKU",
                    help="The products as described in the library",
                    width="medium",
                    options=[
                        product.sku for product in library_products
                    ],
                )
            },
            hide_index=True,
        )

        # items_df_for_verification = []

        items_df_for_verification = get_selected_items(items_df_edited=items_df_edited,library_products=library_products)
        # st.write(items_df_for_verification.to_dict())
        st.markdown("**REVIEW**")
        st.table(items_df_for_verification)

        
        st.session_state["final_items"] = convert_data_to_products(items_df_for_verification.to_dict())
        
        # for item in st.session_state["final_items"]:
        #     st.write(item)

        st.session_state["items_selected"] = True
        col1, col2 = st.columns(2)
        with col1:
            st.write()
        with col2:    
            if st.button("PACK SHIPMENT", use_container_width=True):
                switch_page("PACKING MANIFEST")
    else:
        st.warning("Please enter the products first in the library!")

if __name__ == "__main__":
    main()
