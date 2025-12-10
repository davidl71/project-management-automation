# MCP Extension Evaluation


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on Rust, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use Rust patterns? use context7"
> - "Show me Rust examples examples use context7"
> - "Rust best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

**Date:** 2025-11-26  
**Status:** Evaluated - Not Adopted

## Extensions Evaluated

Four MCP-related extensions were evaluated for potential adoption:

| Extension | Publisher | Status |
|-----------|-----------|--------|
| `automatalabs.copilot-mcp` | Automata Labs | Not in marketplace |
| `aipolabs.aci-vibeops-extension` | Aipo Labs | Not found |
| `sachinhg.knowledge-bank-mcp` | sachinhg | Not found |
| `corespeed.corespeed-mcp-store` | CoreSpeed | Not found |

## Evaluation Details

### 1. automatalabs.copilot-mcp

**What it does:**
- Bridges GitHub Copilot with MCP servers
- Exposes MCP tools to Copilot Chat
- Server discovery and health monitoring
- Auto-reconnect for MCP connections

**Why not adopted:**
- **Cursor has native MCP support** - We use Cursor, not VS Code + Copilot
- MCP servers are configured directly in `.cursor/mcp.json`
- `yutengjing.vscode-mcp-bridge` already installed for any bridge needs
- Adding this would be redundant

**Decision:** ❌ SKIP - Redundant with Cursor's native MCP support

### 2. aipolabs.aci-vibeops-extension

**What it might do:**
- "VibeOps" suggests AI-powered DevOps workflows
- Likely early-stage or internal tool

**Why not adopted:**
- Not available in VS Code or Cursor marketplace
- No public documentation found
- Cannot evaluate features without access

**Decision:** ❌ SKIP - Not publicly available

### 3. sachinhg.knowledge-bank-mcp

**What it might do:**
- Knowledge base/memory system via MCP
- Similar concept to OpenMemory

**Why not adopted:**
- Not available in marketplace
- We already have comprehensive memory solutions:
  - `mem0.openmemory` extension (installed)
  - Exarp `session_memory` tools (`save_memory`, `recall_context`, `search_memories`)
  - `agentic-tools` memory system via MCP

**Decision:** ❌ SKIP - Already have better alternatives

### 4. corespeed.corespeed-mcp-store

**What it might do:**
- MCP server marketplace/discovery
- Similar to Smithery.ai

**Why not adopted:**
- Not available in marketplace
- We manually configure MCP servers in `mcp.json`
- Current servers are well-documented and purpose-built
- Discovery tools add complexity without clear benefit

**Decision:** ❌ SKIP - Not available, manual config sufficient

## Current MCP Setup

Our existing MCP infrastructure is comprehensive:

### MCP Servers (in `.cursor/mcp.json`)

| Server | Purpose |
|--------|---------|
| `exarp_ib` | Project automation for ib_box_spread |
| `exarp_pma` | Project automation for project-management-automation |
| `context7` | Up-to-date library documentation |
| `interactive` | Human-in-the-loop prompts and notifications |
| `agentic-tools` | Task and memory management |
| `tractatus_thinking` | Logical concept analysis |
| `sequential_thinking` | Implementation workflow planning |
| `filesystem` | File system operations |

### MCP-Related Extensions

| Extension | Purpose |
|-----------|---------|
| `yutengjing.vscode-mcp-bridge` | MCP server bridge |
| `mem0.openmemory` | AI memory persistence |
| `todo2.todo2` | Task management |

## Conclusion

No additional MCP extensions are needed. The current setup provides:

- ✅ **Automation:** Exarp tools for project health, security, task management
- ✅ **Memory:** OpenMemory + Exarp session memory + agentic-tools
- ✅ **Documentation:** Context7 for library docs
- ✅ **Interactivity:** interactive-mcp for human-in-the-loop
- ✅ **Thinking:** Tractatus + Sequential for structured analysis
- ✅ **Task Management:** Todo2 + Exarp integration

Adding the evaluated extensions would either be redundant or unavailable.

## Extension Management Best Practices

### Workspace Recommendations

Extensions can be recommended per-workspace via `.vscode/extensions.json`:

```json
{
  "recommendations": ["publisher.extension"],
  "unwantedRecommendations": ["publisher.unwanted"]
}
```

This is configured in both projects to:
- Recommend project-specific extensions (C++, Rust, Swift for ib_box_spread)
- Block unwanted/redundant extensions (90+ in unwantedRecommendations)

### Enterprise Considerations

For organizations managing extensions centrally:
- Use `extensions.allowed` setting to whitelist extensions
- Consider [Private Marketplace](https://code.visualstudio.com/blogs/2025/11/18/PrivateMarketplace) for internal distribution
- Extensions install to `~/.cursor/extensions/` (or `~/.vscode/extensions/`)

## References

- [VS Code Extension Marketplace](https://code.visualstudio.com/docs/configure/extensions/extension-marketplace) - Official extension management docs
- [Private Marketplace for Extensions](https://code.visualstudio.com/blogs/2025/11/18/PrivateMarketplace) - Enterprise extension hosting
- [Automata Labs - copilot-mcp](https://www.automatalabs.io/projects/copilot-mcp)
- [Smithery.ai - MCP Server Directory](https://smithery.ai)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)

