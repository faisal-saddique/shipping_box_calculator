import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import copy

class Box:
    def __init__(self, dimensions, max_weight=45):
        self.dimensions = dimensions  # (length, width, height)
        self.max_weight = max_weight
        self.utilized_weight = 0

    def __str__(self):
        return f"Box: {self.dimensions}, Max weight: {self.max_weight}, Utilized weight: {self.utilized_weight}"

def box_volume(box):
    return box.dimensions[0] * box.dimensions[1] * box.dimensions[2]

def can_fit(product, box, padding):
    return all(
        d_box >= d_product + 2 * padding
        for d_box, d_product in zip(box.dimensions, product.dimensions)
    ) and product.weight <= box.max_weight - box.utilized_weight


def packing_strategy(products, available_boxes, option=1, padding=2):

    st.write(products)

    total_weight = sum(p.weight * p.quantity for p in products)
    total_volume = sum(box_volume(p) * p.quantity for p in products)
    total_dimensions = [max(p.dimensions[i] for p in products) + 2 * padding for i in range(3)]

    if option == 1:
        best_fit_boxes = []
        for box in available_boxes:
            if (
                all(d_box >= d_total for d_box, d_total in zip(box.dimensions, total_dimensions))
                and total_weight <= float(box.max_weight)
                and total_volume <= box_volume(box)
            ):
                best_fit_boxes.append(box)

        if not best_fit_boxes:
            return None  # No packing arrangement found for the given products and boxes

        best_fit_boxes.sort(key=lambda x: box_volume(x) - total_volume)
        for box in best_fit_boxes:
            if total_weight <= box.max_weight - box.utilized_weight:
                box.utilized_weight = total_weight
                return box

    elif option == 2:
        max_dimensions = input("Enter the maximum dimensions (length, width, height) allowed for the box: ")
        max_weight = input("Enter the maximum weight allowed for the box: ")
        max_dimensions = tuple(map(float, max_dimensions.split(',')))
        max_weight = float(max_weight)

        best_fit_box = None
        min_volume_diff = float("inf")

        for box in available_boxes:
            if (
                all(d_box <= d_max for d_box, d_max in zip(box.dimensions, max_dimensions))
                and box.max_weight <= max_weight
            ):
                can_fit_all_products = True
                total_weight = 0

                for product in products:
                    if can_fit(product, box, padding):
                        total_weight += product.weight * product.quantity
                    else:
                        can_fit_all_products = False
                        break

                if can_fit_all_products and total_weight <= box.max_weight:
                    volume_diff = box_volume(box) - sum(box_volume(p) * p.quantity for p in products)
                    if volume_diff < min_volume_diff:
                        min_volume_diff = volume_diff
                        best_fit_box = copy.deepcopy(box)
                        best_fit_box.utilized_weight = total_weight

        if not best_fit_box:
            custom_box_dimensions = [max(p.dimensions[i] for p in products) + 2 * padding for i in range(3)]
            total_weight = sum(p.weight * p.quantity for p in products)
            best_fit_box = Box(custom_box_dimensions, total_weight)
            best_fit_box.utilized_weight = total_weight

        return best_fit_box

    else:
        return None  # Invalid option
    
st.write("Available boxes:")
for box in st.session_state["final_boxes"]:
    st.write(box)

st.write("\nProduct library:")
for product in st.session_state["final_items"]:
    st.write(product)

result = packing_strategy(products=st.session_state["final_items"],available_boxes=st.session_state["final_boxes"],option=2)

if result:
    st.write("\nBest estimated packing arrangement:")
    st.write(f"Box: {result.dimensions} Utilized weight: {result.utilized_weight}")
else:
    st.write("\nNo packing arrangement found for the given products and boxes.")