class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: b / a if a != 0 else "Error: Division by zero", # Added division by zero check
        }
        # Adjusted precedence to reflect standard mathematical order of operations
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression) # Use a more robust tokenizer
        return self._evaluate_rpn(self._infix_to_rpn(tokens)) # Evaluate using Reverse Polish Notation (RPN)

    def _tokenize(self, expression):
        # Simple tokenizer, can be expanded for more complex expressions (e.g., with parentheses)
        import re
        return re.findall(r"(\d+\.?\d*|\+|\-|\*|\/)", expression)

    def _infix_to_rpn(self, tokens):
        output = []
        op_stack = []

        for token in tokens:
            if token.replace('.', '', 1).isdigit(): # Check if token is a number
                output.append(token)
            elif token in self.operators:
                while (
                    op_stack
                    and op_stack[-1] in self.operators
                    and self.precedence.get(op_stack[-1], 0) >= self.precedence.get(token, 0)
                ):
                    output.append(op_stack.pop())
                op_stack.append(token)
            # Add support for parentheses here if needed in the future
            # elif token == '(':
            #     op_stack.append(token)
            # elif token == ')':
            #     while op_stack and op_stack[-1] != '(':
            #         output.append(op_stack.pop())
            #     if op_stack and op_stack[-1] == '(':
            #         op_stack.pop() # Discard the opening parenthesis

        while op_stack:
            output.append(op_stack.pop())

        return output

    def _evaluate_rpn(self, rpn_tokens):
        value_stack = []

        for token in rpn_tokens:
            if token.replace('.', '', 1).isdigit(): # Check if token is a number
                value_stack.append(float(token))
            elif token in self.operators:
                if len(value_stack) < 2:
                    raise ValueError(f"Invalid expression: Not enough operands for operator '{token}'")
                
                b = value_stack.pop()
                a = value_stack.pop()

                # Handle division by zero specifically
                if token == "/" and b == 0:
                    return "Error: Division by zero"
                
                result = self.operators[token](b, a) # Note the order: b is popped first, then a. So it's a op b
                value_stack.append(result)
            else:
                 raise ValueError(f"Invalid token in RPN expression: {token}")


        if len(value_stack) != 1:
            raise ValueError("Invalid expression format")

        return value_stack[0]

