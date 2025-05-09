from django.test import SimpleTestCase
from app.calc import add, subtract

class CalcTest(SimpleTestCase):
    def test_add_number(self):
        res = add(6, 4)
        self.assertEqual(res, 10)

    def test_subtract_number(self):
        res = subtract(10, 15)
        self.assertEqual(res, 5)