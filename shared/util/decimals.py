from decimal import Decimal

def count_decimal_places_decimal(number):
    d = Decimal(str(number))
    return max(0, -d.as_tuple().exponent)