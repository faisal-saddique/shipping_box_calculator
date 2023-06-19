import streamlit as st
import pandas as pd
from utils import convert_data_to_boxes
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.switch_page_button import switch_page

with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def main():
    st.header("PACK A SHIPMENT")
    st.write("New box size - not based on what's available in the library")


    col1, col2, col3 = st.columns([0.2,0.3,0.5])
    with col1:
        length = st.number_input(f"ORDER NUMBER", value=0, step=1)
    with col2:
        orient_choice = st.selectbox("CALCULATION MODE",["EQUALIZE WEIGHT IF MULTIPLE BOXES NEEDED","UTILIZE ALL SPACE IN FIRST BOX IF MULTIPLE BOXES ARE NEEDED"])
    with col3:
        colA, colB, colC = st.columns(3)
        with colA:
            length = st.number_input(f"L", value=25, step=1)
        with colB:
            width = st.number_input(f"W", value=25, step=1)
        with colC:
            height = st.number_input(f"H", value=25, step=1)

        st.session_state["maximum_dimensions"] = (length,width,height)

    if "library_boxes" in st.session_state:
        library_boxes = st.session_state["library_boxes"]

        # for box in library_boxes:
        #     st.write(box.dimensions)

        box_df = pd.DataFrame(
            [
                {
                    "BOX": "",
                    "ROTATION OK": False,
                },
            ],
        )

        box_df_edited = st.data_editor(
            box_df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "BOX": st.column_config.SelectboxColumn(
                    help="The boxes as described in the library",
                    width="medium",
                    options=[
                        box.dimensions for box in library_boxes
                    ],
                )
            },
            hide_index=True,
        )

        # st.json(box_df_edited.to_dict())

        box_df_for_verification = []

        def get_selected_items(box_df_edited, library_boxes):
            box_df_for_display = pd.DataFrame(columns=["BOX", "LENGTH", "WIDTH", "HEIGHT", "MAXIMUM WEIGHT", "ROTATION OK"])

            for box_size, box_rotation in zip(box_df_edited["BOX"], box_df_edited["ROTATION OK"]):
                for prod in library_boxes:
                    # st.write(f"{(prod.dimensions)} == {(tuple(box_size.split(',')))}")
                    # st.write(tuple([int(num) for num in box_size.split(',')]))
                    try:
                        if prod.dimensions == tuple([float(num) for num in box_size.split(',')]):
                            box_dimensions = prod.dimensions
                            box_weight = prod.max_weight

                            box_data = {
                                "BOX": box_size,
                                "LENGTH": box_dimensions[0],
                                "WIDTH": box_dimensions[1],
                                "HEIGHT": box_dimensions[2],
                                "MAXIMUM WEIGHT": box_weight,
                                "ROTATION OK": box_rotation,
                            }

                            # st.write(box_data)
                            box_df_for_display = pd.concat([box_df_for_display, pd.DataFrame(box_data, index=[0])], ignore_index=True)
                            break
                    except:
                        box_df_for_display = pd.DataFrame(columns=["BOX", "LENGTH", "WIDTH", "HEIGHT", "MAXIMUM WEIGHT", "ROTATION OK"])

            return box_df_for_display

        box_df_for_verification = get_selected_items(box_df_edited=box_df_edited,library_boxes=library_boxes)
        st.subheader("REVIEW")
        st.dataframe(box_df_for_verification,use_container_width=True)
        st.session_state["final_boxes"] = convert_data_to_boxes(box_df_for_verification.to_dict())
        # for box in st.session_state["final_boxes"]:
        #     st.write(box)
        st.session_state["boxes_selected"] = True

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Change Items",use_container_width=True):
                switch_page("Pack A Shipment")
        with col2:
            if st.button("Calculate",use_container_width=True):
                switch_page("Packing Manifest")
    else:
        st.warning("Please enter the Boxes first in the library!")

if __name__ == "__main__":
    main()