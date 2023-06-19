import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import copy
import pandas as pd

def pack_items(items, boxes, padding):

    items = copy.deepcopy(items)
    boxes = copy.deepcopy(boxes)
    
    # Sort boxes and items by weight
    boxes.sort(key=lambda box: box.max_weight, reverse=True)
    items.sort(key=lambda item: item.weight, reverse=True)

    remaining_items = copy.deepcopy(items)
    selected_boxes = []

    for box in boxes:
        for item in remaining_items:
            quantity = item.quantity
            while quantity > 0 and box.can_fit(item, padding):
                box.add_item(item)
                quantity -= 1
            if quantity == 0:
                remaining_items.remove(item)
            else:
                item.quantity = quantity
        selected_boxes.append(box)

    return selected_boxes, remaining_items

if "items_selected" in st.session_state and st.session_state["items_selected"] and "boxes_selected" in st.session_state and st.session_state["boxes_selected"]:
    
    st.header("PACKING MANIFEST")

    option = st.checkbox("Select Only from available boxes", value=False,
                         help="Choose whether to select only from available boxes or any box that is under the maximum dimensions specified.")
    col1, col2 = st.columns(2)
    with col1:
        sel_boxes = []
        st.write("Selected boxes:")
        for box in st.session_state["final_boxes"]:
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

    padding = (st.session_state["settings"]["top_padding"], st.session_state["settings"]["bottom_padding"], st.session_state["settings"]["sides_padding"])  # padding (top, bottom, 4 sides)
    
    selected_boxes, rem_items = pack_items(st.session_state["final_items"], st.session_state["final_boxes"],padding=padding)

    st.write("\nBest estimated packing arrangement:")
    filled_boxes = []
    for box in selected_boxes:
        if len(box.items) == 0:
            continue

        box_data = {
            "BOX NAME": f"{box.dimensions[0]}x{box.dimensions[1]}x{box.dimensions[2]}",
            "LENGTH": box.dimensions[0],
            "WIDTH": box.dimensions[1],
            "HEIGHT": box.dimensions[2],
            "MAXIMUM WEIGHT": box.max_weight,
            "UTILIZED WEIGHT": box.current_weight,
            "ITEMS ACCOMODATED": box.get_accom_items()
        }

        filled_boxes.append(box_data)

    df = pd.DataFrame(filled_boxes)
    st.dataframe(df)

    if rem_items:
        st.write("Products still left to pack:")
        for item in rem_items:
            st.warning(item)

else:
    st.warning("Please select the items and boxes first.")