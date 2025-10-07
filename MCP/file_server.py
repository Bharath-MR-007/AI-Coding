import os
from fastmcp import FastMCP

# 1. Define the tool function with a CLEAR docstring.
def read_local_file(filepath: str) -> str:
    """
    Reads the content of a local text file at the given filepath. 
    This tool is useful for fetching context from project files.
    """
    try:
        # Security Note: In a real app, you must sanitize and restrict file paths!
        # For this simple example, we use the raw path.
        with open(filepath, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found at path: {filepath}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# 2. Create the FastMCP server instance and register the tool.
app = FastMCP(tools=[read_local_file])

# 3. The FastMCP run method automatically handles the MCP protocol 
# (initialization, requests) using standard input/output (stdio).
if __name__ == "__main__":
    app.run()
