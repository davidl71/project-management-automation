/**
 * Task Commands
 * 
 * Implements Exarp task management commands for the extension.
 */

import * as vscode from 'vscode';
import { Todo2StateReader, Todo2Task } from './todo2Reader';

export class TaskCommands {
    constructor(private todo2Reader: Todo2StateReader) {}

    /**
     * Create a new task via MCP server.
     * TODO: Implement MCP client integration
     */
    public async createTask() {
        // For Phase 1, show a placeholder
        vscode.window.showInformationMessage(
            'Exarp: Create Task command (MCP integration coming soon)'
        );
    }

    /**
     * List all pending tasks.
     */
    public async listTasks() {
        const tasks = this.todo2Reader.getPendingTasks();
        
        if (tasks.length === 0) {
            vscode.window.showInformationMessage('No pending tasks');
            return;
        }

        // Show tasks in quick pick
        const items = tasks.map(task => ({
            label: task.name,
            description: `ID: ${task.id}`,
            detail: `Priority: ${task.priority || 'medium'} | Tags: ${task.tags?.join(', ') || 'none'}`,
            task: task,
        }));

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: 'Select a task to view details',
        });

        if (selected) {
            vscode.window.showInformationMessage(
                `Selected: ${selected.label} (${selected.task.id})`
            );
        }
    }

    /**
     * Complete a task.
     * TODO: Implement MCP client integration to update task status
     */
    public async completeTask() {
        const tasks = this.todo2Reader.getPendingTasks();
        
        if (tasks.length === 0) {
            vscode.window.showInformationMessage('No pending tasks to complete');
            return;
        }

        const items = tasks.map(task => ({
            label: task.name,
            description: `ID: ${task.id}`,
            task: task,
        }));

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: 'Select a task to complete',
        });

        if (selected) {
            // For Phase 1, show a placeholder
            vscode.window.showInformationMessage(
                `Exarp: Complete Task "${selected.label}" (MCP integration coming soon)`
            );
        }
    }
}
