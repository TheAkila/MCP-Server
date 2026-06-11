from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator", port=8001)


@mcp.tool()
def add(a: float, b: float) -> float:
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("division by zero")
    return a / b


@mcp.tool()
def power(a: float, b: float) -> float:
    return a ** b


@mcp.tool()
def mod(a: int, b: int) -> int:
    return a % b


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
