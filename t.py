import unittest

if __name__ == "__main__":
    # Discover and run all tests starting with 'test_'
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='./test', pattern='test_*.py')

    runner = unittest.TextTestRunner()
    runner.run(suite)
