import * as vscode from 'vscode';
import * as path from 'path';

/**
 * Todo2 Task interface
 */
export interface Todo2Task {
  id: string;
  name?: string;
  content?: string;
  status?: string;
  priority?: string;
  assignee?: {
    name?: string;
    hostname?: string;
  };
  tags?: string[];
  [key: string]: any;
}

/**
 * Todo2 State interface
 */
export interface Todo2State {
  todos: Todo2Task[];
  metadata?: {
    version?: string;
    lastModified?: string;
  };
  [key: string]: any;
}

/**
 * Todo2 File Watcher
 * 
 * Watches `.todo2/state.todo2.json` for changes and notifies listeners.
 * Handles missing files, large files, and rapid changes gracefully.
 */
export class Todo2Watcher {
  private watcher?: vscode.FileSystemWatcher;
  private state: Todo2State | null = null;
  private onTasksChanged: ((tasks: Todo2Task[]) => void)[] = [];
  private isLoading = false;
  private loadDebounceTimer?: NodeJS.Timeout;
  private readonly debounceDelay = 100; // ms

  constructor(private workspaceFolder: vscode.WorkspaceFolder) {
    this.initialize();
  }

  /**
   * Initialize watcher and load initial state
   */
  private async initialize(): Promise<void> {
    const todo2Path = new vscode.RelativePattern(
      this.workspaceFolder,
      '.todo2/state.todo2.json'
    );

    // Check if file exists
    try {
      const files = await vscode.workspace.findFiles(todo2Path, null, 1);
      if (files.length === 0) {
        console.warn('[Todo2Watcher] Todo2 file not found, watching for creation');
      }
    } catch (error) {
      console.error('[Todo2Watcher] Error checking for Todo2 file:', error);
    }

    // Create file watcher
    this.watcher = vscode.workspace.createFileSystemWatcher(todo2Path);

    // Load initial tasks
    await this.loadTasks();

    // Watch for changes (debounced to handle rapid writes)
    this.watcher.onDidChange(async (uri) => {
      console.log('[Todo2Watcher] File changed:', uri.fsPath);
      this.debouncedLoadTasks();
    });

    this.watcher.onDidCreate(async (uri) => {
      console.log('[Todo2Watcher] File created:', uri.fsPath);
      await this.loadTasks();
    });

    this.watcher.onDidDelete(() => {
      console.log('[Todo2Watcher] File deleted');
      this.state = null;
      this.notifyListeners();
    });
  }

  /**
   * Debounced task loading to handle rapid file changes
   */
  private debouncedLoadTasks(): void {
    if (this.loadDebounceTimer) {
      clearTimeout(this.loadDebounceTimer);
    }

    this.loadDebounceTimer = setTimeout(async () => {
      await this.loadTasks();
    }, this.debounceDelay);
  }

  /**
   * Load tasks from Todo2 file
   */
  private async loadTasks(): Promise<void> {
    // Prevent concurrent loads
    if (this.isLoading) {
      console.log('[Todo2Watcher] Already loading, skipping...');
      return;
    }

    this.isLoading = true;

    try {
      const todo2Path = path.join(
        this.workspaceFolder.uri.fsPath,
        '.todo2',
        'state.todo2.json'
      );

      const uri = vscode.Uri.file(todo2Path);

      // Check if file exists
      try {
        await vscode.workspace.fs.stat(uri);
      } catch (error) {
        // File doesn't exist
        this.state = null;
        this.notifyListeners();
        return;
      }

      // Read file
      const content = await vscode.workspace.fs.readFile(uri);
      const jsonString = content.toString();

      // Handle large files (warn if > 10MB)
      const sizeMB = jsonString.length / (1024 * 1024);
      if (sizeMB > 10) {
        console.warn(`[Todo2Watcher] Large file detected: ${sizeMB.toFixed(2)}MB`);
      }

      // Parse JSON
      const data: Todo2State = JSON.parse(jsonString);
      this.state = data;

      // Log stats
      const taskCount = data.todos?.length || 0;
      console.log(`[Todo2Watcher] Loaded ${taskCount} tasks`);

      // Notify listeners
      this.notifyListeners();
    } catch (error: any) {
      console.error('[Todo2Watcher] Error loading tasks:', error.message);
      
      // Show user-friendly error
      if (error instanceof SyntaxError) {
        vscode.window.showWarningMessage(
          'Todo2 file contains invalid JSON. Please check the file format.'
        );
      }
    } finally {
      this.isLoading = false;
    }
  }

  /**
   * Notify all listeners of task changes
   */
  private notifyListeners(): void {
    const tasks = this.getTasks();
    this.onTasksChanged.forEach(callback => {
      try {
        callback(tasks);
      } catch (error) {
        console.error('[Todo2Watcher] Error in listener callback:', error);
      }
    });
  }

  /**
   * Get current tasks
   */
  public getTasks(): Todo2Task[] {
    return this.state?.todos || [];
  }

  /**
   * Get current state
   */
  public getState(): Todo2State | null {
    return this.state;
  }

  /**
   * Get task by ID
   */
  public getTask(taskId: string): Todo2Task | undefined {
    return this.getTasks().find(task => task.id === taskId);
  }

  /**
   * Get tasks by status
   */
  public getTasksByStatus(status: string): Todo2Task[] {
    return this.getTasks().filter(task => task.status === status);
  }

  /**
   * Get tasks by priority
   */
  public getTasksByPriority(priority: string): Todo2Task[] {
    return this.getTasks().filter(task => task.priority === priority);
  }

  /**
   * Register callback for task changes
   */
  public onChanged(callback: (tasks: Todo2Task[]) => void): void {
    this.onTasksChanged.push(callback);
  }

  /**
   * Remove callback
   */
  public removeListener(callback: (tasks: Todo2Task[]) => void): void {
    const index = this.onTasksChanged.indexOf(callback);
    if (index > -1) {
      this.onTasksChanged.splice(index, 1);
    }
  }

  /**
   * Manually refresh tasks
   */
  public async refresh(): Promise<void> {
    await this.loadTasks();
  }

  /**
   * Dispose watcher
   */
  public dispose(): void {
    if (this.loadDebounceTimer) {
      clearTimeout(this.loadDebounceTimer);
    }
    this.watcher?.dispose();
    this.onTasksChanged = [];
  }
}

