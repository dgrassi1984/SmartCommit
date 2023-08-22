#!/usr/bin/env python3

"""
ai_commit_helper.py

Description:
------------

This script uses OpenAI's GPT-3 model to automatically generate meaningful git
commit messages given a set of changes, either as a string or from a .diff file. 
The program uses the openai model to provide a summary and detailed bullet 
points of the changes.

Dependencies:
-------------
- OpenAI Python SDK
- Python 3.6 or higher

Usage:
------
Run the script passing changes as a string or the path to a .diff file:
    
    python3 ai_commit_helper.py "Your changes here"
    OR
    python3 ai_commit_helper.py /path/to/changes.diff
"""

import openai
import argparse
import os

def set_openai_key():
    if "OPENAI_API_KEY" not in os.environ:
        raise Exception("OPENAI_API_KEY not found in environment variables")
    openai.api_key = os.environ["OPENAI_API_KEY"]


def get_args():
    parser = argparse.ArgumentParser(
        description="Generate a git commit message using GPT-3"
    )

    parser.add_argument(
        "changes",
        metavar="changes",
        type=str,
        help="Changes as a string or path to a .diff file",
    )

    parser.add_argument(
        "-i", "--instruction",
        default="",
        help="Additional instruction to guide the AI's response"
    )

    return parser.parse_args()


def get_changes(args):
    if args.changes.endswith(".diff"):
        if os.path.isfile(args.changes):
            with open(args.changes, "r") as file:
                return file.read()
        else:
            raise Exception(f"{args.changes} does not exist.")
    else:
        return args.changes


def generate_commit_message(changes, instruction):
    system_prompt = (
        "You are a helpful assistant that generates meaningful commit messages based "
        "on a list of changes. The commit message should include a title summarizing "
        "the changes and bullets '-' for the detailed changes. Each change should be "
        "on a new line in an imperative style. Please ensure that no line "
        "exceeds 80 characters in length."
    )

    changes = "Write a git commit message for the following changes: " + changes

    # Add the instruction to the AI messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": changes},
    ]

    if instruction:
        messages.append({"role": "user", "content": instruction})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,  # type: ignore
    )

    commit_message = response.choices[0].message["content"]  # type: ignore
    return commit_message


def main():
    set_openai_key()

    args = get_args()

    changes = get_changes(args)

    commit_message = generate_commit_message(changes, args.instruction)

    print(commit_message)


if __name__ == "__main__":
    main()
