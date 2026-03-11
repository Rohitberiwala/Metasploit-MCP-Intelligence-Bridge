import os
import sys
from mcp.server.fastmcp import FastMCP
from pymetasploit3.msfrpc import MsfRpcClient

# Initialize MCP Server
mcp = FastMCP("Metasploit-Intelligence-Bridge")

# Metasploit Connection Details
MSF_PASS = os.getenv("MSF_PASSWORD", "msf")
MSF_HOST = os.getenv("MSF_HOST", "127.0.0.1")
MSF_PORT = int(os.getenv("MSF_PORT", 55553))

def get_msf_client():
    try:
        return MsfRpcClient(MSF_PASS, host=MSF_HOST, port=MSF_PORT, ssl=True)
    except Exception as e:
        print(f"Error connecting to msfrpcd: {e}")
        return None

@mcp.tool()
def search_modules(query: str):
    """Search for Metasploit modules by keyword or CVE."""
    client = get_msf_client()
    if not client: return "Connection Failed"
    return client.modules.search(query)

@mcp.tool()
def run_exploit(module_type: str, module_name: str, options: dict):
    """Execute a Metasploit module with given options."""
    client = get_msf_client()
    if not client: return "Connection Failed"
    exploit = client.modules.use(module_type, module_name)
    for key, value in options.items():
        exploit[key] = value
    return exploit.execute()

@mcp.tool()
def list_sessions():
    """List all active Meterpreter sessions."""
    client = get_msf_client()
    if not client: return "Connection Failed"
    return client.sessions.list

if __name__ == "__main__":
    mcp.run()
