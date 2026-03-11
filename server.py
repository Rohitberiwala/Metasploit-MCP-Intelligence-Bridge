import os
import sys
import time
import logging
from typing import Dict, List, Optional, Union
from mcp.server.fastmcp import FastMCP
from pymetasploit3.msfrpc import MsfRpcClient
from pymetasploit3.utils import MsfRpcError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metasploit_bridge.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('metasploit_bridge')

# Initialize MCP Server
mcp = FastMCP("Metasploit-Intelligence-Bridge")

# Metasploit Connection Details
MSF_PASS = os.getenv("MSF_PASSWORD", "msf")
MSF_HOST = os.getenv("MSF_HOST", "127.0.0.1")
MSF_PORT = int(os.getenv("MSF_PORT", 55553))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 5))

class MetasploitManager:
    def __init__(self):
        self.client = None
        self.connect_attempts = 0
        
    def get_msf_client(self) -> Optional[MsfRpcClient]:
        """Establish connection to Metasploit RPC server with retry logic."""
        if self.client:
            try:
                # Verify connection is still valid
                self.client.modules.search("")
                return self.client
            except (MsfRpcError, Exception) as e:
                logger.warning(f"Existing connection failed: {e}")
                self.client = None
                
        # Attempt new connection
        for attempt in range(RETRY_COUNT):
            try:
                logger.info(f"Attempting to connect (attempt {attempt+1}/{RETRY_COUNT})")
                self.client = MsfRpcClient(
                    MSF_PASS,
                    host=MSF_HOST,
                    port=MSF_PORT,
                    ssl=True
                )
                self.connect_attempts = 0
                return self.client
            except Exception as e:
                logger.error(f"Connection attempt {attempt+1} failed: {e}")
                if attempt < RETRY_COUNT - 1:
                    time.sleep(RETRY_DELAY)
                    
        self.connect_attempts += 1
        if self.connect_attempts >= RETRY_COUNT:
            logger.critical("Max connection attempts exceeded")
            
        return None

# Global manager instance
msf_manager = MetasploitManager()

@mcp.tool()
def search_modules(query: str) -> Union[str, List[Dict]]:
    """Search for Metasploit modules by keyword or CVE."""
    client = msf_manager.get_msf_client()
    if not client:
        return "Connection Failed"
        
    try:
        modules = client.modules.search(query)
        logger.info(f"Found {len(modules)} modules for query: {query}")
        return modules
    except Exception as e:
        logger.error(f"Module search failed: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
def run_exploit(module_type: str, module_name: str, options: Dict) -> Union[str, Dict]:
    """Execute a Metasploit module with given options."""
    client = msf_manager.get_msf_client()
    if not client:
        return "Connection Failed"
        
    try:
        logger.info(f"Running {module_type}/{module_name} with options: {options}")
        exploit = client.modules.use(module_type, module_name)
        
        # Set options safely
        for key, value in options.items():
            try:
                exploit[key] = value
            except Exception as e:
                logger.warning(f"Failed to set option {key}: {e}")
                
        result = exploit.execute()
        logger.info(f"Exploit completed with result: {result}")
        return result
    except Exception as e:
        logger.error(f"Exploit execution failed: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
def list_sessions() -> Union[str, Dict]:
    """List all active Meterpreter sessions."""
    client = msf_manager.get_msf_client()
    if not client:
        return "Connection Failed"
        
    try:
        sessions = client.sessions.list
        logger.info(f"Found {len(sessions)} active sessions")
        return sessions
    except Exception as e:
        logger.error(f"Session listing failed: {e}")
        return f"Error: {str(e)}"

@mcp.tool()
def kill_session(session_id: int) -> Union[str, bool]:
    """Kill a specific Meterpreter session."""
    client = msf_manager.get_msf_client()
    if not client:
        return "Connection Failed"
        
    try:
        logger.info(f"Killing session {session_id}")
        result = client.sessions.session(session_id).kill()
        logger.info(f"Session {session_id} killed successfully")
        return result
    except Exception as e:
        logger.error(f"Session termination failed: {e}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting Metasploit-MCP-Intelligence-Bridge")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
    finally:
        logger.info("Bridge shutting down")
