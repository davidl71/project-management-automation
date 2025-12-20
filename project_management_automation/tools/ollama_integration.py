"""
Ollama Integration Tools

Provides tools for interacting with local Ollama models:
- List available models
- Generate text with Ollama
- Check Ollama server status
- Pull/download models
"""

import json
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

# Try to import ollama, handle gracefully if not available
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("Ollama package not available. Install with: uv sync")

# Import error handler
try:
    from ..error_handler import (
        ErrorCode,
        format_error_response,
        format_success_response,
        log_automation_execution,
    )
except ImportError:
    def format_success_response(data, message=None):
        return {"success": True, "data": data, "timestamp": time.time()}

    def format_error_response(error, error_code, include_traceback=False):
        return {"success": False, "error": {"code": str(error_code), "message": str(error)}}

    def log_automation_execution(name, duration, success, error=None):
        logger.info(f"{name}: {duration:.2f}s, success={success}")

    class ErrorCode:
        AUTOMATION_ERROR = "AUTOMATION_ERROR"


def check_ollama_status(host: Optional[str] = None) -> str:
    """
    [HINT: Ollama status. Check if Ollama server is running and accessible.]

    📊 Output: Server status, version, available models count
    🔧 Side Effects: None (read-only check)
    📁 Checks: Ollama server connection
    ⏱️ Typical Runtime: <1 second

    Example Prompt:
    "Is Ollama running? Check Ollama status"

    Args:
        host: Optional Ollama host URL (default: http://localhost:11434)

    Returns:
        JSON with Ollama server status
    """
    start_time = time.time()

    if not OLLAMA_AVAILABLE:
        error_response = format_error_response(
            "Ollama package not installed. Install with: uv sync",
            ErrorCode.AUTOMATION_ERROR
        )
        return json.dumps(error_response, indent=2)

    try:
        # Configure client if host provided
        if host:
            client = ollama.Client(host=host)
        else:
            client = ollama.Client()

        # Try to list models to check connection
        models = client.list()
        
        result = {
            "status": "running",
            "host": host or "http://localhost:11434",
            "model_count": len(models.get("models", [])),
            "models": [m.get("name", "") for m in models.get("models", [])[:10]],  # First 10
        }

        duration = time.time() - start_time
        log_automation_execution("check_ollama_status", duration, True)

        return json.dumps(format_success_response(result), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution("check_ollama_status", duration, False, e)
        
        # Check if it's a connection error
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower():
            error_msg = "Ollama server not running. Start it with: ollama serve"
        
        error_response = format_error_response(error_msg, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)


def list_ollama_models(host: Optional[str] = None) -> str:
    """
    [HINT: Ollama models. List all available Ollama models on the local server.]

    📊 Output: List of models with details (name, size, modified date)
    🔧 Side Effects: None (read-only)
    📁 Queries: Ollama server
    ⏱️ Typical Runtime: <1 second

    Example Prompt:
    "What Ollama models do I have installed?"

    Args:
        host: Optional Ollama host URL (default: http://localhost:11434)

    Returns:
        JSON with list of available models
    """
    start_time = time.time()

    if not OLLAMA_AVAILABLE:
        error_response = format_error_response(
            "Ollama package not installed. Install with: uv sync",
            ErrorCode.AUTOMATION_ERROR
        )
        return json.dumps(error_response, indent=2)

    try:
        # Configure client if host provided
        if host:
            client = ollama.Client(host=host)
        else:
            client = ollama.Client()

        models = client.list()
        model_list = models.get("models", [])

        # Format model information
        formatted_models = []
        for model in model_list:
            formatted_models.append({
                "name": model.get("name", ""),
                "size": model.get("size", 0),
                "modified_at": model.get("modified_at", ""),
                "digest": model.get("digest", "")[:12],  # Short digest
            })

        result = {
            "models": formatted_models,
            "count": len(formatted_models),
            "tip": "Use generate_with_ollama to generate text with a model",
        }

        duration = time.time() - start_time
        log_automation_execution("list_ollama_models", duration, True)

        return json.dumps(format_success_response(result), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution("list_ollama_models", duration, False, e)
        
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower():
            error_msg = "Ollama server not running. Start it with: ollama serve"
        
        error_response = format_error_response(error_msg, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)


def generate_with_ollama(
    prompt: str,
    model: str = "llama3.2",
    host: Optional[str] = None,
    stream: bool = False,
    options: Optional[dict] = None,
) -> str:
    """
    [HINT: Ollama generation. Generate text using a local Ollama model.]

    📊 Output: Generated text response
    🔧 Side Effects: Calls Ollama API (may use GPU/CPU resources)
    📁 Uses: Local Ollama server
    ⏱️ Typical Runtime: 1-30 seconds (depends on model and prompt length)

    Example Prompt:
    "Generate a summary using Ollama llama3.2 model"

    Args:
        prompt: Text prompt to send to the model
        model: Model name (default: llama3.2)
        host: Optional Ollama host URL (default: http://localhost:11434)
        stream: Whether to stream the response (default: False)
        options: Optional model parameters (temperature, top_p, etc.)

    Returns:
        JSON with generated text
    """
    start_time = time.time()

    if not OLLAMA_AVAILABLE:
        error_response = format_error_response(
            "Ollama package not installed. Install with: uv sync",
            ErrorCode.AUTOMATION_ERROR
        )
        return json.dumps(error_response, indent=2)

    try:
        # Configure client if host provided
        if host:
            client = ollama.Client(host=host)
        else:
            client = ollama.Client()

        # Prepare generation parameters
        gen_options = options or {}

        # Generate response
        if stream:
            # Stream response
            response_text = ""
            for chunk in client.generate(model=model, prompt=prompt, stream=True, options=gen_options):
                if "response" in chunk:
                    response_text += chunk["response"]
        else:
            # Single response
            response = client.generate(model=model, prompt=prompt, stream=False, options=gen_options)
            response_text = response.get("response", "")

        result = {
            "model": model,
            "prompt": prompt[:200] + "..." if len(prompt) > 200 else prompt,  # Truncate for display
            "response": response_text,
            "length": len(response_text),
        }

        duration = time.time() - start_time
        log_automation_execution("generate_with_ollama", duration, True)

        return json.dumps(format_success_response(result), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution("generate_with_ollama", duration, False, e)
        
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower():
            error_msg = "Ollama server not running. Start it with: ollama serve"
        elif "model" in error_msg.lower() and "not found" in error_msg.lower():
            error_msg = f"Model '{model}' not found. Pull it with: ollama pull {model}"
        
        error_response = format_error_response(error_msg, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)


def pull_ollama_model(model: str, host: Optional[str] = None) -> str:
    """
    [HINT: Ollama pull. Download/pull an Ollama model from the registry.]

    📊 Output: Pull status and progress
    🔧 Side Effects: Downloads model (may take time and disk space)
    📁 Downloads: Model from Ollama registry
    ⏱️ Typical Runtime: 30 seconds - 10 minutes (depends on model size)

    Example Prompt:
    "Pull the llama3.2 model from Ollama"

    Args:
        model: Model name to pull (e.g., "llama3.2", "mistral", "codellama")
        host: Optional Ollama host URL (default: http://localhost:11434)

    Returns:
        JSON with pull status
    """
    start_time = time.time()

    if not OLLAMA_AVAILABLE:
        error_response = format_error_response(
            "Ollama package not installed. Install with: uv sync",
            ErrorCode.AUTOMATION_ERROR
        )
        return json.dumps(error_response, indent=2)

    try:
        # Configure client if host provided
        if host:
            client = ollama.Client(host=host)
        else:
            client = ollama.Client()

        # Pull model (this may take a while)
        logger.info(f"Pulling model: {model} (this may take several minutes)")
        response = client.pull(model)

        result = {
            "model": model,
            "status": "completed",
            "message": f"Model {model} pulled successfully",
        }

        duration = time.time() - start_time
        log_automation_execution("pull_ollama_model", duration, True)

        return json.dumps(format_success_response(result), indent=2)

    except Exception as e:
        duration = time.time() - start_time
        log_automation_execution("pull_ollama_model", duration, False, e)
        
        error_msg = str(e)
        if "connection" in error_msg.lower() or "refused" in error_msg.lower():
            error_msg = "Ollama server not running. Start it with: ollama serve"
        
        error_response = format_error_response(error_msg, ErrorCode.AUTOMATION_ERROR)
        return json.dumps(error_response, indent=2)


def register_ollama_tools(mcp):
    """
    Register Ollama tools with FastMCP server.
    
    Args:
        mcp: FastMCP server instance
    """
    if not OLLAMA_AVAILABLE:
        logger.warning("Ollama tools not registered: ollama package not available")
        return

    try:
        from fastmcp import pydantic

        @mcp.tool()
        def check_ollama_status_tool(host: Optional[str] = None) -> str:
            """Check if Ollama server is running and accessible."""
            return check_ollama_status(host)

        @mcp.tool()
        def list_ollama_models_tool(host: Optional[str] = None) -> str:
            """List all available Ollama models on the local server."""
            return list_ollama_models(host)

        @mcp.tool()
        def generate_with_ollama_tool(
            prompt: str,
            model: str = "llama3.2",
            host: Optional[str] = None,
            stream: bool = False,
            options: Optional[str] = None,  # JSON string
        ) -> str:
            """
            Generate text using a local Ollama model.
            
            Args:
                prompt: Text prompt to send to the model
                model: Model name (default: llama3.2)
                host: Optional Ollama host URL
                stream: Whether to stream the response
                options: Optional JSON string with model parameters (temperature, top_p, etc.)
            """
            # Parse options if provided
            parsed_options = None
            if options:
                try:
                    parsed_options = json.loads(options)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid options JSON: {options}")
            
            return generate_with_ollama(prompt, model, host, stream, parsed_options)

        @mcp.tool()
        def pull_ollama_model_tool(model: str, host: Optional[str] = None) -> str:
            """Download/pull an Ollama model from the registry."""
            return pull_ollama_model(model, host)

        logger.info("✅ Ollama tools registered")

    except Exception as e:
        logger.error(f"Failed to register Ollama tools: {e}", exc_info=True)

