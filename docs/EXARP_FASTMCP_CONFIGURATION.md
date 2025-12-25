# Exarp FastMCP Configuration


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on NumPy, Pandas, Pydantic, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use NumPy patterns? use context7"
> - "Show me NumPy examples examples use context7"
> - "NumPy best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date**: 2025-11-26
**FastMCP Version**: 2.12.0+
**Reference**: [FastMCP Server Configuration](https://gofastmcp.com/deployment/server-configuration)

---

## Overview

Exarp uses FastMCP's declarative configuration system via `fastmcp.json` files. This provides a portable, shareable way to configure the server without complex command-line arguments.

**Benefits**:
- ✅ Single source of truth for server configuration
- ✅ Portable across environments
- ✅ Easy to share with team members
- ✅ IDE autocomplete and validation (with JSON schema)
- ✅ CLI argument overrides for flexibility

---

## Configuration Files

### 1. `fastmcp.json` (Default/Production)

**Purpose**: Standard configuration for production use

**Configuration**:
```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "type": "filesystem",
    "path": "exarp_project_management/server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.9",
    "project": "."
  },
  "deployment": {
    "transport": "stdio",
    "log_level": "INFO"
  }
}
```

**Usage**:
```bash
fastmcp run                    # Automatically finds fastmcp.json
fastmcp run fastmcp.json      # Explicit file path
```

**Settings**:
- **Transport**: stdio (default for local use)
- **Log Level**: INFO
- **Python**: >=3.9 (matches pyproject.toml)
- **Dependencies**: Managed via `pyproject.toml` (uv project)

---

### 2. `fastmcp.dev.json` (Development)

**Purpose**: Development configuration with debugging enabled

**Configuration**:
```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "type": "filesystem",
    "path": "exarp_project_management/server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.10",
    "project": ".",
    "dependencies": ["fastmcp[dev]"]
  },
  "deployment": {
    "transport": "stdio",
    "log_level": "DEBUG",
    "env": {
      "DEBUG": "true",
      "ENV": "development"
    }
  }
}
```

**Usage**:
```bash
fastmcp run fastmcp.dev.json
fastmcp dev fastmcp.dev.json  # Launch with Inspector UI
```

**Settings**:
- **Transport**: stdio
- **Log Level**: DEBUG (verbose logging)
- **Python**: >=3.10 (newer version for development)
- **Dependencies**: Includes `fastmcp[dev]` for development tools
- **Editable**: `.` (installs package in editable mode for development)
- **Environment**: DEBUG=true, ENV=development

---

### 3. `fastmcp.http.json` (HTTP Transport)

**Purpose**: HTTP transport configuration for network-based deployment

**Configuration**:
```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  "source": {
    "type": "filesystem",
    "path": "exarp_project_management/server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.9",
    "project": "."
  },
  "deployment": {
    "transport": "http",
    "host": "127.0.0.1",
    "port": 8000,
    "log_level": "INFO",
    "env": {
      "ENV": "production"
    }
  }
}
```

**Usage**:
```bash
fastmcp run fastmcp.http.json
# Server accessible at http://127.0.0.1:8000/mcp
```

**Settings**:
- **Transport**: http (Streamable HTTP)
- **Host**: 127.0.0.1 (localhost)
- **Port**: 8000
- **Log Level**: INFO
- **Environment**: ENV=production

**Note**: HTTP transport requires authentication and security configuration (see deployment tasks).

---

## Configuration Structure

### Source Configuration (Required)

**Purpose**: WHERE does your server code live?

```json
"source": {
  "type": "filesystem",           // Source type (filesystem, git, cloud)
  "path": "exarp_project_management/server.py",  // Path to server file
  "entrypoint": "mcp"              // FastMCP instance name
}
```

**Entrypoint**: FastMCP searches for `mcp`, `server`, or `app` if not specified. Exarp uses `mcp` as the instance name.

### Environment Configuration (Optional)

**Purpose**: WHAT environment setup does it require?

```json
"environment": {
  "type": "uv",                    // Environment type (uv, venv, conda)
  "python": ">=3.9",               // Python version constraint
  "project": "."                   // Path to project directory (pyproject.toml)
}
```

**Dependencies**: Managed via `pyproject.toml` when using `"project": "."`. FastMCP uses `uv` to resolve dependencies automatically.

### Deployment Configuration (Optional)

**Purpose**: HOW should the server run?

```json
"deployment": {
  "transport": "stdio",            // Transport: stdio, http, sse
  "log_level": "INFO",             // Log level: DEBUG, INFO, WARNING, ERROR
  "env": {                         // Environment variables
    "ENV": "production"
  }
}
```

**Transport Options**:
- `stdio`: Standard input/output (default, local use)
- `http`: Streamable HTTP (network deployment)
- `sse`: Server-Sent Events (legacy, not recommended)

---

## Usage Examples

### Basic Usage

```bash
# Run with default configuration (fastmcp.json)
fastmcp run

# Run with explicit configuration file
fastmcp run fastmcp.json

# Run with development configuration
fastmcp run fastmcp.dev.json

# Run with HTTP transport
fastmcp run fastmcp.http.json
```

### Development with Inspector

```bash
# Launch development server with Inspector UI
fastmcp dev fastmcp.dev.json

# Inspector available at http://localhost:5173
```

### CLI Overrides

```bash
# Override port in HTTP configuration
fastmcp run fastmcp.http.json --port 9000

# Override log level
fastmcp run fastmcp.json --log-level DEBUG

# Override transport
fastmcp run fastmcp.json --transport http

# Add extra dependencies
fastmcp run fastmcp.json --with pandas --with numpy
```

### Inspect Server

```bash
# View server capabilities and configuration
fastmcp inspect fastmcp.json

# Inspect with specific entrypoint
fastmcp inspect exarp_project_management/server.py:mcp
```

### Install to MCP Clients

```bash
# Install to Claude Desktop
fastmcp install fastmcp.json --client claude-desktop

# Install to Cursor
fastmcp install fastmcp.json --client cursor
```

---

## Migration from Current Setup

### Current Setup (Before)

**Cursor Configuration** (`.cursor/mcp.json`):
```json
{
  "exarp": {
    "command": "python3",
    "args": ["-m", "exarp_project_management.server"],
    "description": "Exarp - Project management automation tools"
  }
}
```

**Manual Execution**:
```bash
python3 -m exarp_project_management.server
```

### New Setup (With fastmcp.json)

**Option 1: Keep Current Setup** (Backwards Compatible)
- Current `.cursor/mcp.json` continues to work
- `fastmcp.json` provides additional configuration options

**Option 2: Use FastMCP CLI** (Recommended for Development)
```bash
# Run with FastMCP CLI
fastmcp run fastmcp.json

# Or update .cursor/mcp.json to use FastMCP CLI
{
  "exarp": {
    "command": "fastmcp",
    "args": ["run", "fastmcp.json"],
    "description": "Exarp - Project management automation tools"
  }
}
```

**Option 3: Use FastMCP Install** (Automatic Configuration)
```bash
# Install to Cursor automatically
fastmcp install fastmcp.json --client cursor
```

---

## Benefits of fastmcp.json

### 1. Portability
- Single file contains all configuration
- Easy to share across team members
- Version control friendly

### 2. Reproducibility
- Same configuration works across environments
- No need to remember command-line arguments
- Consistent execution

### 3. IDE Support
- JSON schema provides autocomplete
- Validation catches errors early
- Inline documentation

### 4. Flexibility
- CLI arguments can override any setting
- Multiple configuration files for different environments
- Easy to switch between transports

### 5. Documentation
- Configuration file serves as documentation
- Clear structure (source, environment, deployment)
- Self-documenting settings

---

## Configuration Best Practices

### 1. Use JSON Schema
Always include the schema reference for IDE support:
```json
{
  "$schema": "https://gofastmcp.com/public/schemas/fastmcp.json/v1.json",
  ...
}
```

### 2. Specify Entrypoint
Explicitly specify the entrypoint for clarity:
```json
"source": {
  "path": "exarp_project_management/server.py",
  "entrypoint": "mcp"
}
```

### 3. Use Project Directory
For Python projects with `pyproject.toml`, use project directory:
```json
"environment": {
  "project": "."
}
```

### 4. Environment-Specific Files
Create separate files for different environments:
- `fastmcp.json` - Production/default
- `fastmcp.dev.json` - Development
- `fastmcp.http.json` - HTTP transport
- `fastmcp.test.json` - Testing

### 5. Version Constraints
Specify Python version constraints:
```json
"environment": {
  "python": ">=3.9"  // Matches pyproject.toml
}
```

---

## Troubleshooting

### Server Not Found

**Error**: `Server instance 'mcp' not found`

**Solution**: Verify the entrypoint name matches your FastMCP instance:
```python
# In server.py
mcp = FastMCP("exarp")  # Must match entrypoint in fastmcp.json
```

### Dependencies Not Resolved

**Error**: `ModuleNotFoundError`

**Solution**: Ensure `pyproject.toml` has all dependencies, or use explicit dependencies:
```json
"environment": {
  "dependencies": ["fastmcp>=2.0.0", "pydantic>=2.0.0"]
}
```

### Transport Issues

**Error**: HTTP transport not working

**Solution**: Verify FastMCP version supports HTTP transport:
```bash
pip install "fastmcp>=2.12.0"
```

---

## Related Documentation

- [FastMCP Server Configuration](https://gofastmcp.com/deployment/server-configuration)
- [Exarp Deployment Options](EXARP_DEPLOYMENT_OPTIONS.md)
- [Exarp Transport Analysis](EXARP_MCP_TRANSPORT_ANALYSIS.md)
- [FastMCP CLI Documentation](https://gofastmcp.com/deployment/running-server#the-fastmcp-cli)

---

## Future Enhancements

**Planned FastMCP Features** (from documentation):
- Git repository sources (`type: "git"`)
- FastMCP Cloud sources (`type: "cloud"`)
- Additional environment types (venv, conda)

**Exarp Integration**:
- Update configuration when new features are available
- Add production deployment configuration
- Integrate with CI/CD pipelines

---

P25-12-25
