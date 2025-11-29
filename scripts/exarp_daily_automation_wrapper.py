#!/usr/bin/env python3
"""
Exarp Daily Automation Wrapper

This script orchestrates Exarp MCP tools to replicate daily automation functionality.
It calls all three Exarp checks and generates a combined report.

Usage:
    python3 scripts/exarp_daily_automation_wrapper.py [project_dir] [--dry-run] [--json] [--auto-fix]

Options:
    --dry-run    Run in dry-run mode (no changes)
    --json       Output results as JSON
    --auto-fix   Auto-fix duplicate tasks (ignored in dry-run mode)
"""

import sys
import json
import signal
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class TimeoutError(Exception):
    """Timeout exception for long-running operations"""
    pass


def timeout_handler(signum, frame):
    """Handle timeout signal"""
    raise TimeoutError("Operation timed out")


class ExarpDailyAutomation:
    """Wrapper for Exarp daily automation tasks"""
    
    def __init__(self, project_dir: Path, dry_run: bool = False, json_output: bool = False):
        self.project_dir = project_dir.resolve()
        self.dry_run = dry_run
        self.json_output = json_output
        self.results: Dict[str, Any] = {
            'timestamp': datetime.now().isoformat(),
            'project_dir': str(self.project_dir),
            'dry_run': dry_run,
            'tasks': {}
        }
    
    def run_tool(self, tool_func, tool_name: str, *args, timeout: int = 300, **kwargs) -> Dict[str, Any]:
        """Run an Exarp tool function with timeout handling"""
        start_time = time.time()
        
        try:
            # Set up timeout (Unix only)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout)
            
            # Run the tool
            result_str = tool_func(*args, **kwargs)
            result_data = json.loads(result_str)
            
            # Cancel timeout
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
            duration = time.time() - start_time
            
            task_result = {
                'success': result_data.get('success', False),
                'duration_seconds': duration,
                'data': result_data.get('data', {}),
                'error': result_data.get('error'),
                'tool_name': tool_name
            }
            
            if not self.json_output:
                if task_result['success']:
                    print(f"✅ {tool_name}: Success ({duration:.2f}s)")
                else:
                    error_msg = task_result.get('error', {}).get('message', 'Unknown error')
                    print(f"❌ {tool_name}: Failed ({duration:.2f}s)")
                    print(f"   Error: {error_msg[:200]}")
            
            return task_result
            
        except TimeoutError:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            error_msg = f"{tool_name} timed out after {timeout} seconds"
            if not self.json_output:
                print(f"⏱️  {error_msg}")
            return {
                'success': False,
                'duration_seconds': timeout,
                'error': error_msg,
                'tool_name': tool_name
            }
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse {tool_name} response: {e}"
            if not self.json_output:
                print(f"❌ {error_msg}")
            return {
                'success': False,
                'duration_seconds': time.time() - start_time,
                'error': error_msg,
                'tool_name': tool_name
            }
        except Exception as e:
            error_msg = f"{tool_name} failed: {str(e)}"
            if not self.json_output:
                print(f"❌ {error_msg}")
            return {
                'success': False,
                'duration_seconds': time.time() - start_time,
                'error': error_msg,
                'tool_name': tool_name
            }
    
    def check_documentation_health(self) -> Dict[str, Any]:
        """Run documentation health check"""
        if not self.json_output:
            print("\n📚 Task 1: Checking documentation health...")
        
        try:
            from project_management_automation.tools.documentation_health import check_documentation_health
            
            result = self.run_tool(
                check_documentation_health,
                'Documentation Health',
                output_path=None,
                create_tasks=True,
                timeout=300
            )
            self.results['tasks']['docs_health'] = result
            return result
        except ImportError as e:
            error_msg = f"Failed to import documentation_health tool: {e}"
            if not self.json_output:
                print(f"❌ {error_msg}")
            result = {
                'success': False,
                'error': error_msg,
                'tool_name': 'Documentation Health'
            }
            self.results['tasks']['docs_health'] = result
            return result
    
    def analyze_todo2_alignment(self) -> Dict[str, Any]:
        """Run Todo2 alignment analysis"""
        if not self.json_output:
            print("\n🎯 Task 2: Analyzing Todo2 alignment...")
        
        try:
            from project_management_automation.tools.todo2_alignment import analyze_todo2_alignment
            
            result = self.run_tool(
                analyze_todo2_alignment,
                'Todo2 Alignment',
                create_followup_tasks=True,
                output_path=None,
                timeout=300
            )
            self.results['tasks']['todo2_alignment'] = result
            return result
        except ImportError as e:
            error_msg = f"Failed to import todo2_alignment tool: {e}"
            if not self.json_output:
                print(f"❌ {error_msg}")
            result = {
                'success': False,
                'error': error_msg,
                'tool_name': 'Todo2 Alignment'
            }
            self.results['tasks']['todo2_alignment'] = result
            return result
    
    def detect_duplicate_tasks(self, auto_fix: bool = False) -> Dict[str, Any]:
        """Run duplicate task detection"""
        if not self.json_output:
            print("\n🔍 Task 3: Detecting duplicate tasks...")
        
        try:
            from project_management_automation.tools.duplicate_detection import detect_duplicate_tasks
            
            result = self.run_tool(
                detect_duplicate_tasks,
                'Duplicate Detection',
                similarity_threshold=0.85,
                auto_fix=auto_fix and not self.dry_run,
                output_path=None,
                timeout=300
            )
            self.results['tasks']['duplicate_detection'] = result
            return result
        except ImportError as e:
            error_msg = f"Failed to import duplicate_detection tool: {e}"
            if not self.json_output:
                print(f"❌ {error_msg}")
            result = {
                'success': False,
                'error': error_msg,
                'tool_name': 'Duplicate Detection'
            }
            self.results['tasks']['duplicate_detection'] = result
            return result
    
    def run_all(self, auto_fix_duplicates: bool = False) -> Dict[str, Any]:
        """Run all Exarp daily automation tasks"""
        if not self.json_output:
            print("🚀 Starting Exarp daily automation...")
            print(f"Project directory: {self.project_dir}")
            if self.dry_run:
                print("Mode: DRY-RUN (no changes will be made)")
            print()
        
        # Change to project directory
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(self.project_dir)
            
            # Run all tasks
            self.check_documentation_health()
            self.analyze_todo2_alignment()
            self.detect_duplicate_tasks(auto_fix=auto_fix_duplicates)
        finally:
            os.chdir(original_cwd)
        
        # Calculate summary
        all_success = all(
            task.get('success', False)
            for task in self.results['tasks'].values()
        )
        
        total_duration = sum(
            task.get('duration_seconds', 0)
            for task in self.results['tasks'].values()
        )
        
        self.results['summary'] = {
            'all_success': all_success,
            'tasks_completed': len(self.results['tasks']),
            'tasks_succeeded': sum(1 for t in self.results['tasks'].values() if t.get('success', False)),
            'tasks_failed': sum(1 for t in self.results['tasks'].values() if not t.get('success', False)),
            'total_duration_seconds': total_duration
        }
        
        if not self.json_output:
            print("\n" + "=" * 70)
            print("📊 Summary:")
            print(f"   Tasks completed: {self.results['summary']['tasks_completed']}")
            print(f"   Tasks succeeded: {self.results['summary']['tasks_succeeded']}")
            print(f"   Tasks failed: {self.results['summary']['tasks_failed']}")
            print(f"   Total duration: {total_duration:.2f}s")
            if all_success:
                print("   ✅ All tasks completed successfully")
            else:
                print("   ⚠️  Some tasks failed - check output above")
            print("=" * 70)
        
        return self.results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Exarp daily automation wrapper - orchestrates Exarp MCP tools'
    )
    parser.add_argument(
        'project_dir',
        nargs='?',
        default='.',
        help='Project directory (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry-run mode (no changes)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--auto-fix',
        action='store_true',
        help='Auto-fix duplicate tasks (ignored in dry-run mode)'
    )
    
    args = parser.parse_args()
    
    project_dir = Path(args.project_dir).resolve()
    
    if not project_dir.exists():
        print(f"Error: Project directory does not exist: {project_dir}", file=sys.stderr)
        sys.exit(1)
    
    automation = ExarpDailyAutomation(
        project_dir=project_dir,
        dry_run=args.dry_run,
        json_output=args.json
    )
    
    results = automation.run_all(auto_fix_duplicates=args.auto_fix and not args.dry_run)
    
    if args.json:
        print(json.dumps(results, indent=2))
    
    # Exit with error code if any task failed
    if not results['summary']['all_success']:
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
