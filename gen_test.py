from requests import post
from string import Template
from json import dumps
import random
import click
import glob
import os


####################################################################################################
####################################################################################################
############################################### CLI ################################################
####################################################################################################
####################################################################################################
@click.command()
@click.option(
    "-r",
    "--rand",
    is_flag=True,
    help="Generate random tests",
    default=True,
    show_default=True,
)
@click.option(
    "-n",
    "--num-tests",
    default=5,
    help="Number of random tests to generate",
    show_default=True,
)
@click.option(
    "-x",
    "--num-lines",
    default=10,
    help="Number of lines in random tests",
    show_default=True,
)
@click.option(
    "-s",
    "--specification",
    is_flag=True,
    help="Generate tests based on specification",
    default=True,
    show_default=True,
)
@click.option(
    "-c",
    "--cleanup",
    is_flag=True,
    help="Cleanup generated tests",
    default=False,
    show_default=True,
)
def main(rand, num_tests, num_lines, specification, cleanup):
    path = "./v1/"

    if cleanup:
        for f in glob.glob(f"{path}tests/test_random_*.br"):
            os.remove(f)
        for f in glob.glob(f"{path}tests/test_pass_*.br"):
            os.remove(f)
        for f in glob.glob(f"{path}fails/test_fail_*.br"):
            os.remove(f)
        return
    total = 0
    if rand:
        for i in range(num_tests):
            test = generate_random_brewin(num_lines)
            write_p_test(test, f"{path}tests/test_random_{i}.br")
            total += 1

    if specification:
        for i, test in enumerate(PASSING_TESTS):
            write_p_test(test, f"{path}tests/test_pass_{i}.br")
            total += 1
        for i, test in enumerate(FAILING_TESTS):
            write_f_test(test, f"{path}fails/test_fail_{i}.br")
            total += 1

    print(f"Success! {total} test cases added.")
    return 0


####################################################################################################
####################################################################################################
############################################# HELPERS ##############################################
####################################################################################################
####################################################################################################


def write_p_test(test, path):
    with open(path, "x") as f:
        output = test_output(test[0], test[1])
        f.write(
            PASS_FORMAT.format(
                program=test[0],
                input=(test[1] + "\n") if test[1] else "",
                output=(output + "\n") if output else "",
            )
        )


def write_f_test(test, path):
    with open(path, "x") as f:
        output = test_output(test, "").split(":")[0]
        f.write(FAIL_FORMAT.format(program=test, output=output + "\n"))


def test_output(program, stdin):
    url = "https://barista-f23.fly.dev/f24"
    data = {"program": program, "stdin": stdin, "version": "1"}
    headers = {
        "Origin": "https://barista-f23.fly.dev",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Content-Type": "application/json",
    }
    response = post(url, data=dumps(data), headers=headers)
    if response.status_code != 200:
        print(response.text)
    result = response.json()["res"]
    return "\n".join(result) if isinstance(result, list) else result


def generate_random_expression(defined_vars):
    """Generates a random arithmetic expression with chained parentheses."""
    operators = ["+", "-"]
    if random.choice([True, False]):
        # Use a constant
        return str(random.randint(0, 100))
    else:
        # Start with a variable or constant
        expr = (
            random.choice(list(defined_vars))
            if defined_vars
            else str(random.randint(0, 100))
        )
        for _ in range(random.randint(1, 5)):  # Randomly chain 1 to 3 operations
            operator = random.choice(operators)
            if random.choice([True, False]) and defined_vars:
                # Use another variable
                next_expr = random.choice(list(defined_vars))
            else:
                # Use a constant
                next_expr = str(random.randint(0, 100))
            # Chain operations inside parentheses
            expr = f"({expr} {operator} {next_expr})"
        return expr


def generate_random_brewin(n):
    # Define possible variable names and constants
    variables = ["foo", "_bar", "bletch", "prompt", "boo", "num", "x", "y", "z"]
    inputi_called = False
    inputs = []

    # Initialize the Brewin program
    program = "func main() {\n"
    defined_vars = set()  # Track defined variables
    assigned_vars = set()  # Track assigned variables
    i = 0
    while i < n:
        # Randomly decide the type of statement to add
        statement_type = random.choice(["var", "assign", "inputi", "print"])

        if statement_type == "var":
            var_name = random.choice(variables)
            if var_name not in defined_vars:
                program += f"    var {var_name};\n"
                defined_vars.add(var_name)
                i += 1

        elif statement_type == "assign" and defined_vars:
            var_name = random.choice(list(defined_vars))
            # Randomly assign a constant or another variable
            choice = random.choice([1, 2, 3])
            if choice == 1:
                value = random.randint(0, 100)  # Assign a constant
            elif choice == 2:
                value = random.choice(list(assigned_vars))  # Assign another variable
                if value == var_name:
                    continue
            else:
                value = generate_random_expression(assigned_vars)  # Assign an expression
            program += f"    {var_name} = {value};\n"
            assigned_vars.add(var_name)
            i += 1

        elif statement_type == "inputi" and defined_vars:
            var_name = random.choice(list(defined_vars))
            if not inputi_called:
                prompt = "Enter a number: "
                program += f'    {var_name} = inputi("{prompt}");\n'
                inputs.append(
                    str(random.randint(1, 100))
                )  # Store random input for inputi
                inputi_called = True
                assigned_vars.add(var_name)
                i += 1
            else:
                program += f"    {var_name} = inputi();\n"
                inputs.append(str(random.randint(1, 100)))  # Store another input
                assigned_vars.add(var_name)
                i += 1

        elif statement_type == "print" and assigned_vars:
            var_name = random.sample(
                list(assigned_vars), random.randint(1, len(assigned_vars))
            )
            program += f"    print({','.join(var_name)});\n"
            i += 1

    program += "}\n"

    # Return program and inputs
    input_str = "\n".join(inputs) if inputs else ""
    return program, input_str


####################################################################################################
####################################################################################################
############################################ CONSTANTS #############################################
####################################################################################################
####################################################################################################
pass_test_main_function = (
    """func main() {
    print("Line 1");
    print("Line 2");
}""",
    "",
)
fail_test_main_function = """func nonMain() {
    print("Line 1");
}"""

pass_test_vardef = (
    """func main() {
    var foo;
    var _bar;
}""",
    "",
)

pass_test_assign = (
    """func main() {
    var foo;
    var _bar;
    foo = 10;
    _bar = 3 + foo;
    var bletch;
    bletch = 3 - (5+2);
    var prompt;
    prompt = "Enter a number: ";
    var boo;
    boo = inputi();
    boo = inputi(prompt);
}""",
    "5\n6",
)

pass_test_func_call = (
    """func main() {
    var a;
    var b;
    a = 5;
    b = 1;
    print(5);
    print("hello world");
    print("the answer is: ", b);
    print("the answer is: ", b + (a - 5), "!");
}""",
    "",
)

fail_test_vardef = """func main() {
    var x;
    var x;
}"""

fail_test_assign = """func main() {
    x = 5;
}"""

fail_test_func_call = """func main() {
    foo();
}"""

pass_test_expr = (
    """func main() {
    var x;
    var y;
    x = 3 + 5;
    y = 4 + inputi("enter a number: ");
    x = 3 - (3 + (2 + inputi()));
    y = ((5 + (6 - 3)) - ((2 - 3) - (1 - 7)));
    print(y);
    print(x);
}""",
    "5\n5",
)

fail_test_expr_add_str = """func main() {
    var x;
    x = 3 + "hello";
}"""

fail_test_expr_inputi = """func main() {
    var x;
    x = inputi("hello", "hi");
}"""

fail_test_expr_undef_var = """func main() {
    var x;
    x = y + 3;
}"""


PASS_FORMAT = "\n".join(
    [
        "{program}\n",
        "/*",
        "*IN*",
        "{input}*IN*",
        "*OUT*",
        "{output}*OUT*",
        "*/",
    ]
)

FAIL_FORMAT = "\n".join(["{program}\n", "/*", "*OUT*", "{output}*OUT*", "*/"])

PASSING_TESTS = [
    pass_test_main_function,
    pass_test_vardef,
    pass_test_assign,
    pass_test_func_call,
    pass_test_expr,
]

FAILING_TESTS = [
    fail_test_main_function,
    fail_test_vardef,
    fail_test_assign,
    fail_test_func_call,
    fail_test_expr_add_str,
    fail_test_expr_inputi,
    fail_test_expr_undef_var,
]

if __name__ == "__main__":
    main()
