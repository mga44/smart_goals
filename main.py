import argparse
import copy
import webbrowser

from termcolor import colored
from tabulate import tabulate

from goal import GoalFileRepository, from_json, Goal


def print_ordered(num=1):
    num = num + 1
    return lambda x: f'{num}. {str(x)}'


def flatten_output(output):
    if isinstance(output, list):
        return ' | '.join(output)

    return output


def print_fetch_result(mapped_to_tabulate_format):
    print(tabulate(
        mapped_to_tabulate_format,
        headers=("Title", "Specific", "Measurable", "Achievable", "Relevant", "Time-bound", "Achieved"),
        tablefmt="rounded_grid",
        maxcolwidths=20,
        missingval="-"
    ))


def get_string_or_split(str):
    values = str.split(";")
    return str if len(values) == 1 else values


def prepare_table_print(x):
    return [
        flatten_output(x.title),
        flatten_output(x.specific),
        flatten_output(x.measurable),
        flatten_output(x.achievable),
        flatten_output(x.realistic),
        flatten_output(x.time_bound),
        colored("✔", 'green') if x.achieved else colored("X", 'red')
    ]


def info(info_string):
    return colored(info_string + '\n\t', 'dark_grey')


parser = argparse.ArgumentParser()
parser.add_argument("operation", help="one of [add, list, reference]")
parser.add_argument("-f", "--full", action="store_true", help="print all goals")
parser.add_argument("--json", help="add goal in JSON format")
parser.add_argument("--title", help="specify goal title for get/update/delete")
parser.add_argument("--achieved")
args = parser.parse_args()
repository = GoalFileRepository('./goals.json.bak')

match args.operation:
    case "list":
        goals = repository.list()
        lp = 0
        if not args.full:
            print("\n".join(map(lambda x: print_ordered(lp)(x.title), goals)))
        else:
            all_goals_in_tabulate_format = map(lambda x: prepare_table_print(x), goals)
            print_fetch_result(all_goals_in_tabulate_format)
    case "get":
        if not args.title:
            raise ValueError("Title argument must be specified")

        goal = repository.get(args.title)
        if goal:
            print(goal)
        else:
            print(f"Goal with title '{args.title}' not found.")
    case "add":
        if args.json:
            s = args.json
            repository.add(from_json(s))
        else:
            print(info("For passing list of elements separate them with semicolon."))
            repository.add(Goal(
                input(info("Please enter title: ")),
                get_string_or_split(input(info("Signifiers that this goal was achieved: "))),
                get_string_or_split(input(info("How will the progress be measured: "))),
                get_string_or_split(input(info("Arguments to ensure that this goal can be achieved: "))),
                get_string_or_split(input(info("Why this goal is important: "))),
                get_string_or_split(input(info("Deadline for this goal: "))),
            ))
        print(colored("Goal added successfully", 'green'))
    case "update":
        if args.title is None:
            raise ValueError("Updated title was not specified.")

        source = repository.get(args.title)
        updated = copy.copy(source)
        updated.achieved = args.achieved
        repository.update(source, updated)
        print(colored("Goal updated successfully", 'green'))
    case "delete":
        if not args.title:
            raise ValueError("Title argument must be specified")

        fetched = repository.get(args.title)
        if not fetched:
            print(f"Goal with title '{args.title}' not found")

        repository.delete(fetched)
    case "reference":
        webbrowser.open("https://www.mindtools.com/a4wo118/smart-goals")
    case default:
        raise ValueError(f'Not supported operation: ${args.operation}')
