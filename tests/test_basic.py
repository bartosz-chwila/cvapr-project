import unittest


class MyTestCase(unittest.TestCase):
    @staticmethod
    def test_run():
        assert True


if __name__ == '__main__':
    unittest.main()
