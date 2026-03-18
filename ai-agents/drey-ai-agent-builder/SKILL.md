---
name: ai-agent-builder
description: |
  9-step framework for building production-ready AI agents from scratch.
  Use when users want to create AI agents, automate with AI, or build multi-agent systems.
  Keywords: agent, ai, automation, llm, workflow, tool use, multi-agent
---

# AI Agent Builder

Build production-ready AI agents using the 9-step framework.

## When to Use

- User wants to automate a task with AI
- User asks "build me an agent for X"
- User wants multi-agent systems
- User needs AI with memory or tool access
- User wants to understand agent architecture

## The 9-Step Framework

### Step 1: Define Role and Goal (Always Start Here)
Answer these questions:
- What will your agent do? (one sentence)
- Who is it helping? (specific user type)
- What output will it generate?

**Template:**
```
AGENT NAME: [Name]
PURPOSE: [One sentence]
USER: [Who uses this]
INPUT: [What it receives]
OUTPUT: [What it produces]
```

### Step 2: Design Structured I/O
Use schemas for consistency:
- Input schema (what agent receives)
- Output schema (what agent returns)
- Use Pydantic, Zod, or JSON Schema

### Step 3: Prompt and Tune (Spend 80% of time here)
System prompt structure:
```
You are [ROLE] that helps [USER TYPE] achieve [GOAL].

Your expertise includes:
- [Domain knowledge]
- [Specific skill]

When given [INPUT], you:
1. [Step 1]
2. [Step 2]

Your outputs are:
- [Quality 1]
- [Quality 2]

You never:
- [Anti-pattern 1]
- [Anti-pattern 2]
```

### Step 4: Add Reasoning and Tools
- **ReAct**: Think → Act → Observe → Repeat
- **Chain-of-Thought**: Break complex problems into steps
- **Tools**: Search, code execution, APIs, file operations

### Step 5: Multi-Agent Logic (Only if needed)
Patterns:
- Planner → Executor
- Researcher → Synthesizer
- Creator → Critic → Creator

### Step 6: Memory/RAG (Only if needed)
- Conversational: Message history
- Summary: Key facts across sessions
- Vector: Search knowledge bases

### Step 7: Voice/Vision (Only if needed)
- Text-to-speech, speech-to-text
- Image understanding, generation

### Step 8: Output Format
Ensure outputs are:
- Human-readable
- Machine-parseable
- Ready for next step

### Step 9: UI/API Wrapper (Only if deploying)
- Gradio for demos
- FastAPI for production
- Streamlit for data apps

## Required Steps by Agent Type

| Agent Type | Steps Needed |
|------------|--------------|
| Simple automation | 1, 2, 3 |
| Tool-using agent | 1, 2, 3, 4 |
| Knowledge-based | 1, 2, 3, 4, 6 |
| Multi-agent | 1, 2, 3, 4, 5 |
| Full product | 1, 2, 3, 4, 6, 8, 9 |

## Output Format

When building agents, provide:
1. **Agent Definition** (Step 1)
2. **Input/Output Schemas** (Step 2)
3. **System Prompt** (Step 3)
4. **Tool Definitions** (if needed)
5. **Implementation Code**
6. **Test Cases**

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Over-engineering | Start with Steps 1-3 |
| Vague prompts | Be specific about role, process, output |
| No structured output | Always define schemas |
| Too many tools | Add one at a time, test each |
| Skipping testing | Test with edge cases |

## Key Insight

**Most powerful agents are simple agents with excellent prompts.** The magic isn't in complex architecture—it's in clear instructions.
