import unittest
from predict import FEATURES, predict_record

class InferenceTests(unittest.TestCase):
    def setUp(self):
        self.record = dict.fromkeys(FEATURES, 0)
        self.record.update(LIMIT_BAL=100000, SEX=2, EDUCATION=2, MARRIAGE=1, AGE=35)

    def test_probability_and_decision(self):
        result = predict_record(self.record)
        self.assertTrue(0 <= result['default_probability'] <= 1)
        self.assertEqual(result['prediction'], int(result['default_probability'] >= 0.5))

    def test_education_mapping(self):
        predictions = [predict_record(dict(self.record, EDUCATION=i)) for i in [0, 5, 6]]
        self.assertEqual(predictions[0], predictions[1])
        self.assertEqual(predictions[0], predictions[2])

    def test_reject_invalid_input(self):
        for change in [{'SEX': 9}, {'AGE': float('nan')}, {'PAY_AMT1': -1}]:
            with self.assertRaises(ValueError):
                predict_record(dict(self.record, **change))

if __name__ == '__main__':
    unittest.main()
