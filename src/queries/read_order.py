"""
Orders (read-only model)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from collections import defaultdict
import json
import logging
from db import get_sqlalchemy_session, get_redis_conn
from sqlalchemy import desc
from models.order import Order

def get_order_by_id(order_id):
    """Get order by ID from Redis"""
    r = get_redis_conn()
    return r.hgetall(order_id)

def get_orders_from_mysql(limit=9999):
    """Get last X orders"""
    session = get_sqlalchemy_session()
    return session.query(Order).order_by(desc(Order.id)).limit(limit).all()

def get_orders_from_redis(limit=9999):
    """Get last X orders"""
    # TODO: écrivez la méthodeè
    r = get_redis_conn()
    keys = r.keys("order:*")
    sorted_keys = sorted(keys, reverse=True)
    
    sorted_keys = sorted_keys[:limit]
    
    orders = []
    for key in sorted_keys:
        order_data = r.hgetall(key)
        if order_data:
            order_dict = {k: v for k, v in order_data.items()}
            orders.append(order_dict)
    return orders

def get_highest_spending_users():
    """Get report of best selling products"""
    # TODO: écrivez la méthode
    # triez le résultat par nombre de commandes (ordre décroissant)
    orders = get_orders_from_redis()
    expenses_by_user = defaultdict(float)
    for order in orders:
        expenses_by_user[order["user_id"]] += float(order["total_amount"])
    highest_spending_users = sorted(expenses_by_user.items(), key=lambda item: item[1], reverse=True)

    return highest_spending_users[:10]

def get_most_sold_product():
    r = get_redis_conn()
    keys = r.keys("product:*")


    products = []
    for key in keys:
        product_data = r.hgetall(key)
        if product_data:
            order_dict = {k: v for k, v in product_data.items()}
            products.append(order_dict)

    # trier du plus vendu au moins vendu
    sorted_products =  sorted(products.count() , key=lambda x: x[1], reverse=True)

    # appliquer une limite (par ex. top 10)
    return sorted_products[:10]
