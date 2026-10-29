"""Evaluate numeric postfix expressions using a Stack."""

import re
from stack import Stack


class PostfixEvaluator:
    """Evaluate space-separated numbers and binary operators."""

    def _apply_operator(self, operator, left, right):
        """Apply an operator; raise ZeroDivisionError for division by zero."""
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return left / right

    def evaluate(self, expression):
        """Return the result; raise ValueError for malformed expressions.

        Input must contain space-separated numeric operands and +, -, *, /.
        Each operator needs two operands, and one result must remain.
        """
        operands = Stack()
        tokens = expression.split()

        if not tokens:
            raise ValueError("Expression is empty.")

        for token in tokens:
            if token in ("+", "-", "*", "/"):
                if operands.size() < 2:
                    raise ValueError(
                        f"Insufficient operands for '{token}'."
                    )

                right = operands.pop()
                left = operands.pop()
                result = self._apply_operator(token, left, right)
                operands.push(result)

            elif re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", token):
                value = float(token) if "." in token else int(token)
                operands.push(value)

            else:
                raise ValueError(f"Invalid token: '{token}'.")

        if operands.size() != 1:
            raise ValueError("Too many operands.")

        return operands.pop()


if __name__ == "__main__":
    evaluator = PostfixEvaluator()

    valid_cases = [
        ("5 3 +", 8),
        ("8 2 - 3 +", 9),
        ("5 3 8 * +", 29),
        ("6 2 / 3 +", 6.0),
        ("5 8 + 3 -", 10),
        ("5 3 + 8 *", 64),
        ("8 2 3 * + 6 -", 8),
        ("5 3 8 * + 2 /", 14.5),
        ("8 2 + 3 6 * -", -8),
        ("5 3 + 8 2 / -", 4.0),
        ("35 27 + 3 *", 186),
        ("23 30 15 * /", 23 / (30 * 15)),
        ("8 2 /", 4),
        ("2.5 4 *", 10),
    ]

    for expression, expected in valid_cases:
        actual = evaluator.evaluate(expression)
        assert actual == expected, (expression, expected, actual)

    invalid_cases = [
        ("26 28 + 32 2 ; - 5 /", ValueError),
        ("2 3 4 +", ValueError),
        ("20 29 9 * ;", ValueError),
        ("25 23 - +", ValueError),
        ("8 0 /", ZeroDivisionError),
        ("5 +", ValueError),
        ("3 + 4", ValueError),
        ("", ValueError),
        ("3 4 &", ValueError),
    ]

    for expression, expected_error in invalid_cases:
        try:
            evaluator.evaluate(expression)
        except expected_error:
            pass
        else:
            raise AssertionError(
                f"Expected {expected_error.__name__}: {expression}"
            )

    print("All PostfixEvaluator tests passed.")
