"""Convert infix expressions to postfix using a Stack."""

import re
from stack import Stack


class InfixToPostfixConverter:
    """Convert expressions with binary +, -, *, / and parentheses."""

    def _precedence(self, operator):
        """Return an operator's precedence."""
        if operator in ("*", "/"):
            return 2
        return 1

    def convert(self, expression):
        """Return space-separated postfix notation.

        Accept variable names or unsigned numbers as operands.
        Raise ValueError for invalid tokens or malformed expressions.
        Unary operators and implicit multiplication are unsupported.
        """
        tokens = re.findall(
            r"[A-Za-z_][A-Za-z_0-9]*|[0-9]+(?:\.[0-9]+)?|\S",
            expression
        )

        if not tokens:
            raise ValueError("Expression is empty.")

        operators = Stack()
        output = []
        expecting_operand = True

        for token in tokens:
            if re.fullmatch(
                r"[A-Za-z_][A-Za-z_0-9]*|[0-9]+(?:\.[0-9]+)?",
                token
            ):
                if not expecting_operand:
                    raise ValueError(f"Misplaced operand: '{token}'.")
                output.append(token)
                expecting_operand = False

            elif token == "(":
                if not expecting_operand:
                    raise ValueError("Missing operator before '('.")
                operators.push(token)

            elif token == ")":
                if expecting_operand:
                    raise ValueError("Missing operand before ')'.")

                while not operators.is_empty() and operators.peek() != "(":
                    output.append(operators.pop())

                if operators.is_empty():
                    raise ValueError("Mismatched closing parenthesis.")

                operators.pop()
                expecting_operand = False

            elif token in ("+", "-", "*", "/"):
                if expecting_operand:
                    raise ValueError(f"Misplaced operator: '{token}'.")

                # Equal precedence is popped for left associativity.
                while (
                    not operators.is_empty()
                    and operators.peek() != "("
                    and self._precedence(operators.peek())
                    >= self._precedence(token)
                ):
                    output.append(operators.pop())

                operators.push(token)
                expecting_operand = True

            else:
                raise ValueError(f"Invalid token: '{token}'.")

        if expecting_operand:
            raise ValueError("Expression is incomplete.")

        while not operators.is_empty():
            operator = operators.pop()
            if operator == "(":
                raise ValueError("Mismatched opening parenthesis.")
            output.append(operator)

        return " ".join(output)


if __name__ == "__main__":
    converter = InfixToPostfixConverter()

    valid_cases = [
        ("A + B", "A B +"),
        ("A + B * C", "A B C * +"),
        ("(A + B) * C", "A B + C *"),
        ("A * B + C / D", "A B * C D / +"),
        ("(A + B) * (C - D)", "A B + C D - *"),
        ("A + B * C - D / E", "A B C * + D E / -"),
        ("A * (B + C) / D", "A B C + * D /"),
        ("(A + B * C) / (D - E)", "A B C * + D E - /"),
        ("A + (B - C) * D", "A B C - D * +"),
        ("(A + B * (C - D)) / E", "A B C D - * + E /"),
        ("A - B + C", "A B - C +"),
        ("A / B * C", "A B / C *"),
        ("((((((((A + B))))))))", "A B +"),
        ("35 + 27 * 3", "35 27 3 * +"),
        ("A+B*C", "A B C * +"),
    ]

    for expression, expected in valid_cases:
        actual = converter.convert(expression)
        assert actual == expected, (expression, expected, actual)

    invalid_cases = [
        "A + B ) C",
        "A + B ; C",
        "+ A B",
        "A + * B",
        "A B + C",
        "A + ) B * C (",
        "(A + B",
        "A + B)",
        "",
        "A +",
        "()",
        "A + B @ C",
        "A(B + C)",
        "(A + B) C",
    ]

    for expression in invalid_cases:
        try:
            converter.convert(expression)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected ValueError: {expression}")

    print("All InfixToPostfixConverter tests passed.")