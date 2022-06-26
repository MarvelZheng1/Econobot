

def findSubtotals(results):
    orders = {}
    for i in results:
        orders[float(i[0])] = float(i[1])

    sum = 0
    for value in orders.keys():
        sum += value
    marketPrice = sum/50

    total = 0
    for value in orders.keys():
        weighted = 1/((abs((value-marketPrice)/marketPrice))+1)*orders[value]
        total += weighted
    return total


def findMarketDepth(asks, bids):
    return findSubtotals(asks) + findSubtotals(bids)
