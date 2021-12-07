## Olist Classes

This folder contains Olist Classes that handle the logic of data cleaning for our project.

Example to return data as a Python dictionnary using the `get_data` method from the `Olist` class:

```python
from olist.data import Olist
olist = Olist()
data = olist.get_data()
```

### Data

Import:

```python
from olist.data import Olist
```

Methods:

- `get_data`: returns all Olist datasets as DataFrames within a Python dict.
- `get_matching_table`: returns the DataFrame `customer_id`, `customer_unique_id`, `order_id`, `seller_id`.

### Order

Import:

```python
from olist.order import Order
```

- `get_wait_time`: returns a DataFrame with: `order_id, wait_time, expected_wait_time ,delay_vs_expected`
- `get_review_score`: returns a DataFrame with: `order_id, dim_is_five_star, dim_is_one_star, review_score`
- `get_number_products`: returns a DataFrame with: `order_id, number_of_products`
- `get_number_sellers`: returns a DataFrame with: `order_id, number_of_products`
- `get_price_and_freight`: returns a DataFrame with: `order_id, price, freight_value`
- `get_training_data`: returns a DataFrame with: `order_id, wait_time, delay_vs_expected, dim_is_five_star, dim_is_one_star, number_of_product, number_of_sellers, freight_value, distance_customer_seller`.

### Product

Import:

```python
from olist.product import Product
```

- `get_product_features`: returns a DataFrame with:
   `'product_id', 'product_category_name', 'product_name_length',
   'product_description_length', 'product_photos_qty', 'product_weight_g',
   'product_length_cm', 'product_height_cm', 'product_width_cm'`
- `get_wait_time`: returns a DataFrame with: `'product_id', 'wait_time'`.
- `get_review_score`: returns a DataFrame with: `'product_id', 'share_of_five_stars', 'share_of_one_stars', 'review_score'`
- `get_quantity`: returns a DataFrame with: `'product_id', 'n_orders', 'quantity'`.
- `get_training_data`: returns a DataFrame with: `product_id, category, height, width, length, weight, price, freight_value, product_name_length, product_description_length, n_orders, quantity, wait_time, share_of_five_stars, share_of_one_stars, review_score`.

### Review

Import:

```python
from olist.review import Review
```

- `get_review_length`: returns a DataFrame with:
   `'review_id', 'length_review', 'review_score'`
- `get_main_product_category`: returns a DataFrame with: `'review_id', 'order_id','length_review'`.
- `get_training_data`: returns a DataFrame with:
   `'review_id', 'order_id', 'review_comment_length', 'product_category'`

### Seller

Import:

```python
from olist.seller import Seller
```
- `get_seller_features`: returns a DataFrame with: `'seller_id', 'seller_city', 'seller_state'`.
- `get_seller_delay_wait_time`: returns a DataFrame with: `'seller_id', 'delay_to_carrier', 'seller_wait_time'`.
- `get_review_score`: returns a DataFrame with: `'seller_id', 'share_of_five_stars', 'share_of_one_stars', 'review_score'`.
- `get_quantity`: returns a DataFrame with: `'seller_id', 'n_orders', 'quantity'`.
- `get_training_data`: returns a DataFrame with: `seller_id, seller_state, seller_city, delay_to_carrier, seller_wait_time, share_of_five_stars, share_of_one_stars, seller_review_score, n_orders`.

### Utils

Utils functions for Olist project.

Import:

```python
from olist.utils import *
```

- `haversine_distance(lat1, lng1, lat2, lng2)`: compute distance (in km) between two pairs of (lat, lng)
  See - (https://en.wikipedia.org/wiki/Haversine_formula)
- `text_scatterplot(df, x, y)`: for a Dataframe `df`, create a scatterplot with `x` and `y` as axis. The index of `df` is the text label.
- `return_significative_coef(model)`: from a `model` as a statsmodels object, returns significant coefficients.
- `plot_kde_plot(df, variable, dimension)`: plot a side by side kdeplot from DataFrame `df` for `variable`, split by `dimension`.
