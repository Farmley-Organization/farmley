from __future__ import unicode_literals
import collections
import json
import requests
import frappe


@frappe.whitelist()
def product_details_for_website(productId=None, productCategory=None, productName=None, source=None):
    """
    param:productId, productCategory, productName, source
    return: products_json
    #  This api will return the website_product views details
    """
    sql_query = "select name,product_code,product_name,product_category,packaging_size, selling_rate,media_url, " \
                "hsn_code, barcode from website_products"
    where = " Where "
    _and = " and "
    sql_query = sql_query + where + "name = '{}'".format(productId) if productId is not None else sql_query
    if productCategory is not None and productId is None:
        sql_query = sql_query + where + "product_category like \'%{}%\'".format(
            productCategory) + _and + "product_name like \'%{}%\'".format(
            productName) if productName is not None else sql_query + where + "product_category like \'%{}%\'".format(
            productCategory)
    elif productCategory is None and productId is None:
        sql_query = sql_query + where + "product_name like \'%{}%\'".format(
            productName) if productName is not None else sql_query

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
    return sql_query, products_json


@frappe.whitelist()
def open_product_category(source=None):
    """
        param:source
        return:product_category
        # it will return the distinct product category to filter on frontend
    """
    sql_query = "select DISTINCT (product_category) from `_a94a8fe5ccb19ba6`.website_products"
    if source is not None:
        sql_query = "select DISTINCT (product_category) from `_a94a8fe5ccb19ba6`.website_products where price_list " \
                    "like \'%{}%\'".format(source)
    db_data = frappe.db.sql(sql_query)
    product_category_json = []
    for row in db_data:
        d = collections.OrderedDict()
        d['product_category'] = row[0]
        product_category_json.append(d)
    return product_category_json


@frappe.whitelist()
def customer_addresses(phoneNumber=None, emailId=None, customerCode=None):
    """
    param: phoneNumber,emailId,customerCode
    return:addresses
    # this api will return all the addresses belong to that customer
    """
    sql_query = "select address_title, name, city, state, country, pincode, contact_name, contact_number, address_line1, address_line2, locality " \
                "from `_a94a8fe5ccb19ba6`.tabAddress "
    where = " where "
    _and = " and "
    if phoneNumber is not None or emailId is not None or customerCode is not None:
        sql_query = sql_query + where + "phone =" + phoneNumber if phoneNumber is not None else sql_query
        sql_query = sql_query + where + "name = " + customerCode if phoneNumber is None and customerCode is not None else sql_query
        sql_query = sql_query + where + "email_id = " + "\'{}\'".format(emailId) if emailId is not None and phoneNumber is None and customerCode is None else sql_query
    print(sql_query)
    addresses = frappe.db.sql(sql_query)
    addresses_json = []
    for row in addresses:
        d = collections.OrderedDict()
        d['label'] = row[0]
        d['address_code'] = row[1]
        # d['organization_code'] = row[2]
        d['city_name'] = row[2]
        d['state_name'] = row[3]
        d['country_name'] = row[4]
        d['pincode'] = row[5]
        d['contact_name'] = row[6]
        d['contact_number'] = row[7]
        d['line_1'] = row[8]
        d['line_2'] = row[9]
        d['locality'] = row[10]
        addresses_json.append(d)
    return addresses_json


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
