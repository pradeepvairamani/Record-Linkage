# Design decisions : Deterministic vs probabilistic (Choose deterministic rule based method because the data looked relatively clean)
import json
from fuzzywuzzy import fuzz


def read_data():
    products = []
    listings = []

    with open("challenge_data_20110429/products.txt", 'rb') as line_products:
        for product in line_products:
            product = product.decode('utf-8').strip()
            products.append(json.loads(product))

    with open("challenge_data_20110429/listings.txt", 'rb') as line_listings:
        for listing in line_listings:
            listing = listing.decode('utf-8').strip()
            listings.append(json.loads(listing))

    return (products, listings)


def get_product_manufacturers(products):
    product_manufacturers = set()
    for p in products:
        product_manufacturers.add(p['manufacturer'])
    return list(product_manufacturers)


def match_listing_product_manufacturer(listing_manufacturer, product_manufacturers):
    listing_manufacturer = listing_manufacturer.lower()

    for p in product_manufacturers:
        p = p.lower()
        if 'fuji' in listing_manufacturer:
            return "fujifilm"
        if p in listing_manufacturer:
            return p
        else:
            None


if __name__ == "__main__":
    (products, listings) = read_data()
    product_manufacturers = get_product_manufacturers(products)
    ans_temp = {}
    count = 0
    for p in products:
        count += 1
        print('Product number ' + str(count) + ' in progress')

        for l in listings:
            product_manufacturer = match_listing_product_manufacturer(l['manufacturer'], product_manufacturers)
            if product_manufacturer == p['manufacturer'].lower():
                if fuzz.partial_ratio(l['title'], p['model']) > 90:
                    if p['product_name'] not in ans_temp:
                        ans_temp[p['product_name']] = []
                    ans_temp[p['product_name']].append(l)
    with open('results.txt', "w", encoding='utf-8') as output:
        for k in ans_temp:
            ans = {}
            ans['product_name'] = k
            ans['listings'] = ans_temp[k]
            output.write(str(ans))
            output.write('\n')
