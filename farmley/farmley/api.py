from __future__ import unicode_literals
import logging
from pprint import pprint
import frappe
import json
import collections
import requests


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
def sales_order():
    return frappe.db.sql("")


# payload = {"order_type": "Sales",
#            "customer_name": "32+Degree+Studio",
#            "customer": "A. K. Trading",
#            "customer_address": "Head Office-Maharashtra-400015-Shipping",
#            "transaction_date": "2021-09-07",
#            "items": [{
#                "item_code": "Almonds-1-10",
#                "item_name": "Premium Almond Blanched Sliced Farmley Carton Box 15KG",
#                "delivery_date": "2021-09-07",
#                "qty": "1",
#                "rate": "230"
#            }]
#            }

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


##create customer

@frappe.whitelist()
def save_customer():
    url1 = "http://localhost:8000/api/resource/Customer"
    header1 = {"Authorization": "Token 9e820d1621292f3:e40525854287561",
               "Accept": "application/json",
               "Content-Type": "application/json"}

    body = {
        "data": {
            "customer_name": "dexciss"
        }

    }
    r1 = requests.post(url=url1, headers=header1, data=json.dumps(body))
    json_data = json.loads(r1.content.decode('utf-8'))

    return r1, json_data


@frappe.whitelist()
def rough():
    url1 = "http://localhost:8000/api/method/frappe.desk.doctype.tag.tag.add_tag"
    header1 = {"Authorization": "Token 9e820d1621292f3:e40525854287561",
               "Accept": "application/json",
               "Content-Type": "application/json"}

    tag_payload = {"tag": "website", "dt": "Sales Order", "dn": "SAL-ORD-2021-00017"}
    r1 = requests.post(url=url1, headers=header1, data=json.dumps(tag_payload))
    json_data = json.loads(r1.content.decode('utf-8'))

    return r1, json_data
