import unittest
from teams import generate_teams


def example_members():
    return ["1a", "2b", "3c", "4d", "5f", "6g", "7h", "8i", "9s", "10j"]


class TestTeams(unittest.TestCase):

    def test_size(self):
        m = example_members()

        res = generate_teams(m, size=4)

        # Should make 3 teams
        self.assertEqual(len(res), 3)

        # the first two will be full
        self.assertEqual(len(res.teams[0]), 4)
        self.assertEqual(len(res.teams[1]), 4)

        # the third is overrun with 2
        self.assertEqual(len(res.teams[2]), 2)

    def test_team_count(self):
        m = example_members()

        # Should generate 3 teams of 3
        # plus 1 'extra'
        res = generate_teams(m, team_count=3)

        # Should make 3 teams
        self.assertEqual(len(res), 3)

        # all teams should have 3 members
        for t in res.teams:
            self.assertEqual(len(t), 3)

        # there should be one 'extra'

        self.assertTrue(res.extras is not None)
        self.assertEqual(len(res.extras), 1)


if __name__ == "__main__":
    unittest.main()
