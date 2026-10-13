# MCP-A2A Architecture Specification

**Status:** Draft / RFC-001  
**Author:** Muhammad Sabiq & Hermes Agent  
**Domain:** Autonomous Multi-Agent Systems & Tool Orchestration  

---

## 1. Abstract

Conventional multi-agent paradigms ("A2A" or Agent-to-Agent) rely on ungrounded conversational loops where LLMs exchange natural language prompts. This introduces severe degradation modes: compounding hallucination, context saturation, and lack of deterministic side effects.

**MCP-A2A** introduces a contract-driven architecture:
$$\mathbf{(Agent_A \rightarrow Tools_A) \iff (Agent_B \rightarrow Tools_B)}$$

Every agent is bound to a scoped **Model Context Protocol (MCP)** tool catalog. Inter-agent communication is forbidden from transmitting speculative natural language; instead, agents must exchange **Evidence Envelopes** backed by cryptographic hashes of actual tool execution records.

---

## 2. Core Axioms

### Axiom 1: No Unbacked Claims
An agent may not assert a factual finding to another agent unless that finding cites at least one verified tool execution record in its payload.

### Axiom 2: Tool Isolation (Least Privilege)
Tools are partitioned strictly by domain. An agent specialized in binary disassembly cannot access compiler or deployment tools; a builder agent cannot access raw system introspection tools.

### Axiom 3: Clean-Room Boundary
When extracting logic from legacy or proprietary artifacts (e.g. reverse engineering via tools like `rea`), the inspector produces a declarative mathematical specification envelope. The builder produces clean source code without ever accessing the binary source directly.

---

## 3. Protocol Envelope Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EvidenceEnvelope",
  "type": "object",
  "properties": {
    "task_id": { "type": "string" },
    "producer_agent": { "type": "string" },
    "consumer_agent": { "type": "string" },
    "evidence_type": { "type": "string" },
    "claims": { "type": "object" },
    "backing_tool_records": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "tool_name": { "type": "string" },
          "arguments": { "type": "object" },
          "output": { "type": "any" },
          "timestamp": { "type": "number" },
          "execution_hash": { "type": "string" }
        },
        "required": ["tool_name", "arguments", "output", "execution_hash"]
      }
    }
  },
  "required": ["task_id", "producer_agent", "consumer_agent", "claims", "backing_tool_records"]
}
```

---

## 4. Lifecycle Stages

1. **Introspection Phase:** Producer Agent executes local MCP tools to observe environment, binary, or API state.
2. **Envelope Synthesis:** Producer packages raw data into normalized claims and seals backing execution records.
3. **Transmission & Validation:** Consumer Agent verifies execution record hashes before accepting state.
4. **Action & Verification Phase:** Consumer executes its own isolated MCP tools to produce verified real-world artifacts (tests, builds, PRs).
