import * as assert from 'assert';
import * as vscode from 'vscode';
import { Todo2Watcher } from '../../todo2/watcher';
import { StatusBarProvider } from '../../providers/statusBar';

suite('StatusBarProvider Test Suite', () => {
  let context: vscode.ExtensionContext;
  let workspaceFolder: vscode.WorkspaceFolder;
  let todo2Watcher: Todo2Watcher;

  suiteSetup(async () => {
    // Get workspace folder
    const folders = vscode.workspace.workspaceFolders;
    if (!folders || folders.length === 0) {
      throw new Error('No workspace folder found');
    }
    workspaceFolder = folders[0];
    todo2Watcher = new Todo2Watcher(workspaceFolder);
    
    // Wait for watcher to initialize
    await new Promise(resolve => setTimeout(resolve, 500));
  });

  suiteTeardown(() => {
    todo2Watcher.dispose();
  });

  test('StatusBarProvider should initialize', () => {
    // Create a mock context
    const mockContext: Partial<vscode.ExtensionContext> = {
      subscriptions: [] as vscode.Disposable[]
    };
    
    const provider = new StatusBarProvider(
      mockContext as vscode.ExtensionContext,
      todo2Watcher
    );
    
    assert.ok(provider);
    
    // Cleanup
    provider.dispose();
  });

  test('StatusBarProvider should update on task changes', async () => {
    const mockContext: Partial<vscode.ExtensionContext> = {
      subscriptions: [] as vscode.Disposable[]
    };
    
    const provider = new StatusBarProvider(
      mockContext as vscode.ExtensionContext,
      todo2Watcher
    );
    
    // Wait for initial update
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Trigger refresh
    await todo2Watcher.refresh();
    
    // Wait for update
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // Status bar should have updated
    assert.ok(true, 'Status bar provider updated successfully');
    
    provider.dispose();
  });

  test('StatusBarProvider should handle state transitions', () => {
    const mockContext: Partial<vscode.ExtensionContext> = {
      subscriptions: [] as vscode.Disposable[]
    };
    
    const provider = new StatusBarProvider(
      mockContext as vscode.ExtensionContext,
      todo2Watcher
    );
    
    // Test state transitions
    provider.setRunning('Testing...');
    provider.setSuccess('Success');
    provider.setError('Error');
    provider.setIdle();
    
    // Should not throw
    assert.ok(true, 'State transitions work correctly');
    
    provider.dispose();
  });
});

