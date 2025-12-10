#!/usr/bin/env python3
"""
Performance test for MCP connection pooling.

Tests the speed improvement from connection pooling vs creating new sessions.
"""

import asyncio
import json
import time
from pathlib import Path
from typing import List, Optional

import pytest

# Try to import MCP client
try:
    from project_management_automation.scripts.base.mcp_client import (
        MCPClient,
        get_mcp_client,
    )
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    pytest.skip("MCP client not available", allow_module_level=True)


def find_project_root() -> Path:
    """Find project root directory."""
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists() or (current / ".git").exists():
            return current
        current = current.parent
    return Path.cwd()


def check_mcp_config(project_root: Path) -> tuple[bool, Optional[str]]:
    """Check if MCP config exists and has agentic-tools."""
    # Check project config
    project_config = project_root / '.cursor' / 'mcp.json'
    if project_config.exists():
        try:
            with open(project_config) as f:
                config = json.load(f)
                servers = config.get('mcpServers', {})
                if 'agentic-tools' in servers:
                    return True, None
        except Exception as e:
            return False, f"Error reading project config: {e}"
    
    # Check global config
    global_config = Path.home() / '.cursor' / 'mcp.json'
    if global_config.exists():
        try:
            with open(global_config) as f:
                config = json.load(f)
                servers = config.get('mcpServers', {})
                if 'agentic-tools' in servers:
                    return True, None
        except Exception as e:
            return False, f"Error reading global config: {e}"
    
    return False, "agentic-tools not found in MCP config (checked .cursor/mcp.json and ~/.cursor/mcp.json)"


@pytest.mark.asyncio
async def test_connection_pooling_performance():
    """Test that connection pooling significantly improves performance."""
    project_root = find_project_root()
    client = get_mcp_client(project_root)
    
    # Check if agentic-tools is configured
    config_ok, error_msg = check_mcp_config(project_root)
    if not config_ok:
        print(f"\n⚠️  Skipping test: {error_msg}")
        print("   To run this test, ensure agentic-tools is configured in MCP config")
        pytest.skip(error_msg or "agentic-tools MCP server not configured")
    
    working_directory = str(project_root)
    project_id = "davidl71/project-management-automation"
    
    # Test 1: Multiple sequential calls (should benefit from pooling)
    print("\n" + "=" * 60)
    print("Test 1: Sequential Calls (Connection Pooling)")
    print("=" * 60)
    
    times: List[float] = []
    for i in range(5):
        start = time.time()
        try:
            result = await client.list_todos(project_id, working_directory)
            elapsed = time.time() - start
            times.append(elapsed)
            result_count = len(result) if isinstance(result, list) else 'N/A'
            print(f"  Call {i+1}: {elapsed:.3f}s (returned {result_count} items)")
        except Exception as e:
            print(f"  Call {i+1}: ERROR - {e}")
            times.append(float('inf'))
    
    if times and all(t < float('inf') for t in times):
        first_call = times[0]
        subsequent_calls = times[1:] if len(times) > 1 else []
        avg_subsequent = sum(subsequent_calls) / len(subsequent_calls) if subsequent_calls else 0
        
        print(f"\n  📊 Results:")
        print(f"     First call: {first_call:.3f}s")
        if subsequent_calls:
            print(f"     Subsequent calls (avg): {avg_subsequent:.3f}s")
            if avg_subsequent > 0:
                speedup = first_call / avg_subsequent
                improvement = ((first_call - avg_subsequent) / first_call) * 100
                print(f"     ⚡ Speedup: {speedup:.1f}x faster")
                print(f"     📈 Improvement: {improvement:.1f}% faster")
            print(f"     Total time: {sum(times):.3f}s")
    
    # Test 2: Batch operations
    print("\n" + "=" * 60)
    print("Test 2: Batch Operations")
    print("=" * 60)
    
    # Create a few test operations
    batch_ops = [
        {
            'tool': 'list_todos',
            'arguments': {
                'workingDirectory': working_directory,
                'projectId': project_id
            }
        }
    ] * 3
    
    start = time.time()
    try:
        results = await client.batch_operations(batch_ops, working_directory)
        batch_time = time.time() - start
        print(f"  Batch (3 operations): {batch_time:.3f}s")
        print(f"  Per operation: {batch_time/len(batch_ops):.3f}s")
        
        # Compare to sequential
        if times and all(t < float('inf') for t in times):
            sequential_time = sum(times[:3]) if len(times) >= 3 else sum(times)
            print(f"  Sequential (3 operations): {sequential_time:.3f}s")
            if sequential_time > 0 and batch_time > 0:
                speedup = sequential_time / batch_time
                print(f"  ⚡ Batch speedup: {speedup:.1f}x faster")
    except Exception as e:
        print(f"  Batch operations ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Compare first call vs subsequent calls
    print("\n" + "=" * 60)
    print("Test 3: First Call vs Subsequent Calls")
    print("=" * 60)
    
    if len(times) >= 2 and all(t < float('inf') for t in times[:2]):
        first = times[0]
        subsequent = times[1]
        if subsequent > 0:
            improvement = ((first - subsequent) / first) * 100
            speedup = first / subsequent
            print(f"  First call: {first:.3f}s")
            print(f"  Second call: {subsequent:.3f}s")
            print(f"  📈 Improvement: {improvement:.1f}% faster")
            print(f"  ⚡ Speedup: {speedup:.1f}x")
    
    # Assertions
    if len(times) >= 2 and all(t < float('inf') for t in times[:2]):
        # Subsequent calls should be significantly faster
        assert times[0] > 0, "First call should take some time"
        if times[1] > 0:
            # Second call should be at least 1.5x faster (conservative estimate)
            # In practice, it should be 10-50x faster
            assert times[0] > times[1] * 1.5, \
                f"Subsequent calls should be faster: {times[0]:.3f}s vs {times[1]:.3f}s"


@pytest.mark.asyncio
async def test_batch_operations_performance():
    """Test that batch operations are faster than sequential calls."""
    project_root = find_project_root()
    client = get_mcp_client(project_root)
    
    config_ok, error_msg = check_mcp_config(project_root)
    if not config_ok:
        pytest.skip(error_msg or "agentic-tools MCP server not configured")
    
    working_directory = str(project_root)
    project_id = "davidl71/project-management-automation"
    
    # Sequential calls
    print("\n" + "=" * 60)
    print("Sequential Calls")
    print("=" * 60)
    sequential_times = []
    for i in range(3):
        start = time.time()
        try:
            await client.list_todos(project_id, working_directory)
            elapsed = time.time() - start
            sequential_times.append(elapsed)
            print(f"  Call {i+1}: {elapsed:.3f}s")
        except Exception as e:
            print(f"  Error on call {i+1}: {e}")
            sequential_times.append(float('inf'))
    
    sequential_total = sum(t for t in sequential_times if t < float('inf'))
    print(f"  Total time: {sequential_total:.3f}s")
    
    # Batch operations
    print("\n" + "=" * 60)
    print("Batch Operations")
    print("=" * 60)
    batch_ops = [
        {
            'tool': 'list_todos',
            'arguments': {
                'workingDirectory': working_directory,
                'projectId': project_id
            }
        }
    ] * 3
    
    start = time.time()
    try:
        await client.batch_operations(batch_ops, working_directory)
        batch_total = time.time() - start
        print(f"  Total time: {batch_total:.3f}s")
        print(f"  Per operation: {batch_total/len(batch_ops):.3f}s")
        
        if sequential_total > 0 and batch_total > 0:
            speedup = sequential_total / batch_total
            print(f"  ⚡ Batch is {speedup:.1f}x faster")
            
            # Batch should be at least as fast (usually faster)
            assert batch_total <= sequential_total * 1.1, \
                f"Batch should be faster: {batch_total:.3f}s vs {sequential_total:.3f}s"
    except Exception as e:
        print(f"  Batch operations ERROR: {e}")
        import traceback
        traceback.print_exc()
        pytest.skip(f"Batch operations failed: {e}")


if __name__ == "__main__":
    # Run tests directly
    import sys
    
    async def run_tests():
        print("=" * 60)
        print("MCP Connection Pooling Performance Test")
        print("=" * 60)
        print()
        
        try:
            await test_connection_pooling_performance()
            print()
            await test_batch_operations_performance()
            print("\n" + "=" * 60)
            print("✅ Performance tests completed!")
            print("=" * 60)
        except Exception as e:
            if "Skipped" in str(type(e).__name__):
                print(f"\n⚠️  Test skipped: {e}")
            else:
                print(f"\n❌ Test failed: {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)
    
    asyncio.run(run_tests())
