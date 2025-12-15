import json
import datetime
from argparse import ArgumentParser, Namespace
from pathlib import Path

tasksfile = Path("tasks.json")
if tasksfile.is_file():
    with open("tasks.json") as f:
        data = json.load(f)
else:
    data = {'tasks': []}
    with open("tasks.json", mode="x", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


parser = ArgumentParser()

sub = parser.add_subparsers(dest="cmd", required=True)

add = sub.add_parser("add")
add.add_argument("description")

add = sub.add_parser("delete")
add.add_argument("ID")

add = sub.add_parser("update")
add.add_argument("ID")
add.add_argument("newDescription")

add = sub.add_parser("mark-in-progress")
add.add_argument("ID")

add = sub.add_parser("mark-todo")
add.add_argument("ID")

add = sub.add_parser("mark-done")
add.add_argument("ID")

args: Namespace = parser.parse_args()

#add task
if args.cmd == "add":
    last_id_plus_one = len(data["tasks"]) + 1
    new_task = {"id": last_id_plus_one, "description": args.description, "status": "todo", "createdAt": str(datetime.datetime.now()), "updatedAt": "never"}
    data["tasks"].append(new_task)

#delete task
if args.cmd == "delete":
    del data["tasks"][int(args.ID) - 1]
    for i, task in enumerate(data["tasks"], start=1):
        data["tasks"][i-1]["id"] = str(i)
#update task
if args.cmd == "update":
    data["tasks"][int(args.ID) - 1]["description"] = args.newDescription
    data["tasks"][int(args.ID) - 1]["updatedAt"] = str(datetime.datetime.now())

#mark task
if args.cmd == "mark-in-progress":
    data["tasks"][int(args.ID) - 1]["status"] = "in-progress"
    data["tasks"][int(args.ID) - 1]["updatedAt"] = str(datetime.datetime.now())


if args.cmd == "mark-done":
    data["tasks"][int(args.ID) - 1]["status"] = "done"
    data["tasks"][int(args.ID) - 1]["updatedAt"] = str(datetime.datetime.now())


if args.cmd == "mark-todo":
    data["tasks"][int(args.ID) - 1]["status"] = "todo"
    data["tasks"][int(args.ID) - 1]["updatedAt"] = str(datetime.datetime.now())

print(data)

with open("tasks.json", mode="w", encoding="utf-8") as write_file:
    json.dump(data, write_file, indent=2)
