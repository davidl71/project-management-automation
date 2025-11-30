import * as vscode from 'vscode';
import { Todo2Watcher } from './todo2/watcher';
import { StatusBarProvider } from './providers/statusBar';
import { TestTreeViewProvider } from './providers/testTreeView';

let todo2Watcher: Todo2Watcher | undefined;
let statusBarProvider: StatusBarProvider | undefined;
let testTreeViewProvider: TestTreeViewProvider | undefined;

/**
 * Activate extension
 */
export function activate(context: vscode.ExtensionContext) {
  console.log('Exarp extension is now active!');

  // Get workspace folder
  const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
  if (!workspaceFolder) {
    vscode.window.showWarningMessage(
      'Exarp requires a workspace folder. Please open a folder first.'
    );
    return;
  }

  // Initialize Todo2 watcher
  todo2Watcher = new Todo2Watcher(workspaceFolder);
  context.subscriptions.push(todo2Watcher);

  // Initialize status bar provider
  statusBarProvider = new StatusBarProvider(context, todo2Watcher);
  context.subscriptions.push(statusBarProvider);

  // Initialize test tree view provider
  testTreeViewProvider = new TestTreeViewProvider(workspaceFolder);
  const testTreeView = vscode.window.createTreeView('exarp.tests', {
    treeDataProvider: testTreeViewProvider,
    showCollapseAll: true
  });
  context.subscriptions.push(testTreeView);

  // Register commands
  registerCommands(context, workspaceFolder, testTreeViewProvider);

  // Show activation message
  vscode.window.showInformationMessage('Exarp extension activated!');
}

/**
 * Register all commands
 */
function registerCommands(
  context: vscode.ExtensionContext,
  workspaceFolder: vscode.WorkspaceFolder,
  testTreeProvider: TestTreeViewProvider
) {
  // Show tasks command
  const showTasksCmd = vscode.commands.registerCommand(
    'exarp.showTasks',
    async () => {
      if (!todo2Watcher) {
        vscode.window.showErrorMessage('Todo2 watcher not initialized');
        return;
      }

      const tasks = todo2Watcher.getTasks();
      
      if (tasks.length === 0) {
        vscode.window.showInformationMessage('No tasks found in Todo2');
        return;
      }

      // Group tasks by status
      const byStatus: { [key: string]: typeof tasks } = {};
      tasks.forEach(task => {
        const status = task.status || 'Unknown';
        if (!byStatus[status]) {
          byStatus[status] = [];
        }
        byStatus[status].push(task);
      });

      // Show quick pick with task count by status
      const statusItems = Object.entries(byStatus).map(([status, taskList]) => ({
        label: `${status} (${taskList.length})`,
        description: `${taskList.length} tasks`,
        detail: taskList.slice(0, 3).map(t => 
          t.name || t.content || t.id
        ).join(', '),
        status
      }));

      const selected = await vscode.window.showQuickPick(statusItems, {
        placeHolder: 'Select status to view tasks...'
      });

      if (selected) {
        const tasksInStatus = byStatus[selected.status];
        const taskItems = tasksInStatus.map(task => ({
          label: task.name || task.content || task.id,
          description: task.priority ? `[${task.priority}]` : undefined,
          detail: task.id,
          task
        }));

        const taskSelected = await vscode.window.showQuickPick(taskItems, {
          placeHolder: `Tasks in ${selected.status}...`
        });

        if (taskSelected) {
          // Show task details
          const task = taskSelected.task;
          const details = [
            `**Task ID:** ${task.id}`,
            `**Name:** ${task.name || 'Unnamed'}`,
            `**Status:** ${task.status || 'Unknown'}`,
            `**Priority:** ${task.priority || 'Not set'}`,
            task.content ? `**Content:**\n${task.content}` : '',
            task.tags ? `**Tags:** ${task.tags.join(', ')}` : ''
          ].filter(Boolean).join('\n\n');

          vscode.window.showInformationMessage(details, { modal: true });
        }
      }
    }
  );

  // Refresh tasks command
  const refreshTasksCmd = vscode.commands.registerCommand(
    'exarp.refreshTasks',
    async () => {
      if (!todo2Watcher) {
        vscode.window.showErrorMessage('Todo2 watcher not initialized');
        return;
      }

      statusBarProvider?.setRunning('Refreshing tasks...');
      await todo2Watcher.refresh();
      statusBarProvider?.setSuccess('Tasks refreshed');
      
      setTimeout(() => {
        statusBarProvider?.setIdle();
      }, 2000);
    }
  );

  // Create task command (placeholder)
  const createTaskCmd = vscode.commands.registerCommand(
    'exarp.createTask',
    async () => {
      vscode.window.showInformationMessage(
        'Create task feature coming soon!'
      );
    }
  );

  // Project scorecard command
  const projectScorecardCmd = vscode.commands.registerCommand(
    'exarp.projectScorecard',
    async () => {
      const currentWorkspaceFolder = vscode.workspace.workspaceFolders?.[0];
      if (!currentWorkspaceFolder) {
        vscode.window.showErrorMessage('No workspace folder found');
        return;
      }

      const output = vscode.window.createOutputChannel('Project Scorecard');
      output.show();
      output.appendLine('Generating project scorecard...');
      
      statusBarProvider?.setRunning('Generating scorecard...');

      try {
        const { MCPClient } = await import('./utils/mcpClient');
        const client = new MCPClient(currentWorkspaceFolder);
        
        const result = await client.getProjectScorecard('json', true);
        
        if (result.success && result.data) {
          const scorecard = result.data;
          const overallScore = scorecard.overall_score || 0;
          const productionReady = scorecard.production_ready ? '✅ Yes' : '❌ No';
          
          output.appendLine('✅ Project Scorecard Generated');
          output.appendLine('═'.repeat(60));
          output.appendLine(`Overall Score: ${overallScore.toFixed(1)}%`);
          output.appendLine(`Production Ready: ${productionReady}`);
          output.appendLine('');
          
          // Display component scores
          if (scorecard.scores) {
            output.appendLine('Component Scores:');
            Object.entries(scorecard.scores).forEach(([component, score]: [string, any]) => {
              const bar = '█'.repeat(Math.round(score / 5));
              output.appendLine(`  ${component.padEnd(20)}: ${score.toFixed(1)}% ${bar}`);
            });
          }
          
          // Display blockers
          if (scorecard.blockers && scorecard.blockers.length > 0) {
            output.appendLine('');
            output.appendLine('Blockers:');
            scorecard.blockers.forEach((blocker: string) => {
              output.appendLine(`  ❌ ${blocker}`);
            });
          }
          
          // Display recommendations
          if (scorecard.recommendations && scorecard.recommendations.length > 0) {
            output.appendLine('');
            output.appendLine('Recommendations:');
            scorecard.recommendations.forEach((rec: any) => {
              output.appendLine(`  ${rec.priority === 'high' ? '🔴' : rec.priority === 'medium' ? '🟡' : '🟢'} [${rec.priority}] ${rec.area}: ${rec.action}`);
              if (rec.impact) {
                output.appendLine(`      Impact: ${rec.impact}`);
              }
            });
          }
          
          statusBarProvider?.setSuccess(`Score: ${overallScore.toFixed(1)}%`);
          vscode.window.showInformationMessage(
            `Project scorecard: ${overallScore.toFixed(1)}% (${productionReady})`
          );
        } else {
          output.appendLine(`❌ Error: ${result.error || 'Unknown error'}`);
          statusBarProvider?.setError('Scorecard failed');
          vscode.window.showErrorMessage(
            `Project scorecard failed: ${result.error || 'Unknown error'}`
          );
        }
      } catch (error: any) {
        output.appendLine(`❌ Error: ${error.message}`);
        statusBarProvider?.setError('Scorecard error');
        vscode.window.showErrorMessage(`Error: ${error.message}`);
      } finally {
        setTimeout(() => {
          statusBarProvider?.setIdle();
        }, 3000);
      }
    }
  );

  // Test commands
  const runAllTestsCmd = vscode.commands.registerCommand(
    'exarp.tests.runAll',
    async () => {
      const output = vscode.window.createOutputChannel('Exarp Tests');
      output.show();
      output.appendLine('Running all tests...');
      
      try {
        const { exec } = require('child_process');
        const util = require('util');
        const execAsync = util.promisify(exec);
        
        const testCommand = 'npm run test';
        const { stdout, stderr } = await execAsync(testCommand, {
          cwd: workspaceFolder.uri.fsPath,
          maxBuffer: 10 * 1024 * 1024
        });
        
        output.appendLine(stdout);
        if (stderr) {
          output.appendLine(`\n--- Errors ---\n${stderr}`);
        }
        
        vscode.window.showInformationMessage('Tests completed. Check output channel for results.');
      } catch (error: any) {
        output.appendLine(`Error: ${error.message}`);
        vscode.window.showErrorMessage(`Test execution failed: ${error.message}`);
      }
    }
  );

  const runTestFileCmd = vscode.commands.registerCommand(
    'exarp.tests.runFile',
    async (item: any) => {
      if (!item || !item.testFile) {
        vscode.window.showErrorMessage('No test file selected');
        return;
      }

      const output = vscode.window.createOutputChannel('Exarp Tests');
      output.show();
      output.appendLine(`Running test file: ${item.testFile}...`);
      
      vscode.window.showInformationMessage('Running individual test files requires test runner configuration.');
      output.appendLine('Note: Individual test file execution requires VS Code Test Runner.');
    }
  );

  const refreshTestsCmd = vscode.commands.registerCommand(
    'exarp.tests.refresh',
    () => {
      testTreeProvider.refresh();
      vscode.window.showInformationMessage('Tests refreshed');
    }
  );

  context.subscriptions.push(
    showTasksCmd,
    refreshTasksCmd,
    createTaskCmd,
    projectScorecardCmd,
    runAllTestsCmd,
    runTestFileCmd,
    refreshTestsCmd
  );
}

/**
 * Deactivate extension
 */
export function deactivate() {
  todo2Watcher?.dispose();
  statusBarProvider?.dispose();
  testTreeViewProvider?.refresh();
}

