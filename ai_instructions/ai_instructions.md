# AI instructions

## Python functions

- When writing Python functions, always add docstrings in the Google style:

``` Python

def divide(a: float, b: float) -> float:
    """Divide two numbers.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient of a divided by b.

    Raises:
        ZeroDivisionError: If b is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```

## Deploy via Docker

We want to deploy our product on a server.
Therefore, make sure that the product can
always be started with a docker or docker-compose command.

## System prompt

- Suggest only code that a junior developer would understand.
- Don't create unnecessary comments.
  For instance don't write `# load data` when the next line is `load_file(filename)`
