import copy
import itertools

class Product:
    def __init__(self, sku, dimensions, weight, quantity=1, rotation=False):
        self.sku = sku
        self.dimensions = dimensions
        self.weight = weight
        self.quantity = quantity
        self.rotation = rotation

    def __str__(self):
        return f"Product: {self.sku}, Dimensions: {self.dimensions}, Weight: {self.weight}, Quantity: {self.quantity}, Rotation: {self.rotation}"

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

def convert_data_to_boxes(parsed_data):
    boxes = []

    for i, dimensions in parsed_data["BOX"].items():
        dimensions = tuple(map(int, dimensions.split(",")))
        max_weight = parsed_data["MAXIMUM WEIGHT"][i]
        box = Box(dimensions, max_weight)
        boxes.append(box)

    return boxes

def convert_data_to_products(parsed_data):
    products = [
        Product(
            sku=parsed_data["SKU"][i],
            dimensions=(
                parsed_data["LENGTH"][i],
                parsed_data["WIDTH"][i],
                parsed_data["HEIGHT"][i]
            ),
            weight=parsed_data["WEIGHT"][i],
            quantity=int(parsed_data["QTY"][i]) if parsed_data["QTY"][i] else 1,
            rotation=bool(parsed_data["ROTATION OK"][i])
        )
        for i in parsed_data["SKU"]
    ]

    return products


def create_products_from_library(data):
    products = []
    skus = data['SKU']
    lengths = data['LENGTH (in)']
    widths = data['WIDTH']
    heights = data['HEIGHT']
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
    lengths = data['LENGTH (in)']
    widths = data['WIDTH']
    heights = data['HEIGHT']
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