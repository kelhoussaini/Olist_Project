from nbresult import ChallengeResultTestCase


class TestTraining(ChallengeResultTestCase):
  def test_training_data_shape(self):
    self.assertEqual(self.result.shape, (97007, 12))

  def test_training_data_columns(self):
    columns = ['delay_vs_expected',
                'dim_is_five_star',
                'dim_is_one_star',
                'expected_wait_time',
                'freight_value',
                'number_of_products',
                'number_of_sellers',
                'order_id',
                'order_status',
                'price',
                'review_score',
                'wait_time']
    self.assertEqual(self.result.columns, columns)


