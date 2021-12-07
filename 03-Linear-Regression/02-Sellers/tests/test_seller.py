from nbresult import ChallengeResultTestCase


class TestSeller(ChallengeResultTestCase):
    def test_shape(self):
        self.assertEqual(self.result.shape, (2970, 14))

    def test_columns(self):
        columns = ['date_first_sale',
                   'date_last_sale',
                   'delay_to_carrier',
                   'n_orders',
                   'quantity',
                   'quantity_per_order',
                   'review_score',
                   'sales',
                   'seller_city',
                   'seller_id',
                   'seller_state',
                   'share_of_five_stars',
                   'share_of_one_stars',
                   'wait_time']
        self.assertEqual(self.result.columns, columns)

    def test_average_review_score(self):
        self.assertEqual(self.result.avg_review_score, 4)

    def test_unique_state(self):
        states = ['AM',
                  'BA',
                  'CE',
                  'DF',
                  'ES',
                  'GO',
                  'MA',
                  'MG',
                  'MS',
                  'MT',
                  'PA',
                  'PB',
                  'PE',
                  'PI',
                  'PR',
                  'RJ',
                  'RN',
                  'RO',
                  'RS',
                  'SC',
                  'SE',
                  'SP']
        self.assertEqual(self.result.unique_state, states)

    def test_wait_time(self):
        self.assertEqual(self.result.min_wait_time, 1.21)
        self.assertEqual(self.result.max_wait_time, 189)
        self.assertEqual(self.result.avg_wait_time, 12)

    def test_average_delay_carrier(self):
        self.assertLess(self.result.avg_delay_carrier, 0.6)
        self.assertGreater(self.result.avg_delay_carrier, 0.3)

    def test_quantity(self):
        self.assertIn(self.result.avg_quantity, (37, 38))
        self.assertLess(self.result.max_quantity, 2040)
        self.assertGreater(self.result.max_quantity, 2030)
        self.assertEqual(self.result.min_quantity, 1)

    def test_average_sales(self):
        self.assertEqual(self.result.avg_sales, 4566)
