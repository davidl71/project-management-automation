/**
 * Exarp Cursor Extension
 * 
 * Provides task management integration with Exarp MCP server.
 * Phase 1: Status bar and basic commands.
 */

import * as vscode from 'vscode';
import { Todo2StateReader } from './todo2Reader';
import { TaskCommands } from './commands';

let statusBarItem: vscode.StatusBarItem;
let todo2Reader: Todo2StateReader;
let taskCommands: TaskCommands;

export function activate(context: vscode.ExtensionContext) {
    console.log('Exarp extension is now active!');

    // Initialize components
    todo2Reader = new Todo2StateReader();
    taskCommands = new TaskCommands(todo2Reader);

    // Create status bar item
    statusBarItem = vscode.window.createStatusBarItem(
        vscode.StatusBarAlignment.Right,
        100
    );
    statusBarItem.command = 'exarp.listTasks';
    statusBarItem.show();

    // Update status bar on activation
    updateStatusBar();

    // Register commands
    const createTaskCmd = vscode.commands.registerCommand(
        'exarp.createTask',
        () => taskCommands.createTask()
    );
    
    const listTasksCmd = vscode.commands.registerCommand(
        'exarp.listTasks',
        () => taskCommands.listTasks()
    );
    
    const completeTaskCmd = vscode.commands.registerCommand(
        'exarp.completeTask',
        () => taskCommands.completeTask()
    );

    context.subscriptions.push(
        statusBarItem,
        createTaskCmd,
        listTasksCmd,
        completeTaskCmd
    );

    // Set up file watcher for Todo2 state changes
    const watcher = vscode.workspace.createFileSystemWatcher(
        '**/.todo2/state.todo2.json'
    );
    
    watcher.onDidChange(() => {
        updateStatusBar();
    });

    context.subscriptions.push(watcher);
}

function updateStatusBar() {
    try {
        const taskCount = todo2Reader.getPendingTaskCount();
        statusBarItem.text = `$(checklist) ${taskCount} tasks`;
        statusBarItem.tooltip = `Exarp: ${taskCount} pending tasks`;
    } catch (error) {
        statusBarItem.text = '$(checklist) Exarp';
        statusBarItem.tooltip = 'Exarp: Error reading tasks';
    }
}

export function deactivate() {
    // Cleanup
}
