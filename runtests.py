import unittest


def run_test(module:str):
    print(f'Testing module: {module}')
    unittest.main(module=module, exit=False)
    print('\n\n')

if __name__ == '__main__':
    run_test('tests.game_tests')
    run_test('tests.ai_tests')


