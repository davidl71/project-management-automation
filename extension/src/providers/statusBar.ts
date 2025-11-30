import * as vscode from 'vscode';
import { Todo2Watcher, Todo2Task } from '../todo2/watcher';

/**
 * Status Bar Provider
 * 
 * Shows Exarp status in the status bar with:
 * - Current task count
 * - Active task info
 * - Quick actions
 */
export class StatusBarProvider {
  private statusBarItem: vscode.StatusBarItem;
  private taskCountItem?: vscode.StatusBarItem;
  private currentTaskItem?: vscode.StatusBarItem;

  constructor(
    private context: vscode.ExtensionContext,
    private todo2Watcher: Todo2Watcher
  ) {
    // Main status bar item
    this.statusBarItem = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Right,
      100
    );
    this.statusBarItem.command = 'exarp.showTasks';
    this.statusBarItem.tooltip = 'Exarp - Click to show tasks';
    this.statusBarItem.text = '$(tools) Exarp';
    this.statusBarItem.show();

    // Task count item (optional - shown when tasks exist)
    this.taskCountItem = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Right,
      99
    );
    this.taskCountItem.tooltip = 'Todo2 Task Count';
    this.taskCountItem.command = 'exarp.showTasks';

    // Current task item (optional - shown when task is active)
    this.currentTaskItem = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Right,
      98
    );
    this.currentTaskItem.tooltip = 'Current Task';

    // Listen for task changes
    this.todo2Watcher.onChanged((tasks) => {
      this.updateStatusBar(tasks);
    });

    // Initial update
    this.updateStatusBar(this.todo2Watcher.getTasks());

    context.subscriptions.push(
      this.statusBarItem,
      this.taskCountItem,
      this.currentTaskItem
    );
  }

  /**
   * Update status bar based on current tasks
   */
  private updateStatusBar(tasks: Todo2Task[]): void {
    const taskCount = tasks.length;
    const inProgress = tasks.filter(t => 
      t.status === 'In Progress' || t.status === 'in_progress'
    );
    const todo = tasks.filter(t => 
      t.status === 'Todo' || t.status === 'todo'
    );

    // Update main status bar
    if (taskCount === 0) {
      this.statusBarItem.text = '$(tools) Exarp';
      this.statusBarItem.tooltip = 'Exarp - No tasks found';
    } else {
      this.statusBarItem.text = `$(tools) Exarp`;
      this.statusBarItem.tooltip = `Exarp - ${taskCount} tasks (${todo.length} todo, ${inProgress.length} in progress)`;
    }

    // Update task count item
    if (taskCount > 0) {
      this.taskCountItem!.text = `$(list-unordered) ${taskCount} tasks`;
      this.taskCountItem!.show();
    } else {
      this.taskCountItem!.hide();
    }

    // Update current task item (show first in-progress task)
    const activeTask = inProgress[0];
    if (activeTask) {
      const taskName = activeTask.name || activeTask.content || 'Unnamed';
      const shortName = taskName.length > 30 
        ? taskName.substring(0, 27) + '...' 
        : taskName;
      this.currentTaskItem!.text = `$(sync~spin) ${shortName}`;
      this.currentTaskItem!.tooltip = `Current Task: ${taskName}`;
      this.currentTaskItem!.command = 'exarp.showTasks';
      this.currentTaskItem!.show();
    } else {
      this.currentTaskItem!.hide();
    }
  }

  /**
   * Update status for running operation
   */
  public setRunning(message?: string): void {
    this.statusBarItem.text = '$(sync~spin) Exarp';
    this.statusBarItem.backgroundColor = new vscode.ThemeColor(
      'statusBarItem.prominentForeground'
    );
    if (message) {
      this.statusBarItem.tooltip = `Exarp - ${message}`;
    }
  }

  /**
   * Update status for success
   */
  public setSuccess(message?: string): void {
    this.statusBarItem.text = '$(check) Exarp';
    this.statusBarItem.backgroundColor = undefined;
    if (message) {
      this.statusBarItem.tooltip = `Exarp - ${message}`;
    }
  }

  /**
   * Update status for error
   */
  public setError(message?: string): void {
    this.statusBarItem.text = '$(error) Exarp';
    this.statusBarItem.backgroundColor = new vscode.ThemeColor(
      'statusBarItem.errorBackground'
    );
    if (message) {
      this.statusBarItem.tooltip = `Exarp - Error: ${message}`;
    }
  }

  /**
   * Reset to idle state
   */
  public setIdle(): void {
    this.statusBarItem.text = '$(tools) Exarp';
    this.statusBarItem.backgroundColor = undefined;
    this.updateStatusBar(this.todo2Watcher.getTasks());
  }

  /**
   * Dispose
   */
  public dispose(): void {
    this.statusBarItem.dispose();
    this.taskCountItem?.dispose();
    this.currentTaskItem?.dispose();
  }
}

