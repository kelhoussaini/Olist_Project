from nbresult import ChallengeResultTestCase

class TestOrders(ChallengeResultTestCase):
    def test_keys_len(self):
      self.assertEqual(self.result.keys_len, 9)

    def test_key_names(self):
      sorted_key_names = ['customers',
                          'geolocation',
                          'order_items',
                          'order_payments',
                          'order_reviews',
                          'orders',
                          'product_category_name_translation',
                          'products',
                          'sellers']
      self.assertEqual(self.result.key_names, sorted_key_names)
    
    def test_reviews_number(self):
      self.assertEqual(self.result.reviews_number, 100000)
