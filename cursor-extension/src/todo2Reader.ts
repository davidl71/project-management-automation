/**
 * Todo2 State Reader
 * 
 * Reads and parses .todo2/state.todo2.json to extract task information.
 */

import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

export interface Todo2Task {
    id: string;
    name: string;
    status: string;
    priority?: string;
    tags?: string[];
}

export interface Todo2State {
    project?: {
        id: string;
        name: string;
        path: string;
    };
    todos: Todo2Task[];
}

export class Todo2StateReader {
    private workspaceRoot: string | undefined;

    constructor() {
        // Find workspace root
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders && workspaceFolders.length > 0) {
            this.workspaceRoot = workspaceFolders[0].uri.fsPath;
        }
    }

    /**
     * Get the path to the Todo2 state file.
     */
    private getStateFilePath(): string | null {
        if (!this.workspaceRoot) {
            return null;
        }
        return path.join(this.workspaceRoot, '.todo2', 'state.todo2.json');
    }

    /**
     * Read and parse the Todo2 state file.
     */
    public readState(): Todo2State | null {
        const filePath = this.getStateFilePath();
        if (!filePath || !fs.existsSync(filePath)) {
            return null;
        }

        try {
            const content = fs.readFileSync(filePath, 'utf-8');
            return JSON.parse(content) as Todo2State;
        } catch (error) {
            console.error('Failed to read Todo2 state:', error);
            return null;
        }
    }

    /**
     * Get count of pending tasks.
     */
    public getPendingTaskCount(): number {
        const state = this.readState();
        if (!state || !state.todos) {
            return 0;
        }

        return state.todos.filter(
            task => task.status === 'todo' || task.status === 'Todo' || task.status === 'pending'
        ).length;
    }

    /**
     * Get all pending tasks.
     */
    public getPendingTasks(): Todo2Task[] {
        const state = this.readState();
        if (!state || !state.todos) {
            return [];
        }

        return state.todos.filter(
            task => task.status === 'todo' || task.status === 'Todo' || task.status === 'pending'
        );
    }

    /**
     * Get task by ID.
     */
    public getTaskById(taskId: string): Todo2Task | null {
        const state = this.readState();
        if (!state || !state.todos) {
            return null;
        }

        return state.todos.find(task => task.id === taskId) || null;
    }
}
