# MCP-A2A: (Agent > Tools) × (Agent > Tools)

> **The Tool-Augmented Multi-Agent Architecture for Real-World AI Engineering.**  
> *Stop letting LLMs talk in speculative prompt loops. Ground every agent with isolated Model Context Protocol (MCP) tools and enforce contract-driven evidence handover.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Protocol: MCP](https://img.shields.io/badge/Protocol-MCP%20JSON--RPC-orange.svg)](https://modelcontextprotocol.io)
[![Architecture: Clean--Room](https://img.shields.io/badge/Pattern-Clean--Room%20Synthesis-purple.svg)]()

---

## The Flaw of Pure "Agent-to-Agent" (A2A)

The industry is full of demos showing "Agent-to-Agent" (A2A) communication where multiple LLMs chat with each other in natural language:

```
[Agent A (Researcher)]  ── "I think the auth function uses AES-256" ──►  [Agent B (Coder)]
[Agent A (Researcher)]  ◄── "Are you sure? What's the IV?" ───────────  [Agent B (Coder)]
[Agent A (Researcher)]  ── "Yes, probably standard IV of zeros" ──────►  [Agent B (Coder)]
```

**Why pure A2A collapses in production:**
1. **Compounding Hallucinations:** When Agent A speculates, Agent B treats that speculation as fact and builds upon it. Error rates grow exponentially.
2. **Context Window Bloat:** Unstructured back-and-forth chat consumes hundreds of thousands of tokens without producing a single byte of verifiable code.
3. **Zero Grounding:** Agents have opinions, not evidence. No real side effects occur.

---

## The Solution: MCP-A2A

In **MCP-A2A**, agents never pass conversational opinions. Every agent is strictly augmented with isolated **Model Context Protocol (MCP)** tools:

$$\mathbf{(Agent_A \rightarrow Tools_A) \iff (Agent_B \rightarrow Tools_B)}$$

```
┌─────────────────────────────────┐                 ┌─────────────────────────────────┐
│        INSPECTOR AGENT          │                 │          BUILDER AGENT          │
│   (Domain: Binary Forensics)    │                 │    (Domain: Clean Implementation)│
├─────────────────────────────────┤                 ├─────────────────────────────────┤
│       ISOLATED MCP TOOLS:       │                 │       ISOLATED MCP TOOLS:       │
│  • rea_extract_symbols          │                 │  • fs_write_file                │
│  • rea_decompile_procedure      │                 │  • fs_read_file                 │
│  • rea_analyze_control_flow     │                 │  • runtime_run_test             │
└────────────────┬────────────────┘                 └────────────────▲────────────────┘
                 │                                                   │
                 │          TYPED EVIDENCE ENVELOPE                  │
                 │      (Cryptographically Hashed Facts)             │
                 └───────────────────────────────────────────────────┘
```

1. **Agent A** uses its local MCP tools (e.g. `rea` decompilation, network packet triage, static analysis).
2. It packages its findings into a structured **Evidence Envelope** backed by exact tool execution hashes.
3. **Agent B** consumes the evidence envelope (without having access to Agent A's heavy tools or binary blobs) and invokes its own MCP tools (compiler, filesystem, unit test runner) to deliver a verified, working deliverable.

---

## Architecture in Action: Clean-Room Reverse Engineering

A prime example is combining **[morluto/rea](https://github.com/morluto/rea)** with clean-room software development:

* **Step 1 (Inspector Agent):** Calls REA MCP tools on a native binary target (`/usr/bin/legacy_auth_service`). Recovers symbol trees, control flow graphs, and algorithmic constants.
* **Step 2 (The Boundary):** Strips proprietary binary assembly. Packs the mathematical formula into a typed `EvidenceEnvelope`.
* **Step 3 (Builder Agent):** Reads the clean mathematical specification. Writes clean Python/TypeScript code and executes an automated unit-test suite to verify correctness.

---

## Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/emsabiq-alt/mcp-a2a.git
cd mcp-a2a
```

### 2. Run the Interactive Pipeline
```bash
python demo.py
```

### 3. Run Automated Tests
```bash
python -m unittest discover -s tests
```

---

## Execution Output Example

```
======================================================================
🌟 INITIATING MCP-A2A PIPELINE: (Agent > Tools) × (Agent > Tools)
======================================================================
[BinaryInspector] 🔍 Inspecting target binary: /usr/bin/legacy_auth_service for symbol: _compute_request_signature...
[BinaryInspector] ✅ Evidence envelope generated with 3 backing tool execution records.
[ProductionBuilder] 📥 Received Evidence Envelope from BinaryInspector...
[ProductionBuilder] 📋 Target Feature: Request Signature Algorithm
[ProductionBuilder] 🔬 Algorithm: Modified DJB2 Hash with XOR Mask
[ProductionBuilder] 🚀 Implementation verified via test runner: PASSED
======================================================================
✨ PIPELINE COMPLETE: Production-grade artifact delivered with zero hallucination.
======================================================================

📦 EVIDENCE ENVELOPE SUMMARY:
- Producer: BinaryInspector
- Consumer: ProductionBuilder
- Evidence Records Count: 3
  * [f6aadffdd7d46c77] rea_extract_symbols
  * [a4f7064029834908] rea_decompile_procedure
  * [7789fe7f964414c0] rea_analyze_control_flow

🛠️ BUILD RESULT:
- Status: SUCCESS
- Generated Artifact: ./workspace/signature.py
- Verification Suite: PASSED
```

---

## Comparison: Pure A2A vs. MCP-A2A

| Feature | Pure A2A (Conversational) | MCP-A2A (Tool-Augmented) |
| :--- | :--- | :--- |
| **Communication Medium** | Raw Unstructured Natural Language | Typed JSON Evidence Envelopes |
| **Tool Execution** | Vague or Shared Flat Context | Domain-Isolated MCP Catalogs |
| **Hallucination Risk** | High (Exponential Compounding) | Zero (Grounded in Verified Tool Output) |
| **Separation of Concerns** | Weak (All agents know everything) | Strict (Least Privilege Architecture) |
| **Verification Gate** | "Looks good to me" (Subjective LLM) | Automated Unit Tests / Compiler Execution |

---

## License

MIT License. Designed and built by Muhammad Sabiq with Hermes Agent.
Contribute, fork, and star if you believe in grounded AI engineering!
