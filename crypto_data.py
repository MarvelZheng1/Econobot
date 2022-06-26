from requests.exceptions import HTTPError
import krakenex

kraken = krakenex.API()


def checkValidity(id): #false means invalid, true means valid
    try:
        response = kraken.query_public('Depth', {'pair': id, 'count': '500'})
        bids = response['result'][list(response["result"].keys())[0]]['bids']
        return True
    except KeyError:
        return False


def findMarketDepth(pair):
    try:
        response = kraken.query_public('Depth', {'pair': pair, 'count': '500'})
        bids = response['result'][list(response["result"].keys())[0]]['bids']
        asks = response['result'][list(response["result"].keys())[0]]['asks']
    except HTTPError as e:
        print(str(e))

    def findSubtotals(results):
        orders = {}
        for i in results:
            orders[float(i[0])] = float(i[1])

        sum = 0
        for value in orders.keys():
            sum += value
        marketPrice = sum/500

        total = 0
        for value in orders.keys():
            weighted = 1/((abs((value-marketPrice)/marketPrice))+1)*orders[value]
            total += weighted
        return total
    
    return(findSubtotals(asks) + findSubtotals(bids))


def findAveragePrice(pair):
    try:
        response = kraken.query_public('Depth', {'pair': pair, 'count': '500'})
        asks = response['result'][list(response["result"].keys())[0]]['asks']
    except HTTPError as e:
        print(str(e))
    sum = 0
    for i in asks:
        sum += float(i[0])
    return sum / 500
