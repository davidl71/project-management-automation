# Breaking Test Results

**Date**: 2025-12-26  
**Goal**: Make a working tool fail by copying patterns from a failing tool

## Test Setup

- **Working Tool**: `estimation` (reported as working in comprehensive test)
- **Failing Tool**: `automation` (confirmed broken)
- **Change Made**: Added `tag_list: Optional[list[str]] = None` parameter to `estimation` to match `automation`'s `tasks: Optional[list[str]] = None` parameter

## Results

### Test 1: estimation without list[str] parameter
- **Status**: ❌ **BROKEN**
- **Error**: `object dict can't be used in 'await' expression`
- **Finding**: `estimation` was already broken, even without the `list[str]` parameter!

### Test 2: estimation WITH list[str] parameter
- **Status**: ❌ **BROKEN** (same error)
- **Finding**: Adding `list[str]` parameter didn't change the behavior - tool was already broken

### Test 3: automation (known broken)
- **Status**: ❌ **BROKEN** (confirmed)

## Key Discovery

**The `estimation` tool was already broken**, despite being reported as "working" in the comprehensive test. This suggests:

1. **The comprehensive test may have used different arguments** that hit a different code path
2. **The error occurs conditionally** based on which code path is executed
3. **The "working" status in the test may have been a false positive**

## Analysis

Looking at the `estimation` function implementation:

```python
elif action == "analyze":
    from .estimation_learner import EstimationLearner
    learner = EstimationLearner()
    result = learner.analyze_estimation_accuracy()
    return json.dumps(result, indent=2) if isinstance(result, dict) else result

elif action == "stats":
    from .task_duration_estimator import TaskDurationEstimator
    estimator = TaskDurationEstimator()
    stats = estimator.get_statistics()
    return json.dumps(stats, indent=2) if isinstance(stats, dict) else stats
```

Both branches:
1. Call a method that returns a dict
2. Check if result is dict and convert to JSON string
3. Return the result

**The issue**: FastMCP may be detecting the dict return type from `analyze_estimation_accuracy()` or `get_statistics()` during static analysis, even though we convert it to a JSON string before returning.

## Conclusion

The `list[str]` parameter is **NOT** the root cause. The issue is that:
- FastMCP performs static analysis on the call chain
- It detects dict return types in intermediate function calls
- Even though we convert dicts to JSON strings before returning, FastMCP flags the dict type in the call chain

## Next Steps

1. Check what `analyze_estimation_accuracy()` and `get_statistics()` return
2. See if making those functions return JSON strings directly fixes the issue
3. Compare with `run_daily_automation()` which already returns a JSON string

