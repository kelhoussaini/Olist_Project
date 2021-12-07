from nbresult import ChallengeResultTestCase


class TestProducts(ChallengeResultTestCase):
  def test_shape(self):
    self.assertEqual(self.result.shape, (71, 15))

  def test_average_review_score(self):
    self.assertEqual(self.result.avg_review_score, 4)

  def test_average_price(self):
    self.assertEqual(self.result.avg_price, 169)

  def test_average_quantity(self):
    self.assertEqual(self.result.avg_quantity, 1551)
