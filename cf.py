#!usr/bin/python3
"""
Script to automate testing codeforces solutions.

To avoid sending solution failing pre-tests :P.
"""

import sys
import argparse
import difflib
import requests
import subprocess
from wasabi import color
from bs4 import BeautifulSoup

def diff_strings(a: str, b: str):
    """
    Creates a colored string with a formated string of the diff from a to b.

    Hard copied from https://gist.github.com/ines/04b47597eb9d011ade5e77a068389521.
    """
    output = []
    matcher = difflib.SequenceMatcher(None, a, b)
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == "equal":
            output.append(a[a0:a1])
        elif opcode == "insert":
            output.append(color(b[b0:b1], fg=16, bg="green"))
        elif opcode == "delete":
            output.append(color(a[a0:a1], fg=16, bg="red"))
        elif opcode == "replace":
            output.append(color(b[b0:b1], fg=16, bg="green"))
            output.append(color(a[a0:a1], fg=16, bg="red"))
    return "".join(output)


def compile_cpp(src_path: str, exec_path: str, gpp_options=""):
    """
    Compiles the source file and returns the executable name.

    Args:
        src_path (str): The path to the source file.
        exec_path (str): The executable path.
        gpp_options (str): Extra options to pass to g++.
    """
    subprocess.run(["g++", src_path, "-o", exec_path])


def get_test_cases(problem: str, contest: str) -> list[tuple[str, str]]:
    """
    Gets the test cases for the given problem and contest.

    Args:
        problem (str): The problem id, e.g. A, B, C1.
        contest (str): The contest number, e.g. 1890.
    Returns:
        tuple[str, str]: The input and output test cases.
    """
    problem_url = f"https://codeforces.com/contest/{contest}/problem/{problem}"
    # Get the problem page
    page = requests.get(problem_url, timeout=3)
    # Parse the page
    soup = BeautifulSoup(page.content, "html.parser")
    # Get the sample tests
    sample_test_inputs = soup.find("div", class_="sample-test").findAll("div", class_="input")
    sample_test_outputs = soup.find("div", class_="sample-test").findAll("div", class_="output")
    # Get the sample inputs
    sample_inputs = [div_input.find("pre").get_text(separator="\n").strip("\n") for div_input in sample_test_inputs]
    # Get the sample outputs
    sample_outputs = [div_output.find("pre").get_text(separator="\n").strip("\n") for div_output in sample_test_outputs]
    return list(zip(sample_inputs, sample_outputs))


def test(executable: str, cases: list[tuple[str, str]], print_diff=True) -> bool:
    """
    Tests the given executable against the test cases for the given problem and contest.

    Args:
        executable (str): The executable to test.
        problem (str): The problem id, e.g. A, B, C1.
        contest (str): The contest number, e.g. 1890.
        print_diff (bool): Whether to print the diff of the test cases.
    Returns:
        bool: True if all test cases pass, False otherwise.
    """

    tests_passing = True
    # Call the executable with the test cases
    for in_, out_ in cases:
        # Call the executable with the input
        out = subprocess.run([f"./{executable}"], input=in_, capture_output=True, text=True, check=True)
        # Check if the output matches the expected output
        if out.stdout.strip("\n") != out_:
            # Print the diff if required
            if print_diff:
                print(diff_strings(out.stdout,out_))

            print("Wanted:")
            print(out_)
            print("Got:")
            print(out.stdout)
            tests_passing = False
    return tests_passing


if __name__ == '__main__':
    # Parse the problem name from the CLI argument
    parser = argparse.ArgumentParser(description="Codeforces CLI tool to test and submit solutions")
    parser.add_argument("--problem", required=True, help="The problem id, e.g. A, B, C1")
    parser.add_argument("--contest", required=False, help="The contest number, e.g. 1890. If not given looks for codeforces/<contest_number> in the pwd.")
    parser.add_argument("src", help="The source file to test/submit")
    args = parser.parse_args()

    executable_name = args.problem

    compile_cpp(args.src, executable_name)
    # Get the test cases
    cases = get_test_cases(args.problem, args.contest)
    from os import path
    assert path.isfile(executable_name), f"Executable {executable_name} not found!"
    if test(executable_name, cases):
        print(f'{color(f"All {len(cases)} pre-tests passed", fg=16, bg="green")}  🚀')
        sys.exit(0)
    else:
        print(f'{color("Some tests failed", fg=16, bg="red")} 💣')
        sys.exit(1)
