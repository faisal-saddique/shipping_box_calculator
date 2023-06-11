import streamlit as st
import pandas as pd
from utils import convert_data_to_products

with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():
    st.header("PACK A SHIPMENT")
    st.write("New box size - not based on what's available in the library")


    col1, col2 = st.columns([0.3,0.7])
    with col1:
        length = st.number_input(f"ORDER NUMBER", value=0, step=1)
    with col2:
        orient_choice = st.selectbox("CALCULATION MODE",["EQUALIZE WEIGHT IF MULTIPLE BOXES NEEDED","UTILIZE ALL SPACE IN FIRST BOX IF MULTIPLE BOXES ARE NEEDED"])

    if "library_products" in st.session_state:
        library_products = st.session_state["library_products"]

        # for products in library_products:
        #     st.write(products)

        items_df = pd.DataFrame(
            [
                {
                    "SKU": "",
                    "QTY": None,
                    "ROTATION OK": False,
                },
            ],
        )

        items_df_edited = st.data_editor(
            items_df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "SKU": st.column_config.SelectboxColumn(
                    "Products",
                    help="The products as described in the library",
                    width="medium",
                    options=[
                        product.sku for product in library_products
                    ],
                )
            },
            hide_index=True,
        )

        # st.json(items_df_edited.to_dict())

        items_df_for_verification = []

        def get_selected_items(items_df_edited, library_products):
            items_df_for_display = pd.DataFrame(columns=["SKU", "LENGTH", "WIDTH", "HEIGHT", "WEIGHT", "QTY", "ROTATION OK"])

            for item_sku, item_qnt, item_rotation in zip(items_df_edited["SKU"], items_df_edited["QTY"], items_df_edited["ROTATION OK"]):
                for prod in library_products:
                    if prod.sku == item_sku:
                        item_dimensions = prod.dimensions
                        item_weight = prod.weight

                        item_data = {
                            "SKU": item_sku,
                            "LENGTH": item_dimensions[0],
                            "WIDTH": item_dimensions[1],
                            "HEIGHT": item_dimensions[2],
                            "WEIGHT": item_weight,
                            "QTY": item_qnt,
                            "ROTATION OK": item_rotation,
                        }

                        # st.write(item_data)
                        items_df_for_display = items_df_for_display = pd.concat([items_df_for_display, pd.DataFrame(item_data, index=[0])], ignore_index=True)
                        break

            return items_df_for_display

        items_df_for_verification = get_selected_items(items_df_edited=items_df_edited,library_products=library_products)

        st.dataframe(items_df_for_verification,use_container_width=True)
        st.session_state["final_items"] = convert_data_to_products(items_df_for_verification.to_dict())
        for item in st.session_state["final_items"]:
            st.write(item)
    else:
        st.warning("Please enter the products first in the library!")

if __name__ == "__main__":
    main()