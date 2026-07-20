import json


def load_json_file(filename):

    try:

        with open(filename, "r") as file:
            return json.load(file)

    except FileNotFoundError:

        raise FileNotFoundError(
            f"""
FILE ERROR:
Could not find file:
{filename}

Check:
- File name is correct
- File exists in project folder
"""
        )


    except json.JSONDecodeError as e:

        raise ValueError(
            f"""
JSON ERROR:
Invalid JSON format.

File:
{filename}

Line:
{e.lineno}

Column:
{e.colno}

Fix the JSON syntax and try again.
"""
        )