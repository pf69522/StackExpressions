"""Demonstrate expression conversion, evaluation, and error handling."""

from infix_converter import InfixToPostfixConverter
from postfix_evaluator import PostfixEvaluator


def main():
    """Run valid and invalid examples for both components."""
    evaluator = PostfixEvaluator()
    converter = InfixToPostfixConverter()

    print("----- Postfix Evaluator -----")

    postfix_cases = [
        "5 3 +",
        "8 2 - 3 +",
        "35 27 + 3 *",
        "5 3 8 * + 2 /",
        "8 2 /",
        "2 3 4 +",
        "5 +",
        "8 0 /",
        "3 4 &",
    ]

    for expression in postfix_cases:
        try:
            result = evaluator.evaluate(expression)
            print(f"[{expression}] = {result}")
        except (ValueError, ZeroDivisionError) as error:
            print(f"[{expression}] -> ERROR: {error}")

    print("\n----- Infix to Postfix Converter -----")

    infix_cases = [
        "A + B",
        "A + B * C",
        "(A + B) * C",
        "A - B + C",
        "A / B * C",
        "(A + B * (C - D)) / E",
        "A + * B",
        "(A + B",
        "A B + C",
        "A + B @ C",
    ]

    for expression in infix_cases:
        try:
            postfix = converter.convert(expression)
            print(f"[{expression}] -> [{postfix}]")
        except ValueError as error:
            print(f"[{expression}] -> ERROR: {error}")

    print("\n----- Combined Conversion and Evaluation -----")

    combined_cases = [
        ("(35 + 27) * 3", 186),
        ("8 / 2 * 3", 12),
        ("5 + 3 * 8", 29),
        ("(5 + 3 * (8 - 6)) / 2", 5.5),
    ]

    for expression, expected in combined_cases:
        postfix = converter.convert(expression)
        result = evaluator.evaluate(postfix)
        assert result == expected, (expression, expected, result)
        print(f"[{expression}] -> [{postfix}] = {result}")

    print("\nAll combined integration tests passed.")


if __name__ == "__main__":
    main()