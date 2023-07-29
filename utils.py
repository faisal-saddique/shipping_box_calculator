import copy
import itertools
import pandas as pd
import streamlit as st
import math

total_pages = 6

class Product:
    def __init__(self, sku, dimensions, weight, quantity=1, rotation=False):
        self.sku = sku
        self.dimensions = dimensions
        self.weight = weight
        self.quantity = quantity
        self.rotation = rotation

    def __str__(self):
        return f"Product: {self.sku}, Dimensions: {self.dimensions}, Weight: {self.weight}, Quantity: {self.quantity}, Rotation: {self.rotation}"

    def __eq__(self, other):
        if isinstance(other, Product):
            return self.sku == other.sku and self.dimensions == other.dimensions and self.weight == other.weight
        return False

    def volume(self):
        return self.dimensions[0] * self.dimensions[1] * self.dimensions[2]
    
class Box:
    def __init__(self, dimensions, max_weight=45):
        self.dimensions = dimensions  # (length, width, height)
        self.max_weight = max_weight
        self.current_weight = 0
        self.items = []

    def __str__(self):
        description = f"Box: {self.dimensions}, Max weight: {self.max_weight}, Utilized weight: {self.current_weight}"
        items = {}
        for item in self.items:
            if item.sku not in items.keys():
                items[item.sku] = 1
            else:
                items[item.sku] += 1

        description = description + f" Items packed: {items}"
        return description

    def can_fit(self, item, padding=(0, 0, 0)):
        remaining_volume = self.volume(padding) - sum(item.volume() for item in self.items)
        return (
            self.current_weight + item.weight <= self.max_weight
            and remaining_volume >= item.volume()
        )


    def add_item(self, item):
        self.items.append(item)
        self.current_weight += item.weight

    def volume(self, padding=(0, 0, 0)):
        padded_length = self.dimensions[0] - 2 * padding[2]
        padded_width = self.dimensions[1] - 2 * padding[2]
        padded_height = self.dimensions[2] - padding[0] - padding[1]
        return padded_length * padded_width * padded_height

    def get_accom_items(self):
        items = {}
        for item in self.items:
            if item.sku not in items.keys():
                items[item.sku] = 1
            else:
                items[item.sku] += 1
        # print(items)
        return items

def pack_items(items_param, boxes, padding, consider_maximum_dimensions=False):



    if not consider_maximum_dimensions:

        items = copy.deepcopy(items_param)
        boxes = copy.deepcopy(boxes)

        # Sort boxes and items by weight
        boxes.sort(key=lambda box: box.volume(), reverse=True)
        items.sort(key=lambda item: item.weight, reverse=True)

        # for it in boxes:
        #     st.warning(it)

        # for it in items:
        #     st.error(it)

        remaining_items = copy.deepcopy(items)

        # for it in remaining_items:
        #     st.success(it)

        selected_boxes = []

        for box in boxes:
            # st.success(box)

            for item in items:

                # st.success(item)

                # st.write(f"{item} item and {rem_item} rem items")

                while item.quantity > 0 and box.can_fit(item, padding):
                    box.add_item(item)
                    item.quantity -= 1

                if item.quantity == 0:
                    # st.write(item)
                    for rem_item in remaining_items:
                        if rem_item.sku == item.sku:
                            remaining_items.remove(rem_item)
                            break

            selected_boxes.append(box)

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
                "ITEMS ACCOMMODATED": box.get_accom_items()
            }

            filled_boxes.append(box_data)

        df = pd.DataFrame(filled_boxes)
        st.dataframe(df)

        if remaining_items:
            st.write("Products still left to pack:")
            for item in remaining_items:
                st.warning(item)

    else:
        items = copy.deepcopy(items_param)

        volume = 0
        for item in items:
            volume += item.volume() * item.quantity

        # st.success(f"Complete volume is: {volume}")

        max_dimensions_tuple = st.session_state.maximum_dimensions

        best_combination = None
        best_difference = float('inf')  # Initialize with positive infinity

        for length in range(1, max_dimensions_tuple[0] + 1 - 2 * padding[2]):
            for width in range(1, max_dimensions_tuple[1] + 1 - 2 * padding[2]):
                for height in range(1, max_dimensions_tuple[2] + 1 - padding[0] - padding[1]):
                    # st.write(f"testing: {max_dimensions_tuple[0] + 1 - 2 * padding[2]} == {max_dimensions_tuple[1] + 1 - 2 * padding[2]} == {max_dimensions_tuple[2] + 1 - padding[0] - padding[1]}")
                    current_volume = length * width * height
                    difference = abs(current_volume - volume)

                    if difference == 0:
                        best_combination = (length + 2 * padding[2], width + 2 * padding[2], height + padding[0] + padding[1])  # Perfect match found
                    elif difference < best_difference:
                        best_combination = (length + 2 * padding[2], width + 2 * padding[2], height + padding[0] + padding[1])
                        best_difference = difference

        if any(x - y for x, y in zip(best_combination, max_dimensions_tuple)):
            st.success(f"The dimensions of best fit box size are: {best_combination}")
        else:
            st.error(best_combination)
            st.error("No valid combination found within the given limits.")
            
def skip_sub_data_frame_loadups(page_number: int):
    for pno in range(1,total_pages+1):
        if pno == int(page_number):
            # st.success(st.session_state[f"allow_first_time_load_page_{pno}"])
            continue
        st.session_state[f"allow_first_time_load_page_{pno}"] = True
        # st.error(f"allow_first_time_load_page_{pno} = True")


def convert_data_to_boxes(parsed_data):
    boxes = []

    for i, dimensions in parsed_data["BOX"].items():
        dimensions = tuple(map(int, dimensions.split(",")))
        max_weight = parsed_data["MAXIMUM WEIGHT"][i]
        box = Box(dimensions, max_weight)
        boxes.append(box)

    return boxes

def get_selected_items(items_df_edited, library_products):
    items_df_for_display = pd.DataFrame(columns=["SKU", "LENGTH (In)", "WIDTH (In)", "HEIGHT (In)", "WEIGHT (lbs)", "QTY", "ROTATION OK"])

    for item_sku, item_qnt, item_rotation in zip(items_df_edited["SKU"], items_df_edited["QTY"], items_df_edited["ROTATION OK"]):
        for prod in library_products:
            if prod.sku == item_sku:
                item_dimensions = prod.dimensions
                item_weight = prod.weight
                # st.warning(item_qnt)
                item_data = {
                    "SKU": item_sku,
                    "LENGTH (In)": item_dimensions[0],
                    "WIDTH (In)": item_dimensions[1],
                    "HEIGHT (In)": item_dimensions[2],
                    "WEIGHT (lbs)": item_weight,
                    "QTY": 1 if item_qnt is None or math.isnan(item_qnt) else item_qnt,
                    "ROTATION OK": False if item_rotation is None else item_rotation,
                }

                # st.write(item_data)
                items_df_for_display = pd.concat([items_df_for_display, pd.DataFrame(item_data, index=[0])], ignore_index=True)
                break

    return items_df_for_display

def convert_data_to_products(parsed_data):
    products = [
        Product(
            sku=parsed_data["SKU"][i],
            dimensions=(
                parsed_data["LENGTH (In)"][i],
                parsed_data["WIDTH (In)"][i],
                parsed_data["HEIGHT (In)"][i]
            ),
            weight=parsed_data["WEIGHT (lbs)"][i],
            quantity=int(parsed_data["QTY"][i]) if parsed_data["QTY"][i] else 1,
            rotation=bool(parsed_data["ROTATION OK"][i])
        )
        for i in parsed_data["SKU"]
    ]

    return products


def create_products_from_library(data):
    products = []
    skus = data['SKU']
    lengths = data['LENGTH (In)']
    widths = data['WIDTH (In)']
    heights = data['HEIGHT (In)']
    weights = data['WEIGHT (lbs)']

    # Determine the starting index based on the keys
    starting_index = 0 if 0 in skus else 1

    # Ensure the lengths, widths, heights, and weights have the same number of entries
    num_entries = len(skus)
    if len(lengths) != num_entries or len(widths) != num_entries or len(heights) != num_entries or len(weights) != num_entries:
        raise ValueError("Invalid data format. Lengths, widths, heights, and weights should have the same number of entries.")

    for i in range(starting_index, num_entries + starting_index):
        sku = skus[i]
        dimensions = (lengths[i], widths[i], heights[i])
        weight = weights[i]
        product = Product(sku, dimensions, weight)
        products.append(product)

    return products


def create_boxes_from_library(data):
    boxes = []
    box_sizes = data['BOX SIZE']
    lengths = data['LENGTH (In)']
    widths = data['WIDTH (In)']
    heights = data['HEIGHT (In)']
    max_weight = data['MAXIMUM WEIGHT']
    # Determine the starting index based on the keys
    starting_index = 0 if 0 in box_sizes else 1

    # Ensure the box_sizes, lengths, widths, and heights have the same number of entries
    num_entries = len(box_sizes)
    if len(lengths) != num_entries or len(widths) != num_entries or len(heights) != num_entries:
        raise ValueError("Invalid data format. Box sizes, lengths, widths, and heights should have the same number of entries.")

    for i in range(starting_index, num_entries + starting_index):
        dimensions = (lengths[i], widths[i], heights[i])
        
        box = Box(dimensions, max_weight=max_weight[i])
        boxes.append(box)

    return boxes

def box_volume(box):
    return box.dimensions[0] * box.dimensions[1] * box.dimensions[2]


def add_box_sizes():
    return [Box((10, 10, 10), 20), Box((15, 15, 15), 30), Box((20, 20, 20), 35)]


def add_products():
    return [
        Product("Planner", (7.25, 8.5, 0.75), 0.5, 8),
        Product("Large Notepad", (8.5, 11, 0.25), 0.3, 4),
        Product("Small Notepad", (4.25, 5.5, 0.25), 0.1, 8),
        Product("Greeting Card", (4.25, 5.5, 0.03125), 0.01, 180)
    ]


def can_fit(product, box, padding):
    return all(
        d_box >= d_product + 2 * padding
        for d_box, d_product in zip(box.dimensions, product.dimensions)
    ) and product.weight <= box.max_weight - box.utilized_weight


def packing_strategy(products, available_boxes, option=1, padding=2):

    print(products)

    total_weight = sum(p.weight * p.quantity for p in products)
    total_volume = sum(box_volume(p) * p.quantity for p in products)
    total_dimensions = [max(p.dimensions[i] for p in products) + 2 * padding for i in range(3)]

    if option == 1:
        best_fit_boxes = []
        for box in available_boxes:
            if (
                all(d_box >= d_total for d_box, d_total in zip(box.dimensions, total_dimensions))
                and total_weight <= box.max_weight
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


if __name__ == "__main__":
    available_boxes = add_box_sizes()
    product_library = add_products()
    padding = 1  # Padding amount, you can change this value as needed

    print("Available boxes:")
    for box in available_boxes:
        print(box)

    print("\nProduct library:")
    for product in product_library:
        print(product)

    option = int(input("Enter 1 to find the best box size based on available boxes or 2 to find the best box size based on any box size: "))
    result = packing_strategy(product_library, available_boxes, option, padding)
    if result:
        print("\nBest estimated packing arrangement:")
        print(f"Box: {result.dimensions} Utilized weight: {result.utilized_weight}")
    else:
        print("\nNo packing arrangement found for the given products and boxes.")