# Shannon Framework v2.1 - Working Examples

Complete set of executable Python examples demonstrating Shannon's core capabilities with **real outputs**.

## Prerequisites

```bash
# Install Shannon framework
cd /Users/nick/Documents/shannon
pip install -e .

# Required dependencies (should be installed automatically)
# - numpy>=1.24.0
# - asyncio (built-in Python 3.7+)
```

## Examples Overview

### 1️⃣ Basic Wave Orchestration (`01_basic_orchestration.py`)

**What it demonstrates:**
- Automatic complexity detection (8 dimensions)
- Wave orchestration triggering when complexity exceeds 0.7
- Strategy selection based on task characteristics
- Agent count recommendation

**Key concepts:**
- Scope analysis (files, directories, lines)
- Dependency complexity
- Operation type classification
- Risk and uncertainty scoring
- Automatic wave spawning

**Run it:**
```bash
cd examples
python 01_basic_orchestration.py
```

**Expected output:**
- Complexity scores across 8 dimensions
- Total complexity: 0.720 (exceeds 0.7 threshold)
- Recommendation: `validation` strategy with 5 agents
- Warning about high risk detected

**Use cases:**
- Understanding when Shannon auto-spawns waves
- Tuning complexity thresholds for your projects
- Analyzing task complexity before execution

---

### 2️⃣ Manual Checkpoint Management (`02_manual_checkpoints.py`)

**What it demonstrates:**
- Real-time token usage monitoring
- 4-level alert system (GREEN → YELLOW → ORANGE → RED)
- Manual checkpoint creation with context preservation
- Serena MCP memory key tracking
- Checkpoint restoration instructions

**Key concepts:**
- Alert thresholds: 60%, 75%, 85%, 95%
- Context snapshots with full state
- Serena key references for memory persistence
- Wave state preservation
- Recovery instructions generation

**Run it:**
```bash
cd examples
python 02_manual_checkpoints.py
```

**Expected output:**
- Initial state: 0 tokens, GREEN alert
- After analysis: 50K tokens (25%), GREEN alert
- After implementation: 130K tokens (65%), YELLOW alert with recommendations
- After testing: 180K tokens (90%), RED alert with warnings
- 2 checkpoints created with full restoration instructions

**Use cases:**
- Managing context in long sessions
- Creating recovery points before risky operations
- Debugging context usage issues
- Planning checkpoint strategies

---

### 3️⃣ Quantum Superposition (`03_quantum_exploration.py`)

**What it demonstrates:**
- Quantum-inspired parallel universe exploration
- Multiple solution approaches in superposition
- Probability amplitude calculation (Born rule)
- Quantum interference between similar solutions
- Collapse to best solution

**Key concepts:**
- Parallel execution with `asyncio.gather()`
- Complex amplitude with phase
- Probability = |amplitude|²
- Constructive and destructive interference
- Entanglement between related solutions

**Run it:**
```bash
cd examples
python 03_quantum_exploration.py
```

**Expected output:**
- 5 parallel universes explored in ~65ms
- Quantum states with amplitudes and probabilities
- Best solution: "Batch Processing" (88.9% probability)
- Interference events: 1
- Quantum coherence: 0.842
- Top 3 alternatives ranked by probability

**Use cases:**
- Exploring multiple implementation strategies in parallel
- Probability-weighted solution selection
- Performance optimization with multiple approaches
- A/B testing with quantum semantics

---

### 4️⃣ Agent Evolution (`04_agent_evolution.py`)

**What it demonstrates:**
- Agent DNA creation with 7 gene types
- Genetic algorithm evolution over 5 generations
- Multi-objective fitness evaluation
- Crossover and mutation mechanisms
- Performance improvement tracking

**Key concepts:**
- 7 gene types: tool_preference, mcp_affinity, parallelism, memory_tier, error_strategy, topology, optimization
- Tournament selection for parents
- Uniform/single-point/two-point crossover
- Adaptive mutation based on diversity
- Elite preservation (top 20%)
- Fitness = 35% speed + 40% quality + 25% resources

**Run it:**
```bash
cd examples
python 04_agent_evolution.py
```

**Expected output:**
- Generation 0: Random population, best fitness 0.534
- Generation 1: Best fitness 0.612 (+14.6%)
- Generation 2: Best fitness 0.687 (+12.3%)
- Generation 3: Best fitness 0.743 (+8.1%)
- Generation 4: Best fitness 0.798 (+7.4%)
- **Total improvement: 49.4% over 5 generations**
- Champion agent with optimized gene configuration

**Use cases:**
- Optimizing agent configurations for specific tasks
- Understanding genetic algorithm mechanics
- Tracking performance improvements across generations
- Building adaptive agent populations

---

## Running All Examples

```bash
cd examples

# Run each example sequentially
for example in 01_*.py 02_*.py 03_*.py 04_*.py; do
    echo "Running $example..."
    python "$example"
    echo
done
```

## Example Output Directory Structure

```
shannon/
├── examples/
│   ├── README.md                    # This file
│   ├── 01_basic_orchestration.py   # Wave auto-spawning
│   ├── 02_manual_checkpoints.py    # Context management
│   ├── 03_quantum_exploration.py   # Quantum superposition
│   └── 04_agent_evolution.py       # Genetic algorithms
└── src/
    ├── core/
    │   ├── orchestrator.py          # Used in example 01
    │   └── wave_config.py
    ├── memory/
    │   └── context_monitor.py       # Used in example 02
    ├── quantum/
    │   └── superposition_engine.py  # Used in example 03
    └── agents/
        └── dna.py                   # Used in example 04
```

## Key Takeaways

### From Example 1 (Orchestration):
- Complexity ≥0.7 → automatic wave spawning
- 8 dimensions analyzed: scope, deps, ops, domains, concurrency, uncertainty, risk, scale
- Strategy selection: progressive, systematic, adaptive, enterprise, validation

### From Example 2 (Checkpoints):
- GREEN (0-60%): Normal operation
- YELLOW (60-75%): Optimize and cache
- ORANGE (75-85%): Defer non-critical ops
- RED (85-95%): Force efficiency, create checkpoints
- Serena keys enable cross-session context restoration

### From Example 3 (Quantum):
- True parallel execution with asyncio
- Probability amplitudes weight solutions
- Interference eliminates similar approaches
- Born rule selects best by probability
- Coherence measures phase alignment

### From Example 4 (Evolution):
- Agents evolve over generations
- Fitness = speed + quality + resources
- Crossover combines parent genes
- Mutation explores new configurations
- Elite preservation keeps best agents

## Troubleshooting

### Import errors:
```bash
# Ensure Shannon is installed
pip install -e /Users/nick/Documents/shannon
```

### Missing dependencies:
```bash
pip install numpy>=1.24.0
```

### Slow execution:
- Examples use `asyncio.sleep()` to simulate work
- Real Shannon operations are much faster
- Adjust sleep durations in examples if needed

## Next Steps

1. **Modify examples**: Change parameters and observe behavior
2. **Build your own**: Use examples as templates for custom agents
3. **Integrate**: Import Shannon modules into your projects
4. **Extend**: Add new gene types, strategies, or quantum operations

## Questions?

- Read framework documentation: `/docs/`
- Check integration guides: `/docs/integration/`
- Review API reference: `/docs/api/`
- See architecture overview: `/docs/architecture.md`

---

**Shannon Framework v2.1** - Multi-agent orchestration with quantum-inspired parallelism and genetic evolution.