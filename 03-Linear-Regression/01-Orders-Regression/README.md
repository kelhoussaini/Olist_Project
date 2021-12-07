## Orders - Multivariate Linear Regression

A quick analysis of the `orders` dataset showed that `review_score` is mostly correlated with features such as `wait_time` and `delay_vs_expected`

However, these two features were also highly correlated with each other.

In this exercise, we will use `statsmodels` to determine the effect of one feature, **holding the other one constant**

Open `orders_regression.ipynb` and follow the instructions
