## Warm-up : a quick logistic regression

We have seen that many customers are unhappy, with 11% of orders receiving 1-star reviews.

Often, being able to identify clearly the worst reviews (1 star) is more important than being precise in predicting the exact review score of each order.

In this warm-up challenge, we will simply run a Logit model for `dim_is_one_star` from our `orders` training set, and compare that with our OLS prediction of `review_score`.

We will also compare it to a Logit model for `dim_is_five_star`.

Open the notebook `logit.ipynb` and follow instructions.
