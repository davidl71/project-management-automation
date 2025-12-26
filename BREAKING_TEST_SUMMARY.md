# Breaking Test Summary

**Date**: 2025-12-26  
**Test**: Try to break a working tool by copying patterns from a failing tool

## Findings

1. **`estimation` was already broken** - Despite being reported as "working" in comprehensive test
2. **`list[str]` parameters are NOT the issue** - Adding them didn't change behavior
3. **Making underlying functions return JSON strings didn't fix it** - Still broken after fixing `get_statistics()`
4. **Exception handlers with dict returns are detected** - But fixing them didn't fix the tool either

## Conclusion

FastMCP's static analysis is detecting dict returns in ways we haven't fully identified yet. The issue may be:
- Detecting dict literals in function bodies (even if converted to strings)
- Analyzing intermediate variables
- Detecting dict types in type annotations
- A deeper framework bug that can't be fixed at the application level

## Recommendation

Since we can't reliably fix tools by removing dict returns, the workaround (`EXARP_FORCE_STDIO=1`) remains the best solution until FastMCP fixes the framework bug.

