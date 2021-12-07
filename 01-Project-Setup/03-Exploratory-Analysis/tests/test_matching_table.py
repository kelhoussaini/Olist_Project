from nbresult import ChallengeResultTestCase

class TestMatchingTable(ChallengeResultTestCase):

  def test_shape(self):
    self.assertEqual(self.result.shape, (114100, 5))

  def test_columns(self):
    self.assertEqual(self.result.columns, ['customer_id', 'order_id', 'product_id', 'review_id', 'seller_id'])
