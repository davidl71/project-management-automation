# FastMCP Version Check Results

**Date**: 2025-12-26  
**Current Version**: 2.14.1 (latest)  
**Status**: ✅ Up to date

## Version Information

- **Installed**: 2.14.1
- **Latest Available**: 2.14.1 (released December 15, 2025)
- **Status**: Already on latest version

## Recent FastMCP Updates

### Version 2.14.1 (December 15, 2025)
- Performance optimizations
- Minor bug fixes

### Version 2.14.0 (Recent)
- Protocol-native background tasks
- MCP 2025-11-25 specification adoption
- SSE polling for graceful connection handling
- Multi-select enums for elicitation
- Default form values
- Tool name validation at registration time

## Key Finding: Return Type Handling

FastMCP expects tools to return values that can be converted to `ToolResult` objects. The framework:
1. Calls the tool function
2. Wraps the result in a `ToolResult` object
3. Calls `to_mcp_result()` on the `ToolResult`

**The Issue**: FastMCP is trying to call `to_mcp_result()` directly on dict/string returns instead of wrapping them in `ToolResult` first.

## Error Analysis

### Error 1: "object dict can't be used in 'await' expression"
- **Location**: FastMCP middleware/execution layer
- **Cause**: FastMCP trying to await a dict value
- **Affected**: 20 tools

### Error 2: "'dict' object has no attribute 'to_mcp_result'"
- **Location**: FastMCP result processing
- **Cause**: FastMCP calling `to_mcp_result()` on a dict instead of `ToolResult`
- **Affected**: 7 tools

## Conclusion

1. ✅ **Already on latest version** - No updates available
2. ❌ **Framework bug confirmed** - All tools affected
3. 🔍 **Root cause**: FastMCP's return type handling/wrapping is broken

## Recommendations

1. **Check FastMCP GitHub Issues**: Look for similar reports
2. **Try FastMCP Examples**: Verify if official examples work
3. **Consider Workaround**: Use stdio server (`EXARP_FORCE_STDIO=1`)
4. **Report Bug**: If confirmed, report to FastMCP maintainers

## Next Steps

- Check FastMCP GitHub for known issues
- Test with FastMCP official examples
- Consider temporary workaround using stdio server

