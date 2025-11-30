import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Test Tree Item
 */
export class TestTreeItem extends vscode.TreeItem {
  constructor(
    public readonly label: string,
    public readonly collapsibleState: vscode.TreeItemCollapsibleState,
    public readonly testFile?: string,
    public readonly testSuite?: string,
    public readonly icon?: string
  ) {
    super(label, collapsibleState);

    this.tooltip = testFile ? `Test file: ${testFile}` : label;
    this.description = testFile ? path.basename(testFile) : undefined;

    if (icon) {
      this.iconPath = new vscode.ThemeIcon(icon);
    }
  }

  contextValue = this.testFile ? 'testFile' : 'testSuite';
}

/**
 * Test Tree View Provider
 * 
 * Shows test files and suites in the sidebar for easy navigation and running.
 */
export class TestTreeViewProvider implements vscode.TreeDataProvider<TestTreeItem> {
  private _onDidChangeTreeData: vscode.EventEmitter<TestTreeItem | undefined | null | void> = new vscode.EventEmitter<TestTreeItem | undefined | null | void>();
  readonly onDidChangeTreeData: vscode.Event<TestTreeItem | undefined | null | void> = this._onDidChangeTreeData.event;

  constructor(private workspaceFolder: vscode.WorkspaceFolder) {}

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: TestTreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(element?: TestTreeItem): Thenable<TestTreeItem[]> {
    if (!element) {
      // Root level - show test suites
      return Promise.resolve(this.getTestSuites());
    } else if (element.testFile) {
      // Show tests in a test file
      return Promise.resolve(this.getTestsInFile(element.testFile));
    } else {
      return Promise.resolve([]);
    }
  }

  private getTestSuites(): TestTreeItem[] {
    console.log('[TestTreeView] Getting test suites...');
    console.log('[TestTreeView] Workspace folder:', this.workspaceFolder.uri.fsPath);
    
    // Try multiple possible test directory paths
    const possiblePaths = [
      // Workspace root with extension subdirectory
      path.join(this.workspaceFolder.uri.fsPath, 'extension', 'src', 'test', 'suite'),
      // Extension directory as workspace root
      path.join(this.workspaceFolder.uri.fsPath, 'src', 'test', 'suite'),
      // Current directory structure
      path.join(this.workspaceFolder.uri.fsPath, 'src', 'test', 'suite'),
      // Fallback: search for test directories
      path.join(this.workspaceFolder.uri.fsPath, 'test', 'suite'),
    ];

    let testDir: string | null = null;
    for (const testPath of possiblePaths) {
      console.log('[TestTreeView] Checking path:', testPath, 'exists:', fs.existsSync(testPath));
      if (fs.existsSync(testPath)) {
        testDir = testPath;
        console.log('[TestTreeView] Found test directory:', testDir);
        break;
      }
    }

    // If not found, try to find test files recursively
    if (!testDir) {
      console.log('[TestTreeView] Test directory not found, searching recursively...');
      const recursiveResults = this.findTestFilesRecursively(this.workspaceFolder.uri.fsPath);
      console.log('[TestTreeView] Found', recursiveResults.length, 'test files recursively');
      if (recursiveResults.length > 0) {
        return recursiveResults;
      }
      
      // Show helpful message
      return [
        new TestTreeItem(
          'No test files found - Click to refresh',
          vscode.TreeItemCollapsibleState.None,
          undefined,
          undefined,
          'info'
        )
      ];
    }

    const testFiles = fs.readdirSync(testDir)
      .filter(file => file.endsWith('.test.ts') || file.endsWith('.test.js') || file.endsWith('.spec.ts') || file.endsWith('.spec.js'))
      .map(file => path.join(testDir!, file));
    
    console.log('[TestTreeView] Found', testFiles.length, 'test files');

    if (testFiles.length === 0) {
      console.log('[TestTreeView] No test files in directory, searching recursively...');
      // Try recursive search as fallback
      const recursiveResults = this.findTestFilesRecursively(this.workspaceFolder.uri.fsPath);
      if (recursiveResults.length > 0) {
        console.log('[TestTreeView] Found', recursiveResults.length, 'test files recursively');
        return recursiveResults;
      }
      
      console.log('[TestTreeView] No test files found anywhere');
      return [
        new TestTreeItem(
          'No test files found - Check extension/src/test/suite/',
          vscode.TreeItemCollapsibleState.None,
          undefined,
          undefined,
          'info'
        )
      ];
    }

    return testFiles.map(file => {
      const fileName = path.basename(file);
      const suiteName = fileName.replace(/\.(test|spec)\.(ts|js)$/, '');
      const displayName = this.formatSuiteName(suiteName);

      // Count tests in file
      const testCount = this.countTestsInFile(file);

      return new TestTreeItem(
        `${displayName} (${testCount} tests)`,
        vscode.TreeItemCollapsibleState.Collapsed,
        file,
        suiteName,
        'beaker'
      );
    });
  }

  private getTestsInFile(testFile: string): TestTreeItem[] {
    try {
      const content = fs.readFileSync(testFile, 'utf8');
      const tests: TestTreeItem[] = [];

      // Extract suite name
      const suiteMatch = content.match(/suite\(['"]([^'"]+)['"]/);
      const suiteName = suiteMatch ? suiteMatch[1] : 'Tests';

      // Extract test names
      const testMatches = content.matchAll(/test\(['"]([^'"]+)['"]/g);
      
      for (const match of testMatches) {
        const testName = match[1];
        tests.push(
          new TestTreeItem(
            testName,
            vscode.TreeItemCollapsibleState.None,
            testFile,
            suiteName,
            'circle-outline'
          )
        );
      }

      return tests.length > 0 
        ? tests 
        : [
            new TestTreeItem(
              'No tests found',
              vscode.TreeItemCollapsibleState.None,
              undefined,
              undefined,
              'info'
            )
          ];
    } catch (error) {
      return [
        new TestTreeItem(
          `Error reading file: ${error}`,
          vscode.TreeItemCollapsibleState.None,
          undefined,
          undefined,
          'error'
        )
      ];
    }
  }

  private countTestsInFile(testFile: string): number {
    try {
      const content = fs.readFileSync(testFile, 'utf8');
      const matches = content.matchAll(/test\(['"]/g);
      return Array.from(matches).length;
    } catch {
      return 0;
    }
  }

  private formatSuiteName(name: string): string {
    // Convert kebab-case or snake_case to Title Case
    return name
      .split(/[-_]/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  private findTestFilesRecursively(rootPath: string): TestTreeItem[] {
    const testFiles: string[] = [];
    
    try {
      const walkDirectory = (dir: string, depth: number = 0): void => {
        // Limit recursion depth to avoid searching too deeply
        if (depth > 5) return;
        
        if (!fs.existsSync(dir)) return;
        
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        
        for (const entry of entries) {
          const fullPath = path.join(dir, entry.name);
          
          // Skip node_modules and other common ignore directories
          if (entry.isDirectory()) {
            const skipDirs = ['node_modules', '.git', 'out', 'dist', 'build', '.vscode-test'];
            if (skipDirs.includes(entry.name)) continue;
            
            walkDirectory(fullPath, depth + 1);
          } else if (entry.isFile()) {
            // Check if it's a test file
            if (entry.name.match(/\.(test|spec)\.(ts|js)$/i)) {
              testFiles.push(fullPath);
            }
          }
        }
      };
      
      walkDirectory(rootPath);
      
      if (testFiles.length === 0) {
        return [];
      }
      
      // Group test files by directory/suite
      const grouped = new Map<string, string[]>();
      for (const testFile of testFiles) {
        const dir = path.dirname(testFile);
        if (!grouped.has(dir)) {
          grouped.set(dir, []);
        }
        grouped.get(dir)!.push(testFile);
      }
      
      // Create tree items
      const items: TestTreeItem[] = [];
      for (const [dir, files] of grouped.entries()) {
        for (const testFile of files) {
          const fileName = path.basename(testFile);
          const suiteName = fileName.replace(/\.(test|spec)\.(ts|js)$/i, '');
          const displayName = this.formatSuiteName(suiteName);
          const testCount = this.countTestsInFile(testFile);
          
          items.push(
            new TestTreeItem(
              `${displayName} (${testCount} tests)`,
              vscode.TreeItemCollapsibleState.Collapsed,
              testFile,
              suiteName,
              'beaker'
            )
          );
        }
      }
      
      return items;
    } catch (error) {
      console.error('[TestTreeView] Error finding test files:', error);
      return [];
    }
  }
}

