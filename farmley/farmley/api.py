from __future__ import unicode_literals
import collections
import json
import requests
import frappe
from operator import itemgetter


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
def product_details(name=None, productCategoryName=None, productName=None):
    """
    param:productId, productCategory, productName, source
    return: products_json
    #  This api will return the website_product views details
    """
    sql_query = "select name,product_code,product_name,product_category,packaging_size,media_url, " \
                "hsn_code, barcode,parent_product_media_url,`Standard Buying`,`Website MRP List`," \
                "`Website Price list`,`B2B Price List`,`Standard Selling`,uuid,slug from product_details "
    where = " where "
    _and = " and "
    if name is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "name = \'{}\'".format(
        name)
    if productCategoryName is not None: sql_query = sql_query + (
        _and if "where" in sql_query else where) + "product_category like \'%{}%\'".format(productCategoryName)
    if productName is not None: sql_query = sql_query + (
        _and if "where" in sql_query else where) + "product_name like \'%{}%\'".format(productName)
    # if isParentProduct is True: sql_query = sql_query + (_and if "where" in sql_query else where) + " variant_of IS NULL "
    # if isParentProduct is False: sql_query = sql_query + (_and if "where" in sql_query else where) + " variant_of IS NOT NULL "

    db_data = frappe.db.sql(sql_query)
    products_json = []
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
        products_json.append(d)
    return products_json


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
def open_product_category(source=None):
    """
        param:source
        return:product_category
        # it will return the distinct product category to filter on frontend
    """
    sql_query = "select DISTINCT (product_category) from product_details"
    _and = " and "
    where = " where "
    if source is not None: sql_query = sql_query + (
        _and if "where" in sql_query else where) + "price_list like \'%{}%\'".format(source)
    db_data = frappe.db.sql(sql_query)
    product_category_json = []
    for row in db_data:
        d = collections.OrderedDict()
        d['productCategory'] = row[0]
        product_category_json.append(d)
    return product_category_json


@frappe.whitelist()
def customer_addresses(phoneNumber=None, emailId=None, name=None):
    """
    param: phoneNumber,emailId,customerCode
    return:addresses
    # this api will return all the addresses belong to that customer
    """
    sql_query = "select address_title, name, city, state, country, pincode, contact_name, contact_number, " \
                "address_line1, address_line2, locality from tabAddress "
    where = " where "
    _and = " and "
    if phoneNumber is not None: sql_query = sql_query + (
        _and if "where" in sql_query else where) + "phone = \'{}\'".format(phoneNumber)
    if name is not None: sql_query = sql_query + (_and if "where" in sql_query else where) + "name = \'{}\'".format(
        name)
    if emailId is not None: sql_query = sql_query + (
        _and if "where" in sql_query else where) + "email_id = \'{}\'".format(emailId)
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
def add_to_cart(customer, customerAddress, transactionDate, itemCode, itemName, deliveryDate, qty, rate, source):
    headers = {"Authorization": "Token 9e820d1621292f3:e40525854287561",
               "Accept": "application/json",
               "Content-Type": "application/json"}
    payload = {"order_type": "Shopping Cart",
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


@frappe.whitelist()
def save_orders(customer, order_name):
    headers = {"Authorization": "Token 9e820d1621292f3:e40525854287561",
               "Accept": "apcustomerAddress, transactionDate, itemCode, itemName, deliveryDate, qty, rate,plication/json",
               "Content-Type": "application/json"}
    payload = {"doc":{"name":"name",
                "order_type": "Sale",
               "customer": None,
               "customer_address": None,
                      "items": [{
                      }]
             },
               "action":"Save"
               }
    url = "http://localhost:8000/api/resource/Sales Order"
    url1 = "http://localhost:8000/api/method/frappe.desk.form.load.getdoc?doctype=Sales+Order&name=SAL-ORD-2021-00046&_=1632227660416"

    sales_order = frappe.db.get_all(doctype="Sales Order",
                                    filters=[["name", "=", order_name]],
                                    fields=["name","customer","customer_address","delivery_date", "transaction_date","`tabSales Order Item`.`item_code`",
                                            "`tabSales Order Item`.`item_name`", "`tabSales Order Item`.`qty`",
                                            "`tabSales Order Item`.`rate`"])
    payload["doc"]["name"] = sales_order[0]["name"]
    payload["doc"]["customer"] = sales_order[0]["customer"]
    payload["doc"]["customer_address"] = sales_order[0]["customer_address"]
    # payload["doc"]["transaction_date"] = sales_order[0]["transaction_date"]
    # payload["items"][0]["item_code"] = sales_order[0]["item_code"]
    # payload["items"][0]["item_name"] = sales_order[0]["item_name"]
    # payload["items"][0]["delivery_date"] = sales_order[0]["delivery_date"]
    # payload["items"][0]["qty"] = sales_order[0]["qty"]
    # payload["items"][0]["rate"] = sales_order[0]["rate"]
    pay= {
"doc":{
   "name":"SAL-ORD-2021-00046",
   "owner":"Administrator",
   "creation":"2021-09-21 17:44:54.483125",
   "modified":"2021-09-21 23:11:56.507107",
   "modified_by":"Administrator",
   "idx":0,
   "docstatus":0,
   "title":"{customer_name}",
   "naming_series":"SAL-ORD-.YYYY.-",
   "customer":"APNA FASAL",
   "customer_name":"APNA FASAL",
   "order_type":"Shopping Cart",
   "skip_delivery_note":0,
   "company":"Farmley",
   "transaction_date":"2021-09-07",
   "delivery_date":"2021-09-12",
   "customer_address":"A-Karnataka-560078-Shipping",
   "billing_address_gstin":"29AANFN1730F1Z9",
   "address_display":"GROUND FLOOR<br>NO 4 SAI ARCADE, KOTHANUR MAIN ROAD OPPOSITE TO ADISHWAR,NEAR BRIGADE MILLENNIUM JP<br>Bangalore<br>\nKarnataka, State Code: 29<br>Postal Code: 560078<br>India<br>\nPhone: 9986027568<br>GSTIN: 29AANFN1730F1Z9<br>",
   "shipping_address_name":"APNA FASAL-Telangana-500100-Shipping",
   "customer_gstin":"36BGJPG2358D1ZL",
   "place_of_supply":"29-Karnataka",
   "shipping_address":"202, Datta Avenue, Gangastan, Dhulapally, Gandimaisamma Mandal<br>Medchal - Malkajgiri,Malkajgiri<br>Hyderabad<br>\nTelangana, State Code: 36<br>Postal Code: 500100<br>India<br>\nPhone: 9885063992<br>Email: apnafasal@gmail.com<br>GSTIN: 36BGJPG2358D1ZL<br>",
   "customer_group":"All Customer Groups",
   "territory":"All Territories",
   "currency":"INR",
   "conversion_rate":1,
   "selling_price_list":"Standard Selling",
   "price_list_currency":"INR",
   "plc_conversion_rate":1,
   "ignore_pricing_rule":0,
   "total_qty":50,
   "base_total":26250,
   "base_net_total":26250,
   "total_net_weight":0,
   "total":26250,
   "net_total":26250,
   "tax_category":"",
   "base_total_taxes_and_charges":0,
   "total_taxes_and_charges":0,
   "loyalty_points":0,
   "loyalty_amount":0,
   "apply_discount_on":"Grand Total",
   "base_discount_amount":0,
   "additional_discount_percentage":0,
   "discount_amount":0,
   "base_grand_total":26250,
   "base_rounding_adjustment":0,
   "base_rounded_total":26250,
   "base_in_words":"",
   "grand_total":26250,
   "rounding_adjustment":0,
   "rounded_total":26250,
   "in_words":"",
   "advance_paid":0,
   "disable_rounded_total":0,
   "payment_terms_template":"ADVANCE",
   "is_internal_customer":0,
   "language":"en",
   "group_same_items":0,
   "status":"Draft",
   "delivery_status":"Not Delivered",
   "per_delivered":0,
   "per_billed":0,
   "billing_status":"Not Billed",
   "commission_rate":0,
   "total_commission":0,
   "doctype":"Sales Order",
   "items":[
      {
         "name":"74a3a01cc5",
         "owner":"Administrator",
         "creation":"2021-09-21 17:44:54.483125",
         "modified":"2021-09-21 23:11:56.507107",
         "modified_by":"Administrator",
         "parent":"SAL-ORD-2021-00046",
         "parentfield":"items",
         "parenttype":"Sales Order",
         "idx":1,
         "docstatus":0,
         "item_code":"Almonds-1-10",
         "ensure_delivery_based_on_produced_serial_no":0,
         "delivery_date":"2021-09-12",
         "item_name":"Popular California Almonds Farmley PP Bag 25 kg",
         "description":"Premium Almond Blanched Sliced Farmley Carton Box 15 KG",
         "gst_hsn_code":"08021200",
         "is_nil_exempt":0,
         "is_non_gst":0,
         "item_group":"Almonds",
         "image":"",
         "qty":50,
         "stock_uom":"Kg",
         "uom":"Kg",
         "conversion_factor":1,
         "stock_qty":50,
         "price_list_rate":350,
         "base_price_list_rate":350,
         "margin_type":"Amount",
         "margin_rate_or_amount":175,
         "rate_with_margin":0,
         "discount_percentage":0,
         "discount_amount":-175,
         "base_rate_with_margin":0,
         "rate":525,
         "amount":26250,
         "base_rate":525,
         "base_amount":26250,
         "stock_uom_rate":525,
         "is_free_item":0,
         "net_rate":525,
         "net_amount":26250,
         "base_net_rate":525,
         "base_net_amount":26250,
         "billed_amt":0,
         "valuation_rate":0,
         "gross_profit":26250,
         "delivered_by_supplier":0,
         "weight_per_unit":0,
         "total_weight":0,
         "warehouse":"Stores - F",
         "against_blanket_order":0,
         "blanket_order_rate":0,
         "projected_qty":-250,
         "actual_qty":0,
         "ordered_qty":0,
         "planned_qty":0,
         "work_order_qty":0,
         "delivered_qty":0,
         "produced_qty":0,
         "returned_qty":0,
         "page_break":0,
         "item_tax_rate":"{}",
         "transaction_date":"2021-09-07",
         "doctype":"Sales Order Item"
      }
   ],
   "pricing_rules":[

   ],
   "taxes":[

   ],
   "packed_items":[

   ],
   "payment_schedule":[
      {
         "name":"2921539b39",
         "owner":"Administrator",
         "creation":"2021-09-21 17:44:55.568081",
         "modified":"2021-09-21 23:11:56.507107",
         "modified_by":"Administrator",
         "parent":"SAL-ORD-2021-00046",
         "parentfield":"payment_schedule",
         "parenttype":"Sales Order",
         "idx":1,
         "docstatus":0,
         "payment_term":"ADVANCE",
         "due_date":"2021-09-07",
         "invoice_portion":100,
         "discount_type":"Percentage",
         "discount_date":"2021-09-07",
         "discount":0,
         "payment_amount":26250,
         "outstanding":26250,
         "paid_amount":0,
         "discounted_amount":0,
         "base_payment_amount":26250,
         "doctype":"Payment Schedule"
      }
   ],
   "sales_team":[

   ],
   "_user_tags":",app",
   "__onload":{
      "make_payment_via_journal_entry":0
   },
   "__last_sync_on":"2021-09-22T04:40:32.592Z",
   "__unsaved":1
},
"action":"Save"
}

    save_orders_response = requests.post(url=url, data=json.dumps(payload), headers=headers)
    save_orders_json_data = json.loads(save_orders_response.content.decode('utf-8'))

    return save_orders_json_data
