from __future__ import unicode_literals
import collections
import json
import requests
import frappe


@frappe.whitelist()
def product_details_for_website(productCategory="", productName=""):
    sql_query = "select name,product_code,product_name,product_category,packaging_size, selling_rate,media_url, " \
                "hsn_code, barcode from website_products where product_category like \'%{}%\' and name like \'%{}%\'".format(
        productCategory, productName)

    db_data = frappe.db.sql(sql_query)
    products_json = []
    for row in db_data:
        d = collections.OrderedDict()
        d['name'] = row[0]
        d['productCode'] = row[1]
        d['productName'] = row[2]
        d['productCategory'] = row[3]
        d['packagingSize'] = row[4]
        d['sellingRate'] = row[5]
        d['mediaUrl'] = row[6]
        d['hsnCode'] = row[7]
        d['barcode'] = row[8]
        products_json.append(d)
    return products_json


@frappe.whitelist()
def save_orders(customer, customerAddress, transactionDate, itemCode, itemName, deliveryDate, qty, rate, source):
    headers = {"Authorization": "Token 9e820d1621292f3:e40525854287561",
               "Accept": "application/json",
               "Content-Type": "application/json"}
    payload = {"order_type": "Sales",
               "customer": customer,
               "customer_address": customerAddress,
               "transaction_date": transactionDate,
               "items": [{
                   "item_code": itemCode,
                   "item_name": itemName,
                   "delivery_date": deliveryDate,
                   "qty": qty,
                   "rate": rate
               }]
               }
    url = "http://localhost:8000/api/resource/Sales Order"

    save_orders_response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    save_orders_json_data = json.loads(save_orders_response.content.decode('utf-8'))

    # adding tag on order
    tag_url = "http://localhost:8000/api/method/frappe.desk.doctype.tag.tag.add_tag"
    tag_payload = {"tag": source, "dt": "Sales Order", "dn": save_orders_json_data["data"]["name"]}
    tag_response = requests.post(url=tag_url, data=json.dumps(tag_payload), headers=headers)
    tag_json_data = json.loads(tag_response.content.decode('utf-8'))
    return save_orders_json_data, tag_json_data




