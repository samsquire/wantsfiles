wantsfile = """wants:
- group_name: groceries
  delivery: £5
  wants:
    - name: 4 pints semi skimmed milk
      price: £1.50
      quantity: 1
    - name: 100g milk chocolate
      price: £1.50
      quantity: 1
"""

sellfile = """sell:
- name: 4 pints semi skimmed milk
  price: £1.43
- name: 4 pints semi skimmed milk
  price: £1.46
- name: 4 pints semi skimmed milk
  price: £1.48
- name: 100g milk chocolate
  price: £1.50
- name: 100g milk chocolate
  price: £1.60
"""

import yaml
from operator import itemgetter
import collections
from pprint import pprint
products = collections.defaultdict(dict)

wantsfile = yaml.safe_load(wantsfile)

for group in wantsfile["wants"]:
    for product in group["wants"]:
        product_name = product["name"]
        if "buy" not in products[product_name]:
            products[product_name]["buy"] = []
        products[product_name]["buy"].append(product)
        product["group_name"] = group["group_name"]

for product in yaml.safe_load(sellfile)["sell"]:
    product_name = product["name"]
    if "sell" not in products[product_name]:
            products[product_name]["sell"] = []
    products[product_name]["sell"].append(product)

pprint(products)
matched_products = []
# order matching
for product, value in products.items():
    for index, item in enumerate(value["buy"]):
        item["index"] = index
        item["price"] = int(float(re.sub("[^-0-9.,]", '', item["price"])) * 100)
    for index, item in enumerate(value["sell"]):
        item["index"] = index
        item["price"] = int(float(re.sub("[^-0-9.,]", '', item["price"])) * 100)
    value["buy"].sort(key=lambda x: (x["price"], x["index"]), reverse=True)
    value["sell"].sort(key=lambda x: (x["price"], x["index"]))
    
    pprint(value["buy"])
    pprint(value["sell"])
    
    first_buy = value["buy"][0]
    first_sell = value["sell"][0]
    
    if first_buy["price"] >= first_sell["price"]:
        print("{}: buy {} matches with sell {}".format(product, first_buy["price"], first_sell["price"]))
        price = (first_buy["price"] + first_sell["price"]) / 2
        matched_purchase = (price, first_buy, first_sell)
        matched_products.append(matched_purchase)
        first_buy["matched"] = matched_purchase
    else:
        print("Failed to match")

for group in wantsfile["wants"]:
    if all(map(lambda product: product.get("matched") is not None, group["wants"])):
        print(group["group_name"], "is satisfied")
        



        
