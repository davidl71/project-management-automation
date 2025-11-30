import * as vscode from 'vscode';
import * as path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * MCP Tool Result
 */
export interface MCPToolResult {
  success: boolean;
  data?: any;
  error?: string;
  timestamp?: string;
}

/**
 * MCP Client for calling Python tools
 * 
 * This client directly calls Python functions instead of using MCP protocol
 * since the extension runs in the same workspace as the Python server.
 */
export class MCPClient {
  private projectRoot: string;
  private venvPython?: string;

  constructor(workspaceFolder: vscode.WorkspaceFolder) {
    this.projectRoot = workspaceFolder.uri.fsPath;
    
    // Try to find venv Python
    const venvPath = path.join(this.projectRoot, '.venv', 'bin', 'python3');
    const venvPythonPath = path.join(this.projectRoot, 'venv', 'bin', 'python3');
    
    // Check for venv - use try/catch since we can't easily check file existence synchronously
    // Will default to 'python3' if venv not found, which should work for most setups
    const fs = require('fs');
    if (fs.existsSync(venvPath)) {
      this.venvPython = venvPath;
    } else if (fs.existsSync(venvPythonPath)) {
      this.venvPython = venvPythonPath;
    }
  }

  /**
   * Call a Python tool function
   */
  async callTool(
    moduleName: string,
    functionName: string,
    args: Record<string, any> = {}
  ): Promise<MCPToolResult> {
    try {
      const pythonExec = this.venvPython || 'python3';
      
      // Build argument string
      const argString = Object.entries(args)
        .map(([k, v]) => {
          if (v === null || v === undefined) {
            return `${k}=None`;
          } else if (typeof v === 'boolean') {
            return `${k}=${v}`;
          } else if (typeof v === 'number') {
            return `${k}=${v}`;
          } else if (Array.isArray(v)) {
            return `${k}=${JSON.stringify(v)}`;
          } else {
            return `${k}=${JSON.stringify(v)}`;
          }
        })
        .join(', ');

      // Build Python script
      const pythonScript = `
import sys
import json
import os

# Add project root to path
sys.path.insert(0, '${this.projectRoot}')
os.chdir('${this.projectRoot}')

try:
    from project_management_automation.tools.${moduleName} import ${functionName}
    result = ${functionName}(${argString})
    
    # Handle both JSON strings and dicts
    if isinstance(result, str):
        result_data = json.loads(result)
    else:
        result_data = result
    
    print(json.dumps({
        "success": True,
        "data": result_data,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }))
except Exception as e:
    import traceback
    error_msg = str(e)
    traceback.print_exc()
    print(json.dumps({
        "success": False,
        "error": error_msg,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }))
    sys.exit(1)
`;

      // Execute Python script
      const { stdout, stderr } = await execAsync(
        `"${pythonExec}" -c ${JSON.stringify(pythonScript)}`,
        {
          cwd: this.projectRoot,
          maxBuffer: 10 * 1024 * 1024, // 10MB buffer
          env: { ...process.env, PYTHONPATH: this.projectRoot }
        }
      );

      if (stderr && !stderr.includes('INFO') && !stderr.includes('WARNING')) {
        console.error('[MCPClient] Error output:', stderr);
      }

      const result = JSON.parse(stdout.trim());
      return result;
    } catch (error: any) {
      console.error('[MCPClient] Error calling tool:', error);
      return {
        success: false,
        error: error.message || 'Unknown error',
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * Call project scorecard tool
   */
  async getProjectScorecard(
    outputFormat: string = 'json',
    includeRecommendations: boolean = true
  ): Promise<MCPToolResult> {
    return this.callTool(
      'project_scorecard',
      'generate_project_scorecard',
      {
        output_format: outputFormat,
        include_recommendations: includeRecommendations
      }
    );
  }
}

