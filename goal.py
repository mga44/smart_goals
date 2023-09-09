import json
import string
from collections import namedtuple
from dataclasses import dataclass, field
from json import JSONEncoder
from os.path import exists
from types import SimpleNamespace as Namespace, SimpleNamespace
from termcolor import colored

"""
    The purpose of this class is to represent goal that are relevant to the SMART methodology
    and
    """


@dataclass
class Goal:
    def __init__(self,
                 title=None,
                 specific=None,
                 measurable=None,
                 achievable=None,
                 realistic=None,
                 time_bound=None,
                 achieved=False,
                 other_obj=None
                 ):
        if other_obj:
            self.title = getattr(other_obj, 'title', "")
            self.specific = getattr(other_obj, 'specific', "")
            self.measurable = getattr(other_obj, 'measurable', "")
            self.achievable = getattr(other_obj, 'achievable', "")
            self.realistic = getattr(other_obj, 'realistic', "")
            self.time_bound = getattr(other_obj, 'time_bound', "")
            self.achieved = getattr(other_obj, 'achieved', False)
        else:
            self.title = title
            self.specific = specific
            self.measurable = measurable
            self.achievable = achievable
            self.realistic = realistic
            self.time_bound = time_bound
            self.achieved = achieved

    def __str__(self):
        return f'''{colored(self.title, 'blue')}
    specific: {self.specific}
    measurable: {self.measurable}
    achievable: {self.achievable}
    realistic: {self.realistic}
    time_bound: {self.time_bound}
    achieved: {self.achieved}       
        '''


def to_json(goal):
    return json.dumps(goal, default=lambda o: o.__dict__, sort_keys=False, indent=4, ensure_ascii=False)


def from_json(json_string: string):
    return json.loads(json_string, object_hook=lambda d: Goal(other_obj=Namespace(**d)))


class GoalEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class GoalFileRepository:
    def __init__(self, file="./goals.json"):
        self.file = file

    def list(self):
        repository = open(self.file, "r", encoding="UTF-8")
        lines = repository.readlines()
        repository.close()
        return from_json("".join(lines)) if lines else list()

    def get(self, title):
        result = list(filter(lambda goal: goal.title == title, self.list()))
        if len(result) == 0:
            return None

        return result[0]

    def delete(self, goal):
        goals = self.list()
        goals.remove(goal)
        self._write_to_file(goals)

    def update(self, source, updated):
        updated_goal_list = list(map(lambda goal: updated if goal.title == source.title else goal, self.list()))
        self._write_to_file(updated_goal_list)

    def add(self, goal):
        goal_list = self.list().append(goal)
        self._write_to_file(goal_list)

    def _write_to_file(self, goal_list):
        repository = open(self.file, "w", encoding="UTF-8")
        repository.write(to_json(goal_list))
        repository.close()
