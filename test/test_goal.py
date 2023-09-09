import unittest
from unittest import TestCase

from goal import from_json, to_json, GoalFileRepository
from goal import Goal


class Test(TestCase):
    def test_fromJSON(self):
        json = """
        {
            "title": "title",
            "specific": "spec",
            "measurable": "meas",
            "achievable": "ach",
            "realistic": "real",
            "time_bound": "time b."
        }
        """

        goal = from_json(json)

        self.assertEqual(goal.title, "title")
        self.assertEqual(goal.specific, "spec")
        self.assertEqual(goal.measurable, "meas")
        self.assertEqual(goal.achievable, "ach")
        self.assertEqual(goal.realistic, "real")
        self.assertEqual(goal.time_bound, "time b.")

    def test_toJson(self):
        goal = Goal("title", ["spec1", "spec2"], "meas", "ach", "real", "time b.")

        expected = """{
    "title": "title",
    "specific": [
        "spec1",
        "spec2"
    ],
    "measurable": "meas",
    "achievable": "ach",
    "realistic": "real",
    "time_bound": "time b."
}"""
        self.assertEqual(to_json(goal), expected)

    def test_json_ser_de(self):
        goal = Goal("title", ["spec1", "spec2"], "meas", "ach", "real", "time b.")
        deserialized = from_json(to_json(goal))

        self.assertEqual(goal.title, deserialized.title)
        self.assertEqual(goal.specific, deserialized.specific)
        self.assertEqual(goal.measurable, deserialized.measurable)
        self.assertEqual(goal.achievable, deserialized.achievable)
        self.assertEqual(goal.realistic, deserialized.realistic)
        self.assertEqual(goal.time_bound, deserialized.time_bound)

    def test_list_goals(self):
        goals = [
            Goal("title1", ["spec1", "spec2"], "meas", "ach", "real", "time b."),
            Goal("title2", ["spec1", "spec2"], "meas", "ach", "real", "time b."),
            Goal("title3", ["spec1", "spec2"], "meas", "ach", "real", "time b.")
        ]

        repository = GoalFileRepository("tmp/goals.json")
        [repository.add(g) for g in goals]

        from_db = repository.list()
        for i in range(len(goals)):
            goal = goals[i]
            deserialized = from_db[i]
            self.assertEqual(goal.title, deserialized.title)
            self.assertEqual(goal.specific, deserialized.specific)
            self.assertEqual(goal.measurable, deserialized.measurable)
            self.assertEqual(goal.achievable, deserialized.achievable)
            self.assertEqual(goal.realistic, deserialized.realistic)
            self.assertEqual(goal.time_bound, deserialized.time_bound)


if __name__ == '__main__':
    unittest.main()
