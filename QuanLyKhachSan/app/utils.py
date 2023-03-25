def cart_stats(pay=None):
    total_amount = 0

    if pay:
        for c in pay.values():
            total_amount +=  c['price']

    return {
        'total_amount': total_amount,
    }