from nbresult import ChallengeResultTestCase

class TestLogit(ChallengeResultTestCase):

  def test_question(self):
    res = ["delay_vs_expected influences five_star ratings even more than one_star ratings"]
    self.assertCountEqual(self.result.answers, res)
