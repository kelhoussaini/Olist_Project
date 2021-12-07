import pandas as pd
import numpy as np
from olist.data import Olist
from olist.order import Order


class Product:

    def __init__(self):
        # Import only data once
        olist = Olist()
        self.data = olist.get_data()
        self.matching_table = olist.get_matching_table()
        self.order = Order()

    def get_product_features(self):
        """
        Returns a DataFrame with:
       'product_id', 'product_category_name', 'product_name_length',
       'product_description_length', 'product_photos_qty', 'product_weight_g',
       'product_length_cm', 'product_height_cm', 'product_width_cm'
        """

    def get_price(self):
        """
        Return a DataFrame with:
        'product_id', 'price'
        """

    def get_wait_time(self):
        """
        Returns a DataFrame with:
        'product_id', 'wait_time'
        """

    def get_review_score(self):
        """
        Returns a DataFrame with:
        'product_id', 'share_of_five_stars', 'share_of_one_stars',
        'review_score'
        """

    def get_quantity(self):
        """
        Returns a DataFrame with:
        'product_id', 'n_orders', 'quantity'
        """

    def get_sales(self):
        """
        Returns a DataFrame with:
        'product_id', 'sales'
        """

    def get_training_data(self):
        """
        Returns a DataFrame with:
        product_id, product_category_name, product_name_length,
        product_description_length, product_photos_qty, product_weight_g,
        product_length_cm, product_height_cm, product_width_cm, price,
        wait_time, share_of_five_stars, share_of_one_stars, review_score,
        n_orders, quantity, sales
        """

    def get_product_cat(self, agg="median"):
        '''
        Returns a DataFrame aggregating various properties for each product 'category',
        using the aggregation function passed in argument.
        The 'quantity' columns refers to the total number of product sold for this category.
        '''
