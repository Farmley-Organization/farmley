from __future__ import unicode_literals
import collections
import json
import logging

import requests

import erpnext
import frappe
from operator import itemgetter
import math


@frappe.whitelist()
def parent_product_details():
    sql_query = "select parent_product_name, product_code_erpnext, rate, product_category,parent_product_media,uuid,slug from parent_product_details"
    parent_product_list = frappe.db.sql(sql_query)
    parent_product_json = []
    for row in parent_product_list:
        d = collections.OrderedDict()
        d['parentProductName'] = row[0]
        d['productCodeErpnext'] = row[1]
        d['rate'] = row[2]
        d['productCategory'] = row[3]
        d['parentProductMedia'] = row[4]
        d['uuid'] = row[5]
        d['slug'] = row[6]
        parent_product_json.append(d)
    return parent_product_json


@frappe.whitelist()
def product_details(name=None, productCategoryName=None, productName=None, parentProductCode=None, pageNumber=0,
                    pageSize=10):
    """
    param:productId, productCategory, productName, source
    return: products_json
    #  This api will return the website_product views details
    """
    sql_query = "select name,product_code,product_name,product_category,packaging_size,media_url, " \
                "hsn_code, barcode,parent_product_media_url,`Standard Buying`,`Website MRP List`," \
                "`Website Price list`,`B2B Price List`,`Standard Selling`,uuid,slug,website_description,parent_product_code from product_details "
    count_query = "select COUNT(*) from product_details"
    where = " where "
    _and = " and "
    if name is not None:
        sql_query = sql_query + (_and if "where" in sql_query else where) + "name = \'{}\'".format(name)
        count_query = count_query + (_and if "where" in count_query else where) + "name = \'{}\'".format(name)
    if productCategoryName is not None:
        sql_query = sql_query + (_and if "where" in sql_query else where) + "product_category like \'%{}%\'".format(
            productCategoryName)
        count_query = count_query + (
            _and if "where" in count_query else where) + "product_category like \'%{}%\'".format(
            productCategoryName)
    if productName is not None:
        sql_query = sql_query + (_and if "where" in sql_query else where) + "product_name like \'%{}%\'".format(
            productName)
        count_query = count_query + (_and if "where" in count_query else where) + "product_name like \'%{}%\'".format(
            productName)
    if parentProductCode is not None:
        sql_query = sql_query + (_and if "where" in sql_query else where) + "parent_product_code = \'{}\'".format(
            parentProductCode)
        count_query = count_query + (_and if "where" in count_query else where) + "parent_product_code = \'{}\'".format(
            parentProductCode)
    sql_query = sql_query + "LIMIT {},{}".format(int(pageNumber) * int(pageSize), int(pageSize))
    count = frappe.db.sql(count_query)
    count = count[0][0]
    page = count / int(pageSize)
    total_pages = math.ceil(page)

    db_data = frappe.db.sql(sql_query)
    products_json = []
    p_json = {}
    for row in db_data:
        d = collections.OrderedDict()
        d['name'] = row[0]
        d['productCode'] = row[1]
        d['productName'] = row[2]
        d['productCategory'] = row[3]
        d['packagingSize'] = row[4]
        d['mediaUrl'] = row[5]
        d['hsnCode'] = row[6]
        d['barcode'] = row[7]
        d['parentProductMediaUrl'] = row[8]
        d['standardBuying'] = row[9]
        d['WebsiteMRPList'] = row[10]
        d["websitePriceList"] = row[11]
        d['B2BPriceList'] = row[12]
        d['standardSelling'] = row[13]
        d['uuid'] = row[14]
        d['slug'] = row[15]
        d['websiteDescription'] = row[16]
        d['parentProductCode'] = row[17]
        products_json.append(d)
    p_json["productData"] = products_json
    p_json["totalPages"] = total_pages
    return p_json


@frappe.whitelist()
def featured_product(tagName):
    """
        param:
        return:parent_product
    """

    featured_product_name = frappe.db.get_all(doctype="Item",
                                              filters=[["Item", "_user_tags", "LIKE", '%' + tagName + '%']],
                                              fields=["`tabItem`.name"])
    sql_query = "select name,product_code,product_name,product_category,packaging_size,media_url, " \
                "hsn_code, barcode,parent_product_media_url,`Standard Buying`,`Website MRP List`," \
                "`Website Price list`,`B2B Price List`,`Standard Selling`,uuid,slug from product_details "
    where = " where "
    list_of_name = list(map(itemgetter('name'), featured_product_name))

    sql_query = sql_query + where + " name in " + str(tuple(list_of_name))
    db_featured_product_details = frappe.db.sql(sql_query)
    featured_products_json = []
    for row in db_featured_product_details:
        d = collections.OrderedDict()
        d['name'] = row[0]
        d['productCode'] = row[1]
        d['productName'] = row[2]
        d['productCategory'] = row[3]
        d['packagingSize'] = row[4]
        d['mediaUrl'] = row[5]
        d['hsnCode'] = row[6]
        d['barcode'] = row[7]
        d['parentProductMediaUrl'] = row[8]
        d['standardBuying'] = row[9]
        d['WebsiteMRPList'] = row[10]
        d["websitePriceList"] = row[11]
        d['B2BPriceList'] = row[12]
        d['standardSelling'] = row[13]
        d['uuid'] = row[14]
        d['slug'] = row[15]
        featured_products_json.append(d)

    return featured_products_json


@frappe.whitelist()
def open_product_category():
    """
        param:source
        return:product_category
        # it will return the distinct product category to filter on frontend
    """
    sql_query = "select DISTINCT(product_category),product_category_name from product_details"
    # need media url here
    db_data = frappe.db.sql(sql_query)
    product_category_json = []
    for row in db_data:
        d = collections.OrderedDict()
        d['productCategory'] = row[0]
        d['productCategoryName'] = row[1]
        product_category_json.append(d)
    return product_category_json


@frappe.whitelist()
def customer_addresses(phoneNumber=None, emailId=None, name=None):
    """
    param: phoneNumber,emailId,customerCode
    return:addresses
    # this api will return all the addresses belong to that customer
    """

    sql_query = "select ta.address_title, ta.name, ta.city, ta.state, ta.country, ta.pincode, ta.phone,ta.address_line1, ta.address_line2, ta.locality, tl.link_name from tabAddress as ta "
    sql_query = sql_query + " LEFT JOIN `tabDynamic Link` as tl ON tl.parent = ta.name "
    where = " where "
    _and = " and "
    if phoneNumber is not None: sql_query = sql_query + (
        _and if "where" in sql_query else where) + "ta.phone = \'{}\'".format(phoneNumber)
    if name is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "ta.name = \'{}\'".format(
        name)
    if emailId is not None: sql_query = sql_query + (
        _and if "where" in sql_query else where) + "ta.email_id = \'{}\'".format(emailId)

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
        d['contactNumber'] = row[6]
        d['line1'] = row[7]
        d['line2'] = row[8]
        d['locality'] = row[9]
        d['customerName'] = row[10]
        addresses_json.append(d)
    return addresses_json


@frappe.whitelist()
def create_address(addressTitle, emailId, phone, addressLine1, city, state, pincode, customerName, addressLine2=None,
                   county=None):
    headers = {"Authorization": "Token d3b8f9e29501501:67e95c1f9503c26",
               "Content-Type": "application/json",
               "X-Frappe-CSRF-Token": frappe.generate_hash()
               }

    doc_dict = {
        "docstatus": 0,
        "doctype": "Address",
        "links": [
            {
                "docstatus": 0,
                "doctype": "Dynamic Link",
                "name": "new-dynamic-link-2",
                "parent": "new-address-2",
                "parentfield": "links",
                "parenttype": "Address",
                "idx": 1,
                "link_doctype": "Customer",
                "link_name": customerName
            }
        ],
        "address_title": addressTitle,
        "email_id": emailId,
        "phone": phone,
        "address_line1": addressLine1,
        "address_line2": addressLine2,
        "city": city,
        "county": county,
        "state": state,
        "pincode": pincode
    }

    payload = {
        "doc": json.dumps(doc_dict),
        "action": "Save"
    }
    request_url = "http://dev-erp.farmley.com/api/method/frappe.desk.form.save.savedocs"

    save_address_res = requests.post(url=request_url, data=json.dumps(payload), headers=headers)
    add_save_json = json.loads(save_address_res.content.decode('utf-8'))
    message = """["{\\"message\\": \\"Saved\\", \\"indicator\\": \\"green\\", \\"alert\\": 1}"]"""
    if add_save_json['_server_messages'] == message:
        return True
    else:
        return False


@frappe.whitelist()
def add_to_cart(payload, source, name):
    headers = {"Authorization": "Token d3b8f9e29501501:67e95c1f9503c26",
               "Accept": "application/json",
               "Content-Type": "application/json",
               "X-Frappe-CSRF-Token": frappe.generate_hash()}

    if name is None:

        # url = "http://localhost:8000/api/resource/Sales Order"
        url = "http://dev-erp.farmley.com/api/resource/Sales Order"
        save_orders_response = requests.post(url=url, data=json.dumps(payload), headers=headers)
        save_orders_json_data = json.loads(save_orders_response.content.decode('utf-8'))
        # adding tag on order
        # tag_url = "http://localhost:8000/api/method/frappe.desk.doctype.tag.tag.add_tag"
        tag_url = "http://dev-erp.farmley.com/api/method/frappe.desk.doctype.tag.tag.add_tag"
        tag_payload = {"tag": source, "dt": "Sales Order", "dn": save_orders_json_data["data"]["name"]}
        tag_response = requests.post(url=tag_url, data=json.dumps(tag_payload), headers=headers)
        tag_json_data = json.loads(tag_response.content.decode('utf-8'))
    else:
        # put_url = "http://localhost:8000/api/resource/Sales Order/{}".format(name)
        put_url = "http://dev-erp.farmley.com/api/resource/Sales Order/{}".format(name)
        save_orders_response = requests.put(url=put_url, data=json.dumps(payload), headers=headers)
        save_orders_json_data = json.loads(save_orders_response.content.decode('utf-8'))

    return save_orders_json_data


@frappe.whitelist()
def save_order(name, grandTotal=None):
    headers = {"Authorization": "Token d3b8f9e29501501:67e95c1f9503c26",
               "Accept": "apcustomerAddress, transactionDate, itemCode, itemName, deliveryDate, qty, rate,plication/json",
               "Content-Type": "application/json",
               "X-Frappe-CSRF-Token": frappe.generate_hash()
               }

    # url = "http://localhost:8000/api/resource/Sales Order/{}".format(name)
    url = "http://dev-erp.farmley.com/api/resource/Sales Order/{}".format(name)
    # url1 = "http://dev-erp.farmley.com/api/resource/Sales Order/{}".format(name)

    save_orders_response = requests.get(url=url, headers=headers)
    orders_data_json = json.loads(save_orders_response.content.decode('utf-8'))

    if float(grandTotal) == orders_data_json["data"]["grand_total"]:
        payload = {
            "order_type": "Sales",
            "docstatus": 1
        }

        save_orders_response = requests.put(url=url, data=json.dumps(payload), headers=headers)
        save_orders_response_data = json.loads(save_orders_response.content.decode('utf-8'))
        return True
    else:
        return False


@frappe.whitelist()
def cart_items(name, source=None):
    headers = {"Authorization": "Token d3b8f9e29501501:67e95c1f9503c26",
               "Content-Type": "application/json",
               "X-Frappe-CSRF-Token": frappe.generate_hash()
               }
    # name = cart_items_list[0]["name"]
    # url = "http://localhost:8000/api/resource/Sales Order/{}".format(name)
    url = "http://dev-erp.farmley.com/api/resource/Sales Order/{}".format(name)

    save_orders_response = requests.get(url=url, headers=headers)
    cart_items_list_if_exist = json.loads(save_orders_response.content.decode('utf-8'))
    return cart_items_list_if_exist


@frappe.whitelist()
def delete_cart(name):
    headers = {"Authorization": "Token d3b8f9e29501501:67e95c1f9503c26",
               "Content-Type": "application/json",
               "X-Frappe-CSRF-Token": frappe.generate_hash()
               }
    payload = {"doctype": "Sales Order",
               "name": name}
    request_url = "http://dev-erp.farmley.com/api/method/frappe.client.delete"
    delete_cart_response = requests.post(url=request_url, headers=headers, data=json.dumps(payload))
    delete_cart_response_json = json.loads(delete_cart_response.content.decode('utf-8'))
    return True


@frappe.whitelist()
def orders(customer):
    headers = {"Authorization": "Token d3b8f9e29501501:67e95c1f9503c26",
               "Content-Type": "application/json",
               "X-Frappe-CSRF-Token": frappe.generate_hash()
               }
    payload = {
        "filters": """[["Sales Order","workflow_state","!=","Draft"],["Sales Order","customer","=","{}"]]""".format(
            customer),
        "fields": """["`tabSales Order`.`workflow_state`","`tabSales Order`.`name`","`tabSales Order`.`owner`","`tabSales Order`.`creation`","`tabSales Order`.`modified`","`tabSales Order`.`modified_by`","`tabSales Order`.`_user_tags`","`tabSales Order`.`_comments`","`tabSales Order`.`_assign`","`tabSales Order`.`_liked_by`","`tabSales Order`.`docstatus`","`tabSales Order`.`parent`","`tabSales Order`.`parenttype`","`tabSales Order`.`parentfield`","`tabSales Order`.`idx`","`tabSales Order`.`delivery_date`","`tabSales Order`.`total`","`tabSales Order`.`net_total`","`tabSales Order`.`total_taxes_and_charges`","`tabSales Order`.`discount_amount`","`tabSales Order`.`grand_total`","`tabSales Order`.`rounding_adjustment`","`tabSales Order`.`rounded_total`","`tabSales Order`.`advance_paid`","`tabSales Order`.`status`","`tabSales Order`.`per_delivered`","`tabSales Order`.`per_billed`","`tabSales Order`.`customer_name`","`tabSales Order`.`base_grand_total`","`tabSales Order`.`currency`","`tabSales Order`.`order_type`","`tabSales Order`.`skip_delivery_note`","`tabSales Order`.`_seen`","`tabSales Order`.`party_account_currency`"]"""}
    url = "http://dev-erp.farmley.com/api/resource/Sales Order"
    order_details_list = []
    orders_list_response = requests.get(url=url, headers=headers, data=json.dumps(payload))
    orders_list = json.loads(orders_list_response.content.decode('utf-8'))
    for i in range(len(orders_list["data"])):
        print(orders_list["data"][i]["name"])
        order_details_list.append(cart_items(orders_list["data"][i]["name"]))
    return order_details_list
