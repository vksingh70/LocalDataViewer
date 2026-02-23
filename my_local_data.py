from mcp.server.fastmcp import FastMCP
import os
import subprocess
import sys
mcp = FastMCP("Infrastructure-Helper")

# Tool to read local server logs or terraform files
@mcp.tool()
def read_local_config(file_name: str) -> str:
    """Reads a configuration file from the local /configs directory."""
    safe_path = os.path.join("./configs", file_name)
    with open(safe_path, "r") as f:
        return f.read()

# Tool to list available local scripts
@mcp.tool()
def list_scripts() -> list:
    """Lists all automation scripts in the /scripts folder."""
    return os.listdir("./scripts")

@mcp.tool()
def execute_script(script_name: str) -> str:
    """Executes a Python script from the /scripts folder and returns its output."""
    # Security: Restrict execution to only the scripts folder
    script_path = os.path.abspath(os.path.join("./scripts", script_name))
    
    if not script_path.startswith(os.path.abspath("./scripts")):
        return "Error: Access denied. Scripts must be in the /scripts folder."

    try:
        # Run the script and capture the output (stdout and stderr)
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30  # Safety: kill script if it hangs
        )
        
        output = f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}"
        
        return output
    except Exception as e:
        return f"Execution Failed: {str(e)}"

if __name__ == "__main__":
    mcp.run()