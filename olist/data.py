import os
import pandas as pd


class Olist:

    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrame loaded from csv files
        """
        # Hints: Build csv_path as "absolute path" in order to call this method from anywhere.
        # Do not hardcode your path as it only works on your machine ('Users/username/code...')
        # Use __file__ as absolute path anchor independant of your computer
        # Make extensive use of `import ipdb; ipdb.set_trace()` to investigate what `__file__` variable is really
        # Use os.path library to construct path independent of Unix vs. Windows specificities
        pathh = os.path.dirname(os.path.dirname(os.getcwd()))
        csv_path = os.path.join(pathh, "data",  "csv")
        print(os.getcwd())
        print(pathh)
        print(csv_path)
        ##
        file_names = []
        for i in os.listdir(csv_path):
            print(i)
            if (".csv" in i):
                file_names.append(i)
        ##
        key_names = [i.replace(".csv", "").replace("_dataset", "").replace("olist_", "") for i in file_names]
        #
        data_keys = {}
        for (x, y) in zip( key_names, file_names):
            data_keys[x] = y
        data_keys
        
        data = {}
        for k,l in data_keys.items():
            data[k] =  pd.read_csv(os.path.join(csv_path, l))
        #dataframe = pd.read_csv(os.path.join(csv_path, y)).head())
        return data



    def get_matching_table(self):
        """
        This function returns a matching table between
        columns [ "order_id", "review_id", "customer_id", "product_id", "seller_id"]
        """

        data = self.get_data()

        # Select only the columns of interest
        orders = data["orders"][["customer_id", "order_id"]]
        reviews = data["order_reviews"][["order_id", "review_id"]]
        items = data["order_items"][["order_id", "product_id", "seller_id"]]

        # Merge DataFrame
        matching_table = orders\
        .merge(reviews, on="order_id", how="outer")\
        .merge(items, on="order_id", how="outer")

        return matching_table

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")


