warehouse = {"HP Omen 16": {'stock':10,'price':1000 },"Android Phone":{'stock':5,"price":500},"Apple Watch":{"stock":0,"price":300}}


def check_warehouse(device_name: str) -> dict:
    if device_name in warehouse:
        return warehouse[device_name]
    return {"Message": "Device Not Found in warehouse"}

def apply_discount(device_name:str,years_as_customer:int) -> dict:
    if device_name in warehouse:
        device_price = warehouse[device_name]['price']
        discount_to_provide = min(years_as_customer*0.05,.3)
        discount_price = device_price*discount_to_provide
        return device_price-discount_price
    return {"Message": "Device not found in warehouse"}