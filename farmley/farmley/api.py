from __future__ import unicode_literals
import collections
import json
import logging

import requests
import frappe


@frappe.whitelist()
def product_details_for_website(name=None, productCategoryName=None, productName=None):
    """
    param:productId, productCategory, productName, source
    return: products_json
    #  This api will return the website_product views details
    """
    sql_query = "select name,product_code,product_name,product_category,packaging_size, selling_rate,media_url, " \
                "hsn_code, barcode,parent_product_media_url from website_products"
    where = " where "
    _and = " and "

    if name is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "name = \'{}\'".format(name)
    if productCategoryName is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "product_category like \'%{}%\'".format(productCategoryName)
    if productName is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "product_name like \'%{}%\'".format(productName)

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
        d['parentProductMediaUrl'] = row[9]
        products_json.append(d)
    return products_json


@frappe.whitelist()
def open_product_category(source=None):
    """
        param:source
        return:product_category
        # it will return the distinct product category to filter on frontend
    """
    sql_query = "select DISTINCT (product_category) from website_products"
    _and = " and "
    where = " where "
    if source is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "price_list like \'%{}%\'".format(source)
    db_data = frappe.db.sql(sql_query)
    product_category_json = []
    for row in db_data:
        d = collections.OrderedDict()
        d['productCategory'] = row[0]
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
                "from tabAddress "
    where = " where "
    _and = " and "
    if phoneNumber is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "phone = \'{}\'".format(phoneNumber)
    if customerCode is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "name = \'{}\'".format(customerCode)
    if emailId is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "email_id = \'{}\'".format(emailId)
    addresses = frappe.db.sql(sql_query)
    addresses_json = []
    for row in addresses:
        d = collections.OrderedDict()
        d['label'] = row[0]
        d['name'] = row[1]
        d['cityName'] = row[2]
        d['stateName'] = row[3]
        d['countryName'] = row[4]
        d['pincode'] = row[5]
        d['contactName'] = row[6]
        d['contactNumber'] = row[7]
        d['line1'] = row[8]
        d['line2'] = row[9]
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
