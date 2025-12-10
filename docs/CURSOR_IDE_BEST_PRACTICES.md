# Cursor IDE: 10 Best Practices


> 💡 **AI Assistant Hint:** For up-to-date, version-specific documentation on FastAPI, Pydantic, Python, use the Context7 MCP server by appending `use context7` to your prompts. For example:
> - "How do I use FastAPI async endpoints? use context7"
> - "Show me FastAPI hooks examples use context7"
> - "FastAPI best practices 2025 use context7"
>
> Context7 provides current documentation (2025), version-specific API references, and real code examples without hallucinations.

> **Source:** [Mastering Cursor IDE: 10 Best Practices (Building a Daily Task Manager App)](https://medium.com/@roberto.g.infante/mastering-cursor-ide-10-best-practices-building-a-daily-task-manager-app-0b26524411c1) by Roberto Infante

## Overview

Cursor is an AI-powered code editor that deeply integrates large language models into your development workflow. It's like an always-on pair programmer inside your IDE — one that understands your codebase and can help you build features faster.

The overarching theme is **intentionality**. Using Cursor effectively means being intentional about how you engage with the AI. If you just treat it as fancy autocomplete and let it code willy-nilly, you may get inconsistent results. But if you guide it with clear requirements, rules, and context, it becomes a powerful force multiplier.

---

## The 10 Best Practices

### 1. Generate a PRD File

**Begin with a clear Product Requirements Document.**

Every successful project starts with a plan. A PRD (Product Requirements Document) is a blueprint that defines the app's purpose, features, target users, tech stack, and more. It serves as your "North Star" to guide development.

**Why do this first?**
- Ensures both you and the AI agent are aligned on the end goal
- Cursor can actually generate a PRD from a simple description
- Creates a reference document for the entire project

**Sample Prompt:**
```
You are a software product manager. Help me create a Product Requirements Document for a [Project Name]. Include: project purpose, user stories, technical requirements, features, and success criteria.
```

**Tip:** Save as `instructions.md` or `PRD.md` in your project root. Review and edit any inaccuracies before proceeding.

---

### 2. Set Project Rules

**Define custom Cursor rules for your tech stack.**

Cursor Rules are one of the most powerful (and underrated) features of Cursor IDE. They allow you to define custom guidelines that the AI follows when generating or modifying code.

**How to define rules:**
- Create a `.cursor/rules/` directory in your project
- Add Markdown Cursor rule files (`.mdc` extension)
- Rules can encode architectural patterns, library choices, and code style

**Example rules structure:**
```
.cursor/rules/
├── backend.fastapi.mdc    # FastAPI guidelines
├── frontend.react.mdc     # React guidelines  
└── general.mdc           # Project-wide conventions
```

**What rules can encode:**
- Architectural patterns ("All database access must go through repository classes")
- Library choices ("Use Pydantic models for request/response schemas")
- Code style ("Use snake_case for functions, PascalCase for classes")

**Resources:**
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) - Community rules repository
- [sparesparrow/cursor-rules](https://github.com/sparesparrow/cursor-rules) - Additional examples

---

### 3. Choose the Right Agent Mode (AGENT vs ASK)

**Understand when to use AGENT mode versus ASK mode.**

| Mode | Purpose | When to Use |
|------|---------|-------------|
| **Agent Mode** | Autonomous execution | When you want Cursor to implement features, create/modify files, run commands |
| **Ask Mode** | Q&A and exploration | When you need information, design discussion, or planning |

**Agent Mode:**
- Acts autonomously to execute your requests
- Can create files, edit multiple files, run commands
- Use when you want to say: "Cursor, do this for me"

**Ask Mode:**
- Read-only, won't make changes to files
- Perfect for exploring options, understanding code, planning
- Use when you want to say: "Cursor, tell me about this"

**Best Practice:**
- Start with Ask mode to discuss design
- Switch to Agent mode for implementation
- Return to Ask mode to review and plan next steps

---

### 4. Select the Best Model for the Job

**Pick an appropriate AI model for the task.**

Different models have different strengths. Cursor lets you choose which model to use.

**Model Selection Guidelines:**

| Scenario | Recommended Models |
|----------|-------------------|
| Complex tasks / Critical code | Claude-4 Sonnet, OpenAI o3, Gemini 2.5 Pro |
| Large context / Many files | Models with extended context windows (200K+ tokens) |
| Speed-sensitive work | GPT-4o or faster models |
| Cost-sensitive work | Smaller, efficient models |

**Key Considerations:**
- **Context length:** Large projects need models with extended context windows
- **Speed vs Quality:** Top models may have higher latency
- **Cost:** Most powerful models consume more credits
- **Max Mode:** Enables extended context for larger codebases

---

### 5. Use @ References in Prompts

**Provide context by referencing files, web pages, code, or terminal outputs directly in prompts.**

This is one of Cursor's killer features — the ability to inject specific context using `@` references.

**Available @ Commands:**

| Reference | Purpose | Example |
|-----------|---------|---------|
| `@File` | Include file contents | `@models.py` - Reference a specific file |
| `@Code` | Reference code symbols | `@update_task_status` - Reference a function |
| `@Web` | Pull web information | `@Web how to implement drag-and-drop in React` |
| `@Terminal` | Include terminal output | `@Terminal` - Reference recent command outputs |
| `@Git` | Reference git history | `@git` - Show recent commits or diffs |

**Example Combined Usage:**
```
Using @tasks.py and @models.py for context, implement the feature described in @instructions.md (the PRD).
```

**Tip:** You can also drag-and-drop files into chat or right-click "Add to Chat" in the file explorer.

---

### 6. Write Detailed, Precise Prompts

**Be explicit about what you want.**

Large language models do much better when you spell out exactly what you want. In coding, this means providing requirements, constraints, and context.

**Best Practices for Prompt Writing:**

1. **State objectives and constraints clearly:**
   ```
   Add a user login feature to the app. Use JWT for authentication tokens. 
   Store users in SQLite. Include email validation.
   ```

2. **Refer to specific components by name:**
   ```
   Modify the Task Pydantic model in @models.py to include a priority field 
   (High, Medium, Low). Update the API endpoints accordingly.
   ```

3. **Provide examples if needed:**
   ```
   Format the output as: Task 1 – [Done] (ID, then title, then status in brackets)
   ```

4. **Specify files to change or create:**
   ```
   Create a new file database.py for database connection logic and 
   update main.py to import and use it.
   ```

5. **Mention relevant rules or context:**
   ```
   Recall our project rule: use dependency injection for database sessions.
   ```

**The Difference:** When you say "Implement X" generically, the AI might produce code that works but ignores edge cases or doesn't follow your architecture. Detailed prompts yield accurate results.

---

### 7. Request Logging, Unit Tests, and Documentation

**Don't just ask for feature code.**

Robust software includes more than just the happy-path implementation.

**Three Things to Always Request:**

1. **Logging:**
   - Include logging statements in generated code
   - Helps diagnose issues in production and development
   - Request: "Add logging for key operations using Python's logging module"

2. **Unit Tests:**
   - Cursor is quite good at writing tests
   - Can even do test-driven development (tests before implementation)
   - Request: "Generate unit tests for the CRUD operations in tasks.py using pytest"

3. **Documentation:**
   - Docstrings for functions
   - README sections
   - Request: "Add docstrings to all public functions in Google style format"

**Definition of Done Checklist:**
- ✅ Code implemented?
- ✅ Tests written?
- ✅ Logging in place?
- ✅ Docs updated?

---

### 8. Improve Prompts Iteratively

**Treat each AI generation as a draft.**

Rarely will your first prompt yield a perfect solution. Iteration is key.

**How to Iterate Effectively:**

1. **Review the AI's output thoroughly**
   - Read it as if reviewing a teammate's pull request
   - Check if it meets PRD requirements
   - Verify style/architecture compliance

2. **Identify why issues happened**
   - Was the prompt ambiguous?
   - Was context missing?
   - Did the AI make wrong assumptions?

3. **Refine your prompt with new insights**
   - Follow-up prompts for adjustments
   - Start fresh if things went astray
   - Be more specific about what needs changing

4. **Leverage Cursor's memory**
   - Cursor remembers your corrections
   - Use this to build consistent patterns

5. **Don't be afraid to intervene manually**
   - Small edits can be done by hand
   - Tell Cursor about manual changes: "I renamed X to Y"

**Key Philosophy:** Continuous improvement. Each AI generation is a draft. Use it, test it, poke holes in it, then make the next draft better.

---

### 9. Exclude Unnecessary Files from Indexing

**Speed up Cursor and reduce confusion by ignoring irrelevant files.**

Large repositories with thousands of files can slow down the AI. Cursor automatically respects `.gitignore`, but you often need more.

**Two Configuration Files:**

| File | Behavior |
|------|----------|
| `.cursorignore` | Files completely invisible to Cursor (not indexed, cannot reference) |
| `.cursorindexignore` | Files not indexed automatically, but can reference explicitly |

**Example `.cursorignore`:**
```
# Completely ignore
__pycache__/
*.pyc
*.log
node_modules/
build/
dist/
```

**Example `.cursorindexignore`:**
```
# Don't index but keep referenceable
docs/legacy/
data/samples/
*.sql
```

**Benefits:**
- More efficient AI assistant
- Prevents hitting token limits
- Reduces latency
- **Security:** Ensures secrets aren't accidentally read by Cursor

**Verify indexing:** Use Context → Codebase Indexing view in Cursor.

---

### 10. Utilize MCP Servers (Advanced)

**For advanced users, consider hooking Cursor up to an MCP server.**

MCP (Model Context Protocol) allows Cursor to connect to external knowledge sources or services that provide additional context or capabilities.

**What MCP Can Provide:**
- Vector search over large documentation sets
- Long conversation history maintenance
- Project-specific knowledge bases
- External tool integrations

**Popular MCP Servers:**
- **Context7** - Up-to-date library documentation
- **DeepWiki** - Extended knowledge bases
- **Custom servers** - Your own documentation/context providers

**Configuration:**
MCP servers are configured in `.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

**When to Use MCP:**
- ❌ Small apps - Overkill
- ✅ Large codebases hitting context limits
- ✅ Need specialized knowledge (framework docs, company guidelines)
- ✅ Multi-service architectures with extensive docs

**Note:** MCP can incur additional costs (larger context models, external API calls). Use intentionally when benefits outweigh costs.

---

## Summary

| Practice | Key Takeaway |
|----------|-------------|
| 1. Generate PRD | Start with a clear blueprint |
| 2. Set Project Rules | Define conventions the AI follows |
| 3. Choose Agent Mode | AGENT for doing, ASK for discussing |
| 4. Select Best Model | Match model to task complexity |
| 5. Use @ References | Ground prompts with specific context |
| 6. Write Detailed Prompts | Be explicit about requirements |
| 7. Request Tests/Logs/Docs | Build robust software, not just features |
| 8. Iterate Prompts | Treat output as drafts to refine |
| 9. Exclude Unnecessary Files | Focus AI on what matters |
| 10. Utilize MCP | Extend capabilities for large projects |

---

## Related Resources

- [Cursor Documentation](https://docs.cursor.com/)
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)
- [Cursor Community Forum](https://forum.cursor.com/)
- [Context7 MCP](https://context7.com/)

---

**Last Updated:** 2025-11-26

