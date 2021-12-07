from nbresult import ChallengeResultTestCase


class TestGetData(ChallengeResultTestCase):
    def test_len(self):
        self.assertEqual(self.result.keys_len, 9)

    def test_columns(self):
        self.assertEqual(
            self.result.columns, [
                'seller_city',
                'seller_id',
                'seller_state',
                'seller_zip_code_prefix'
            ]
        )

    def test_keys(self):
        keys = ['customers', 'geolocation', 'order_items', 'order_payments',
                'order_reviews', 'orders', 'product_category_name_translation',
                'products', 'sellers']
        self.assertEqual(self.result.keys, keys)
