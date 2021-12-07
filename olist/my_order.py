import os
import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''

    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        02-01 > Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filtering out non-delivered orders unless specified
        """
        
        orders = self.data['orders'].copy() # good practice to be sure not to modify your `data` variable
        
        # Filter dataframe on delivered orders
        delivered_orders = orders[ orders['order_status'] == 'delivered'].copy()

        ## converting dates from "string" type to "pandas.datetime'

        delivered_orders['order_purchase_timestamp'] = pd.to_datetime(
            delivered_orders['order_purchase_timestamp'], format='%Y-%m-%d')

        delivered_orders['order_approved_at'] = pd.to_datetime(
            delivered_orders['order_approved_at'], format='%Y-%m-%d')

        delivered_orders['order_delivered_carrier_date'] = pd.to_datetime(
            delivered_orders['order_delivered_carrier_date'], format='%Y-%m-%d')

        delivered_orders['order_delivered_customer_date'] = pd.to_datetime(
            delivered_orders['order_delivered_customer_date'], format='%Y-%m-%d')

        delivered_orders['order_estimated_delivery_date'] = pd.to_datetime(
            delivered_orders['order_estimated_delivery_date'], format='%Y-%m-%d')
        
        # wait_time
        #delivered_orders['wait_time'] = delivered_orders['order_delivered_carrier_date'
                                                        #] - delivered_orders['order_approved_at'] 
        one_day_delta = np.timedelta64(24, 'h') # a "timedelta64" object of 1 day (use the one you prefer)

        delivered_orders['wait_time'] = \
           ( delivered_orders['order_delivered_customer_date'] - delivered_orders['order_purchase_timestamp'] ) / one_day_delta

        # expected_wait_time
        #delivered_orders['expected_wait_time'] = delivered_orders['order_estimated_delivery_date'
                                                                 #] - delivered_orders['order_approved_at']
        delivered_orders['expected_wait_time'] = \
       ( delivered_orders['order_estimated_delivery_date'] - delivered_orders['order_purchase_timestamp'] ) / one_day_delta

        # delay_vs_expected
        #delivered_orders['delay_vs_expected'] = delivered_orders['wait_time']  - delivered_orders['expected_wait_time'] 
        delivered_orders['delay_vs_expected'] = \
            delivered_orders['wait_time'] - delivered_orders['expected_wait_time']

        def handle_delay(x):
            return 0 if x < 0 else x
        delivered_orders.loc[:, 'delay_vs_expected'] = delivered_orders['delay_vs_expected'].apply(handle_delay)

        # new dataframe with specific keys
        #orders_new = delivered_orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]
        orders_new = delivered_orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']].copy()

        return orders_new









        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes

    def get_review_score(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        
        reviews = self.data['order_reviews'].copy()
        
        def dim_five_star(d):
            return 1 if d == 5 else 0
        def dim_one_star(d):
            return 1 if d == 1 else 0
    
        reviews["dim_is_five_star"] = reviews["review_score"].map(dim_five_star) # --> Series([0, 1, 1, 0, 0, 1 ...])
        reviews["dim_is_one_star"] = reviews["review_score"].map(dim_one_star) # --> Series([0, 1, 1, 0, 0, 1 ...])
        review_scor_stars = reviews[ ['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]
        return review_scor_stars
        

    def get_number_products(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, number_of_products
        """
        orders_products = self.data['order_items'].copy()
        grouped_products = orders_products.groupby(['order_id']).count()[['order_item_id','product_id']]
        
        return grouped_products


    def get_number_sellers(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, number_of_sellers
        """
        
        orders_products = self.data['order_items'].copy()
        grouped_sellers = orders_products.groupby(['order_id']).count()[['seller_id']]
        
        return grouped_sellers




    def get_price_and_freight(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, price, freight_value
        """
        price_and_freight = self.data['order_items'][ ['order_id','price', 'freight_value'] ].copy()
        return price_and_freight



    # Optional
    def get_distance_seller_customer(self):
        """
        02-01 > Returns a DataFrame with order_id
        and distance between seller and customer
        """

        # import data

        data = self.data
        matching_table = Olist().get_matching_table()

        # Since one zipcode can map to multiple (lat, lng), take first one
        geo = data['geolocation']
        geo = geo.groupby('geolocation_zip_code_prefix',
                          as_index=False).first()

        # Select sellers and customers
        sellers = data['sellers']
        customers = data['customers']

        # Merge geo_location for sellers
        sellers_mask_columns = ['seller_id', 'seller_zip_code_prefix',
                                'seller_city', 'seller_state',
                                'geolocation_lat', 'geolocation_lng']

        sellers_geo = sellers.merge(
            geo,
            how='left',
            left_on='seller_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[sellers_mask_columns]

        # Merge geo_location for customers
        customers_mask_columns = ['customer_id', 'customer_zip_code_prefix',
                                  'customer_city', 'customer_state',
                                  'geolocation_lat', 'geolocation_lng']

        customers_geo = customers.merge(
            geo,
            how='left',
            left_on='customer_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[customers_mask_columns]

        # Use the matching table and merge customers and sellers
        matching_geo = matching_table.merge(sellers_geo,
                                            on='seller_id')\
                                     .merge(customers_geo,
                                            on='customer_id',
                                            suffixes=('_seller',
                                                      '_customer'))
        # Remove na()
        matching_geo = matching_geo.dropna()

        matching_geo.loc[:, 'distance_seller_customer'] =\
            matching_geo.apply(
                lambda row: haversine_distance(
                    row['geolocation_lng_seller'],
                    row['geolocation_lat_seller'],
                    row['geolocation_lng_customer'],
                    row['geolocation_lat_customer']), axis=1)
        # Since an order can have multiple sellers,
        # return the average of the distance per order
        order_distance =\
            matching_geo.groupby(
                'order_id',
                as_index=False).agg({'distance_seller_customer': 'mean'})

        return order_distance
    
    '''def get_training_data(self, is_delivered=True,
                          with_distance_seller_customer=False):
        """
        02-01 > Returns a clean DataFrame (without NaN), with the following columns:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status,
        dim_is_five_star, dim_is_one_star, review_score, number_of_products,
        number_of_sellers, price, freight_value, distance_customer_seller]
        """
        # Hint: make sure to re-use your instance methods defined above
        
        orders = self.data['orders'].copy().dropna() # good practice to be sure not to modify your `data` variable
        
        # Filter dataframe on delivered orders
        delivered_orders = orders[ orders['order_status'] == 'delivered'].copy()

        ## converting dates from "string" type to "pandas.datetime'

        delivered_orders['order_purchase_timestamp'] = pd.to_datetime(
            delivered_orders['order_purchase_timestamp'], format='%Y-%m-%d')

        delivered_orders['order_approved_at'] = pd.to_datetime(
            delivered_orders['order_approved_at'], format='%Y-%m-%d')

        delivered_orders['order_delivered_carrier_date'] = pd.to_datetime(
            delivered_orders['order_delivered_carrier_date'], format='%Y-%m-%d')

        delivered_orders['order_delivered_customer_date'] = pd.to_datetime(
            delivered_orders['order_delivered_customer_date'], format='%Y-%m-%d')

        delivered_orders['order_estimated_delivery_date'] = pd.to_datetime(
            delivered_orders['order_estimated_delivery_date'], format='%Y-%m-%d')
        
        # wait_time
        delivered_orders['wait_time'] = delivered_orders['order_delivered_carrier_date'
                                                        ] - delivered_orders['order_approved_at'] 
        # expected_wait_time
        delivered_orders['expected_wait_time'] = delivered_orders['order_estimated_delivery_date'
                                                                 ] - delivered_orders['order_approved_at']
        # delay_vs_expected
        delivered_orders['delay_vs_expected'] = delivered_orders['wait_time']  - delivered_orders['expected_wait_time'] 
        
        # new dataframe with specific keys
        orders_new = delivered_orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]
        
        reviews = self.data['order_reviews'].copy().dropna()
        
        def dim_five_star(d):
            return 1 if d == 5 else 0
        def dim_one_star(d):
            return 1 if d == 1 else 0
    
        reviews["dim_is_five_star"] = reviews["review_score"].map(dim_five_star) # --> Series([0, 1, 1, 0, 0, 1 ...])
        reviews["dim_is_one_star"] = reviews["review_score"].map(dim_one_star) # --> Series([0, 1, 1, 0, 0, 1 ...])
        review_scor_stars = reviews[ ['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]
        
        orders_products = self.data['order_items'].copy().dropna()
        grouped_products = orders_products.groupby(['order_id']).count()[['order_item_id','product_id']]
        
        orders_products = self.data['order_items'].copy().dropna()
        grouped_sellers = orders_products.groupby(['order_id']).count()[['seller_id']]
        
        price_and_freight = self.data['order_items'][ ['order_id','price', 'freight_value'] ].copy().dropna()
        
        frames = [delivered_orders, review_scor_stars, grouped_products, grouped_sellers, price_and_freight]
        
        merged = delivered_orders.merge(review_scor_stars, on='order_id', how='left')
        merged = merged.merge(price_and_freight, on='order_id', how='left')
        merged = merged.merge(grouped_products, how='inner', right_index = True, left_on = 'order_id')
        merged = merged.merge(grouped_sellers, how='inner', right_index = True, left_on = 'order_id')


        return merged
        '''
    
    def get_training_data(self, is_delivered=True,
                          with_distance_seller_customer=False):
        """
        02-01 > Returns a clean DataFrame (without NaN), with the following
        columns: [order_id, wait_time, expected_wait_time, delay_vs_expected,
        dim_is_five_star, dim_is_one_star, review_score, number_of_products,
        number_of_sellers, price, freight_value, distance_customer_seller]
        """
        # Hint: make sure to re-use your instance methods defined above
        training_set =\
            self.get_wait_time(is_delivered)\
                .merge(
                self.get_review_score(), on='order_id'
               ).merge(
                self.get_number_products(), on='order_id'
               ).merge(
                self.get_number_sellers(), on='order_id'
               ).merge(
                self.get_price_and_freight(), on='order_id'
               )
        # Skip heavy computation of distance_seller_customer unless specified
        if with_distance_seller_customer:
            training_set = training_set.merge(
                self.get_distance_seller_customer(), on='order_id')

        return training_set.dropna()
        
        
        
        
        
        
        
