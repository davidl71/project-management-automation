#!/usr/bin/env python3
"""
Automated script to pull CodeLlama for Exarp PMA
Uses uv for package management (project standard)
"""

import subprocess
import sys
import time
import os
from pathlib import Path

# Use uv run if available, otherwise fall back to direct execution
def get_python_cmd():
    """Get the appropriate Python command (uv run python or python3)."""
    # Check if uv is available
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return "uv run python"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "python3"

def run_command(cmd, check=True, capture_output=False):
    """Run a shell command."""
    try:
        if capture_output:
            result = subprocess.run(
                cmd, shell=True, check=check,
                capture_output=True, text=True
            )
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, check=check)
            return result.returncode == 0, "", ""
    except subprocess.CalledProcessError as e:
        return False, "", str(e)
    except Exception as e:
        return False, "", str(e)

def check_ollama_installed():
    """Check if Ollama CLI is installed."""
    success, _, _ = run_command("which ollama", capture_output=True)
    return success

def check_ollama_server():
    """Check if Ollama server is running."""
    success, _, _ = run_command("ollama list", capture_output=True, check=False)
    return success

def start_ollama_server():
    """Try to start Ollama server."""
    print("🔄 Attempting to start Ollama server...")
    
    # Try opening the app first (macOS)
    if Path("/Applications/Ollama.app").exists():
        print("   Opening Ollama app...")
        run_command("open -a Ollama", check=False)
        print("   ⏳ Waiting for server to start (10 seconds)...")
        time.sleep(10)
        return check_ollama_server()
    
    # Try starting via CLI
    print("   Starting Ollama server in background...")
    run_command("ollama serve", check=False)
    print("   ⏳ Waiting for server to start (5 seconds)...")
    time.sleep(5)
    return check_ollama_server()

def check_codellama_installed():
    """Check if CodeLlama is already installed."""
    success, output, _ = run_command("ollama list", capture_output=True, check=False)
    if success:
        return "codellama" in output.lower()
    return False

def pull_codellama():
    """Pull CodeLlama model."""
    print("📥 Pulling CodeLlama...")
    print("   ⏳ This will download ~3.8GB and may take several minutes...")
    print("   (Download speed depends on your internet connection)")
    print("")
    
    success, stdout, stderr = run_command("ollama pull codellama", capture_output=True, check=False)
    
    if success:
        return True
    else:
        print(f"❌ Error: {stderr}")
        return False

def main():
    print("🚀 Automated CodeLlama Setup for Exarp PMA")
    print("=" * 50)
    print("")
    
    # Check if uv is available (project standard)
    python_cmd = get_python_cmd()
    if python_cmd == "uv run python":
        print("✅ Using uv for Python execution (project standard)")
    else:
        print("⚠️  uv not found, using system Python")
    print("")
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        print("❌ Ollama CLI not found!")
        print("")
        print("Please install Ollama first:")
        print("  macOS: brew install ollama")
        print("  Or visit: https://ollama.ai/download")
        sys.exit(1)
    
    ollama_path = subprocess.run(
        "which ollama", shell=True, capture_output=True, text=True
    ).stdout.strip()
    print(f"✅ Ollama CLI found: {ollama_path}")
    print("")
    
    # Check if server is running
    if check_ollama_server():
        print("✅ Ollama server is already running")
    else:
        print("⚠️  Ollama server is not running")
        if start_ollama_server():
            print("✅ Ollama server started successfully")
        else:
            print("❌ Failed to start Ollama server")
            print("")
            print("Please start Ollama manually:")
            print("  1. Open the Ollama app from Applications")
            print("  2. Or run: ollama serve")
            print("")
            print("Then run this script again.")
            sys.exit(1)
    
    print("")
    
    # Check if CodeLlama is already installed
    if check_codellama_installed():
        print("✅ CodeLlama is already installed!")
        print("")
        print("📋 Installed models:")
        run_command("ollama list", check=False)
        print("")
        print("🎉 Ready to use! You can now use CodeLlama with Exarp PMA.")
        sys.exit(0)
    
    # Pull CodeLlama
    if pull_codellama():
        print("")
        print("✅ CodeLlama pulled successfully!")
        print("")
        print("📋 Installed models:")
        run_command("ollama list", check=False)
        print("")
        print("🎉 Setup complete! CodeLlama is ready to use with Exarp PMA.")
        print("")
        print("💡 Usage examples:")
        print("   - Generate code documentation")
        print("   - Analyze codebases")
        print("   - Code-related task management")
        print("")
        print("   Use via MCP tools: 'Generate text with Ollama using codellama'")
        print(f"   Or via uv: {python_cmd} -c \"from project_management_automation.tools.ollama_integration import generate_with_ollama; print(generate_with_ollama('Hello', 'codellama'))\"")
    else:
        print("")
        print("❌ Failed to pull CodeLlama")
        print("")
        print("Possible issues:")
        print("  - Network connection problem")
        print("  - Insufficient disk space")
        print("  - Ollama server issue")
        print("")
        print("Try manually: ollama pull codellama")
        sys.exit(1)

if __name__ == "__main__":
    main()

