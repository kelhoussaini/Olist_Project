## Sellers

So far, we have seen how `wait_time` was the most significant factor explaining low review scores, but reading comments of the bad reviews also showed that some of them were linked to the seller themself...

Besides, `wait_time` is not known ahead of the order, and thus can hardly be directly addressed by your data-consulting team as a recommendation to the Olist CEO.

On the contrary, we might be able to quantify **which sellers should be removed from the marketplace due to persistent bad reviews**, in order to improve profit margin.

Open the following notebook `sellers.ipynb` :
- We will create a clean training_set with every information possible about sellers (one row per seller)
- Then, we will analyze which sellers repeatedly underperform vs others, and try to understand why
- We will then formulate early hypotheses and patterns to use in order to increase quality supply on the Olist platform

