class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

catalog = {
    "Product A": Product("Product A", 20),
    "Product B": Product("Product B", 40),
    "Product C": Product("Product C", 50)
}

discount_rules = {
    "flat_10_discount": {
        "cart_total": 200,
        "discount_amount": 10
    },
    "bulk_5_discount": {
        "quantity_threshold": 10,
        "discount_percentage": 5
    },
    "bulk_10_discount": {
        "total_quantity_threshold": 20,
        "discount_percentage": 10
    },
    "tiered_50_discount": {
        "total_quantity_threshold": 30,
        "single_product_quantity_threshold": 15,
        "discount_percentage": 50
    }
}

gift_wrap_fee = 1
shipping_fee_per_package = 5
max_units_per_package = 10

def calculate_discount(cart_total, cart_items):
    applicable_discounts = []
    for rule, params in discount_rules.items():
        if rule == "flat_10_discount" and cart_total > params["cart_total"]:
            applicable_discounts.append((rule, params["discount_amount"]))
        elif rule == "bulk_5_discount":
            for item in cart_items:
                if item["quantity"] > params["quantity_threshold"]:
                    discount_amount = item["price"] * item["quantity"] * params["discount_percentage"] / 100
                    applicable_discounts.append((rule, discount_amount))
        elif rule == "bulk_10_discount" and sum(item["quantity"] for item in cart_items) > params["total_quantity_threshold"]:
            discount_amount = cart_total * params["discount_percentage"] / 100
            applicable_discounts.append((rule, discount_amount))
        elif rule == "tiered_50_discount" and sum(item["quantity"] for item in cart_items) > params["total_quantity_threshold"]:
            for item in cart_items:
                if item["quantity"] > params["single_product_quantity_threshold"]:
                    discount_amount = (item["quantity"] - params["single_product_quantity_threshold"]) * item["price"] * params["discount_percentage"] / 100
                    applicable_discounts.append((rule, discount_amount))

    if applicable_discounts:
        return max(applicable_discounts, key=lambda x: x[1])
    else:
        return None

def calculate_shipping_fee(cart_items):
    total_units = sum(item["quantity"] for item in cart_items)
    total_packages = total_units // max_units_per_package
    if total_units % max_units_per_package != 0:
        total_packages += 1
    return total_packages * shipping_fee_per_package

def calculate_total(cart_items, discount_amount, shipping_fee, gift_wrap_fee):
    subtotal = sum(item["quantity"] * item["price"] for item in cart_items)
    total = subtotal - discount_amount + shipping_fee + gift_wrap_fee
    return total,subtotal

def print_receipt(cart_items, discount_name, discount_amount, shipping_fee, gift_wrap_fee, total, subtotal):
    print("Product\t\tQuantity\tTotal")
    for item in cart_items:
        print(f"{item['name']}\t\t{item['quantity']}\t\t{item['quantity'] * item['price']}")
    print(f"\nSubtotal: {subtotal}")
    print(f"Discount Applied: {discount_name}\t-{discount_amount}")
    print(f"Shipping Fee: {shipping_fee}")
    print(f"Gift Wrap Fee: {gift_wrap_fee}")
    print(f"\nTotal: {total}")

def main():
    cart_items = []
    for product_name, product in catalog.items():
        quantity = int(input(f"Enter the quantity of {product_name}: "))
        is_gift_wrapped = input(f"Is {product_name} wrapped as a gift? (yes/no): ").lower() == "yes"
        if quantity > 0:
            cart_items.append({
                "name": product_name,
                "price": product.price,
                "quantity": quantity,
                "is_gift_wrapped": is_gift_wrapped
            })
    
    discount = calculate_discount(sum(item["quantity"] * item["price"] for item in cart_items), cart_items)
    discount_name = "No Discount"
    discount_amount = 0
    if discount:
        discount_name, discount_amount = discount
    
    shipping_fee = calculate_shipping_fee(cart_items)
    
    total = calculate_total(cart_items, discount_amount, shipping_fee, gift_wrap_fee)
    
    print_receipt(cart_items, discount_name, discount_amount, shipping_fee, gift_wrap_fee, total[0],total[1])

if __name__ == "__main__":
    main()
