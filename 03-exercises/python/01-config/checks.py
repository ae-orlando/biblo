from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '90-tools'))
from test_support import module


class ConfigurationTests(unittest.TestCase):
    def test_defaults_explicit_values_and_no_mutation(self):
        load = module().load_config
        env = {'TRAINING_TOKEN': 'fake-token'}
        self.assertEqual(load(env), {'token': 'fake-token', 'port': 8000, 'debug': False})
        self.assertEqual(env, {'TRAINING_TOKEN': 'fake-token'})
        self.assertEqual(load({'TRAINING_TOKEN': ' fake ', 'PORT': '9000', 'DEBUG': 'true'}), {'token': 'fake', 'port': 9000, 'debug': True})

    def test_invalid_configuration_fails_without_leaking_token(self):
        load = module().load_config
        for env in [{}, {'TRAINING_TOKEN': ' '}, {'TRAINING_TOKEN': 'do-not-leak', 'PORT': '0'}, {'TRAINING_TOKEN': 'do-not-leak', 'PORT': '65536'}, {'TRAINING_TOKEN': 'do-not-leak', 'PORT': '1.5'}, {'TRAINING_TOKEN': 'do-not-leak', 'PORT': '1_000'}, {'TRAINING_TOKEN': 'do-not-leak', 'DEBUG': 'yes'}]:
            with self.subTest(env=env), self.assertRaises(ValueError) as caught: load(env)
            self.assertNotIn('do-not-leak', str(caught.exception))


if __name__ == '__main__': unittest.main()
