import sys

# Using AI assistance


def run_pytest():
    import pytest
    return pytest.main()


def run_unittest():
    import unittest
    loader = unittest.TestLoader()
    # Discover tests in current directory matching test*.py
    suite = loader.discover(start_dir='.', pattern='test*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # Exit code 0 if successful, 1 otherwise
    return 0 if result.wasSuccessful() else 1


def main():
    try:
        return run_pytest()
    except ImportError:
        print("pytest not installed; falling back to unittest discovery.")
        return run_unittest()


if __name__ == '__main__':
    sys.exit(main())
