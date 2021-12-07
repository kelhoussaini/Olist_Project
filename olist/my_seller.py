import pandas as pd
import numpy as np
from olist.data import Olist
from olist.order import Order


class Seller:

    def __init__(self):
        # Import only data once
        olist = Olist()
        self.data = olist.get_data()
        self.matching_table = olist.get_matching_table()
        self.order = Order()

    def get_seller_features(self):
        """
        Returns a DataFrame with:
       'seller_id', 'seller_city', 'seller_state'
        """
        sellers = self.data['sellers'].copy()
        
        return sellers[['seller_id', 'seller_city', 'seller_state']]


    def get_seller_delay_wait_time(self):
        """
        Returns a DataFrame with:
       'seller_id', 'delay_to_carrier', 'seller_wait_time'
        """
        orders = self.data['orders'].copy()
        delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
        order_item = self.data['order_items'].copy()
        
        order_seller = delivered_orders[['order_id', 'order_purchase_timestamp',
                                 'order_delivered_carrier_date', 'order_delivered_customer_date']] \
              .merge(order_item[['order_id', 'seller_id', 'shipping_limit_date']], on = "order_id")
        
        order_seller.loc[:, 'order_purchase_timestamp'] = pd.to_datetime(
            order_seller['order_purchase_timestamp'], format='%Y-%m-%d')

        order_seller.loc[:,'order_delivered_customer_date'] = pd.to_datetime(
            order_seller['order_delivered_customer_date'], format='%Y-%m-%d')

        order_seller.loc[:,'order_delivered_carrier_date'] = pd.to_datetime(
            order_seller['order_delivered_carrier_date'], format='%Y-%m-%d')

        order_seller.loc[:,'shipping_limit_date'] = pd.to_datetime(
            order_seller['shipping_limit_date'], format='%Y-%m-%d')
        
        def negative_date(d):
            if d < 0:
                return abs(d)
            return 0
        
        def order_wait_time(df):
            days = np.mean(
                (df.order_delivered_customer_date - df.order_purchase_timestamp)
                / np.timedelta64(24, 'h'))
            return days
        
        def delay_to_logistic_partner(df):
            df['delay'] = (df.shipping_limit_date -
                      df.order_delivered_carrier_date) / np.timedelta64(24, 'h')
            df.loc[:,'delay'] = df.delay.apply(negative_date)
            return np.mean(df.delay)


        
        one_day_delta = np.timedelta64(24, 'h') # a "timedelta64" object of 1 day (use the one you prefer)

        order_seller_0 = order_seller[['seller_id', 'order_delivered_customer_date', 
                             'order_delivered_carrier_date',
                               'shipping_limit_date', 'order_purchase_timestamp']].copy()
        
        wait_time = order_seller_0.groupby('seller_id')\
        .apply( order_wait_time
             )  \
            .reset_index()
        wait_time.columns = ['seller_id', 'wait_time']
        
        delay_time = order_seller_0.groupby('seller_id')\
        .apply(delay_to_logistic_partner)\
            .reset_index()
        delay_time.columns = ['seller_id', 'delay_to_carrier']
        
        order_delay_wait_time = delay_time.merge(wait_time,  on='seller_id')
        #print("test______>", order_delay_wait_time.wait_time.min() )

        return order_delay_wait_time


        
    def get_active_dates(self):
        """
        Returns a DataFrame with:
       'seller_id', 'date_first_sale', 'date_last_sale'
        """
        
        orders = self.data['orders'].copy()
        delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
        order_item = self.data['order_items'].copy()
        
        order_seller = delivered_orders[['order_id', 'order_purchase_timestamp',
                                 'order_delivered_carrier_date', 'order_delivered_customer_date']] \
            .merge(order_item[['order_id', 'seller_id', 'shipping_limit_date']], on = "order_id")
        
        order_seller.loc[:, 'order_purchase_timestamp'] = pd.to_datetime(
            delivered_orders['order_purchase_timestamp'], format='%Y-%m-%d')

        order_seller.loc[:,'order_delivered_customer_date'] = pd.to_datetime(
            order_seller['order_delivered_customer_date'], format='%Y-%m-%d')

        order_seller.loc[:,'order_delivered_carrier_date'] = pd.to_datetime(
            order_seller['order_delivered_carrier_date'], format='%Y-%m-%d')

        order_seller.loc[:,'shipping_limit_date'] = pd.to_datetime(
            order_seller['shipping_limit_date'], format='%Y-%m-%d')
        
        def negative_date(d):
            if d < 0:
                return abs(d)
            return 0
        
        one_day_delta = np.timedelta64(24, 'h') # a "timedelta64" object of 1 day (use the one you prefer)

        order_seller['wait'] = \
              ( ( order_seller['order_delivered_customer_date'] \
                    - order_seller['order_purchase_timestamp'] ) / one_day_delta  ) .apply(negative_date)
        
        order_seller['delay'] = \
              ( ( order_seller['order_delivered_carrier_date'] \
                - order_seller['shipping_limit_date'] )  \
               / one_day_delta  ) .apply(negative_date)
        

        activ_dates = order_seller[ ['order_id','seller_id',
                                                    'order_purchase_timestamp' ]] 
        
        activ_dates = activ_dates.groupby('seller_id',as_index=False) \
           .agg({'order_purchase_timestamp': [np.min,np.max]}) 


        activ_dates.columns= ["seller_id", "date_first_sale", 'date_last_sale'] 
        
        return activ_dates



    def get_review_score(self):
        """
        Returns a DataFrame with:
        'seller_id', 'share_of_five_stars', 'share_of_one_stars',
        'review_score'
        """
        order_item = self.data['order_items'].copy()
        orders = self.data['orders'].copy()
        order_reviews = self.data['order_reviews'].copy()
        
        mask_columns = [ 'order_id', 'review_score','review_id' ]
        merged = orders.merge(order_reviews, on = 'order_id')[mask_columns]
        
        mask_columns = [ 'order_id', 'seller_id', 'review_score','review_id' ]
        merged = merged.merge(order_item, on = 'order_id')[mask_columns]
        
        def dim_five_star(d):
            if d == 5:
                return 1
            return 0

        def dim_one_star(d):
            if d == 1:
                return 1
            return 0

        merged.loc[:, 'dim_is_five_star'] =\
            merged['review_score'].apply(dim_five_star)

        merged.loc[:, 'dim_is_one_star'] =\
            merged['review_score'].apply(dim_one_star)
        
        merged_score = merged.groupby(
            'seller_id', as_index=False).agg({'dim_is_five_star': 'mean',
                                              'dim_is_one_star': 'mean',
                                              'review_score': 'mean'})\
                        .rename(columns= {'dim_is_one_star' : 'share_of_one_stars',
                                          'dim_is_five_star': 'share_of_five_stars'} )
        
        return merged_score




    def get_quantity(self):
        """
        Returns a DataFrame with:
        'seller_id', 'n_orders', 'quantity', 'quantity_per_order'
        """
        order_item = self.data['order_items'].copy()
        
        quantity_unique = order_item.groupby('seller_id', as_index= False)['order_id'].nunique()\
                    .rename(columns={"order_id" : "n_orders"} )
        
        quantity_total = order_item.groupby('seller_id', as_index= False)['order_id'].count()\
                 .rename(columns={"order_id" : "quantity"} ) 
        
        quantity_res = quantity_unique.merge(quantity_total, on = "seller_id")
        
        quantity_res['quantity_per_order'] = quantity_res['n_orders'] / quantity_res['quantity']
        
        return quantity_res




    def get_sales(self):
        """
        Returns a DataFrame with:
        'seller_id', 'sales'
        """
        order_item = self.data['order_items'].copy()
        sales = order_item.groupby('seller_id', as_index= False)['price']\
                   .agg(["sum"]).reset_index() \
                       .rename(columns={'sum': 'sales'})
        return sales
    
   

    def get_training_data(self):
        """
        Returns a DataFrame with:
        'seller_id', 'seller_state', 'seller_city', 'delay_to_carrier',
        'seller_wait_time', 'share_of_five_stars', 'share_of_one_stars',
        'seller_review_score', 'n_orders', 'quantity', 'date_first_sale', 'date_last_sale', 'sales'
        """
        #print("******", self.get_review_score()['review_score'].mean())
        #print("***delay_wait_time***", self.get_seller_delay_wait_time().head(1) )


        training_set =\
            self.get_seller_features()\
                .merge(
                self.get_seller_delay_wait_time(), on='seller_id'
               )
          
        #print("***get_sellers_merge_delai_wait_time***", training_set.head(1))


        training_set = training_set.merge(
                self.get_active_dates(), on='seller_id'
               )
        #print("******", training_set.head(1))
        training_set = training_set.merge(
                self.get_review_score(), on='seller_id'
               )
        #print("***score***", training_set.head(1))


        training_set = training_set.merge(
                self.get_quantity(), on='seller_id'
               )
        
        #print("***quantity***", training_set.head(1))


        training_set = training_set.merge(
                self.get_sales(), on='seller_id'
               )
        
        
        #print("***get_sales***", training_set.head(1))


        return training_set


