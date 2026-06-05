import unittest

from runway_sim_command_cli.cli import months_of_runway, scenario_pack, simulate


class RunwayTests(unittest.TestCase):
    def test_months_of_runway(self):
        self.assertEqual(months_of_runway(120_000, 20_000), 6)

    def test_simulate_decreases_cash(self):
        rows = simulate(100_000, 20_000, revenue=5_000, growth=0.10, months=3)

        self.assertEqual(len(rows), 3)
        self.assertLess(rows[-1]["ending_cash"], 100_000)
        self.assertGreater(rows[-1]["revenue"], rows[0]["revenue"])

    def test_scenario_pack_has_three_modes(self):
        pack = scenario_pack(100_000, 20_000, 5_000)

        self.assertEqual(set(pack), {"base", "lean", "growth"})
        self.assertLess(pack["lean"][0]["net_burn"], pack["growth"][0]["net_burn"])


if __name__ == "__main__":
    unittest.main()
