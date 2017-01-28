def ruleofthree(loop):
    """..."""
    value_price = 0
    value_size = 0
    most_value = 0
    for _ in range(loop):
        price = float(input())
        size = float(input())
        value = size/price
        if value >= most_value:
            if value == most_value:
                if price < value_price:
                    value_price = price
                    value_size = size
            else:
                value_price = price
                value_size = size
            most_value = value
    print("%.2f" %value_price, "%.2f" %value_size)
ruleofthree(int(input()))
