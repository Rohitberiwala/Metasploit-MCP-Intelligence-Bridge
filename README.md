# 🛡️ Metasploit-MCP: The Ultimate AI-to-Exploit Bridge

![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Security](https://img.shields.io/badge/Security-Offensive-red)
![Protocol](https://img.shields.io/badge/Protocol-MCP-green)
![Author](https://img.shields.io/badge/Author-Vikings-black)

## 📌 Overview
**Metasploit-MCP** is a cutting-edge server implementation of the **Model Context Protocol (MCP)**. It creates a seamless communication channel between **AI Agents** (like Claude Code, Deep AI, or GPT-4) and the **Metasploit Framework**. 

With this bridge, your AI agent can browse exploits, generate payloads, and manage active sessions autonomously in a controlled environment.



---

## 🔥 Key Features
* **AI-Powered Module Search**: Use natural language to find CVEs and exploits.
* **Autonomous Exploitation**: Run auxiliary and exploit modules via AI commands.
* **Real-time Session Management**: AI can list, interact with, and close Meterpreter sessions.
* **Payload Automation**: Generate ELF, EXE, and Raw payloads on-the-fly.
* **Safe Mode**: Strict regex validation for module names and sanitized inputs.

---

## 🏗️ Architecture: How it Works
1. **AI Agent**: You give a command to your AI (e.g., "Find an exploit for SMB").
2. **MCP Server**: This server translates the AI's intent into Metasploit RPC commands.
3. **Metasploit RPC (msfrpcd)**: Executes the actual security task on the target system.
4. **Feedback Loop**: The results are fed back to the AI for analysis and next-step planning.



---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have the following installed:
* **Metasploit Framework**
* **Python 3.10+**
* **uv** (Fast Python package manager)

### 2. Start the Metasploit RPC Daemon
The MCP server needs to talk to Metasploit. Start the RPC server:
```bash
msfrpcd -P msf -S -a 127.0.0.1


git clone [https://github.com/Rohitberiwala/Metasploit-MCP-Intelligence-Bridge.git](https://github.com/Rohitberiwala/Metasploit-MCP-Intelligence-Bridge.git)
cd Metasploit-MCP-Intelligence-Bridge
MSF_PASSWORD=msf uv run server.py

📖 Usage ExamplesOnce connected, you can talk to your AI like a Senior Pentester:TaskPrompt ExampleSearch"Search for modules related to MS17-010 and show me the info for the exploit."Payload"Generate a Linux x64 reverse_tcp payload and save it."Exploit"Run the check for the eternalblue module against 192.168.1.10."Sessions"List all active sessions and tell me the sysinfo of session 1."🛠️ Configuration OptionsEnvironment VariableDefaultDescriptionMSF_PASSWORDmsfPassword for msfrpcd authentication.MSF_SERVER127.0.0.1Host address of your Metasploit RPC server.MCP_TRANSPORTstdioTransport mode (stdio or sse).⚠️ Security DisclaimerThis tool is for educational purposes and authorized security auditing only. Unauthorized access to computer systems is illegal. Always obtain permission before testing.
