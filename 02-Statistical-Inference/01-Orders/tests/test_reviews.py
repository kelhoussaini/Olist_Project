from nbresult import ChallengeResultTestCase


class TestReviews(ChallengeResultTestCase):
  def test_dim_five_star(self):
    self.assertEqual(self.result.dim_five_star, 1)
    
  def test_dim_not_five_star(self):
    self.assertEqual(self.result.dim_not_five_star, 0)

  def test_dim_one_star(self):
    self.assertEqual(self.result.dim_one_star, 1)

  def test_dim_not_one_star(self):
    self.assertEqual(self.result.dim_not_one_star, 0)
