/**
 * Todo2 Watcher Test
 * 
 * Manual test script to validate Todo2 file watching functionality.
 * 
 * To test:
 * 1. Create a test Todo2 file at `.todo2/state.todo2.json`
 * 2. Run this script with Node.js
 * 3. Make changes to the file and observe output
 */

import * as fs from 'fs';
import * as path from 'path';
import { watch } from 'fs';

interface Todo2Task {
  id: string;
  name?: string;
  status?: string;
  priority?: string;
}

interface Todo2State {
  todos: Todo2Task[];
}

/**
 * Test Todo2 file watcher
 */
function testTodo2Watcher() {
  const testFile = path.join(process.cwd(), '.todo2', 'state.todo2.json');
  const testDir = path.dirname(testFile);

  console.log('=== Todo2 Watcher Test ===\n');
  console.log(`Watching: ${testFile}`);
  console.log(`Working directory: ${process.cwd()}\n`);

  // Check if file exists
  if (!fs.existsSync(testFile)) {
    console.log('❌ Todo2 file not found. Creating test file...');
    
    // Create directory if needed
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }

    // Create test file
    const testState: Todo2State = {
      todos: [
        {
          id: 'TEST-001',
          name: 'Test Task 1',
          status: 'Todo',
          priority: 'high'
        },
        {
          id: 'TEST-002',
          name: 'Test Task 2',
          status: 'In Progress',
          priority: 'medium'
        }
      ]
    };

    fs.writeFileSync(testFile, JSON.stringify(testState, null, 2));
    console.log('✅ Created test file with 2 tasks\n');
  } else {
    console.log('✅ Todo2 file found\n');
  }

  // Load initial state
  console.log('--- Initial Load ---');
  loadAndDisplayTasks(testFile);

  // Watch for changes
  console.log('\n--- Watching for Changes ---');
  console.log('Make changes to the file to test watching...\n');

  const watcher = watch(testFile, { persistent: true }, (eventType, filename) => {
    console.log(`\n[${new Date().toISOString()}] File event: ${eventType}`);
    
    if (eventType === 'change') {
      // Debounce to handle rapid changes
      setTimeout(() => {
        console.log('\n--- Change Detected ---');
        loadAndDisplayTasks(testFile);
      }, 100);
    } else if (eventType === 'rename') {
      console.log('File renamed or deleted');
    }
  });

  console.log('Watcher started. Press Ctrl+C to stop.\n');

  // Handle cleanup
  process.on('SIGINT', () => {
    console.log('\n\nStopping watcher...');
    watcher.close();
    process.exit(0);
  });
}

/**
 * Load and display tasks from Todo2 file
 */
function loadAndDisplayTasks(filePath: string): void {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const state: Todo2State = JSON.parse(content);
    
    const tasks = state.todos || [];
    console.log(`Tasks loaded: ${tasks.length}`);
    
    if (tasks.length > 0) {
      console.log('\nTasks:');
      tasks.forEach((task, index) => {
        console.log(`  ${index + 1}. [${task.status || 'Unknown'}] ${task.name || task.id}`);
      });
    }

    // Check file size
    const stats = fs.statSync(filePath);
    const sizeMB = stats.size / (1024 * 1024);
    if (sizeMB > 1) {
      console.log(`\n⚠️  Large file: ${sizeMB.toFixed(2)}MB`);
    }

  } catch (error: any) {
    if (error.code === 'ENOENT') {
      console.log('❌ File not found');
    } else if (error instanceof SyntaxError) {
      console.log('❌ Invalid JSON:', error.message);
    } else {
      console.log('❌ Error:', error.message);
    }
  }
}

// Run test
if (require.main === module) {
  testTodo2Watcher();
}

