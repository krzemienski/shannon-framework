"""
Example 1: Basic Wave Orchestration with Automatic Detection
============================================================

Demonstrates Shannon's automatic wave spawning based on complexity detection.
Shows how a simple task triggers wave orchestration when complexity exceeds 0.7 threshold.
"""

import asyncio
import sys
from pathlib import Path

# Add Shannon to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.orchestrator import (
    WaveOrchestrator,
    ComplexityAnalyzer,
    OrchestrationDecision
)


async def main():
    """Demonstrate automatic wave orchestration."""

    # ========================================================================
    # STEP 1: Initialize orchestrator
    # ========================================================================
    config = {
        'complexity_threshold': 0.7,
        'max_concurrent_agents': 10
    }

    orchestrator = WaveOrchestrator(config)
    print("="*70)
    print("Shannon Framework v2.1 - Basic Wave Orchestration")
    print("="*70)
    print(f"Complexity Threshold: {config['complexity_threshold']}")
    print(f"Max Agents: {config['max_concurrent_agents']}")
    print()

    # ========================================================================
    # STEP 2: Define a moderately complex task
    # ========================================================================
    task = {
        'description': 'Refactor authentication system across microservices',
        'scope_indicators': {
            'file_count': 25,
            'dir_count': 8,
            'line_count': 6000
        },
        'operations': [
            {'type': 'refactor'},
            {'type': 'test'},
            {'type': 'validate'}
        ],
        'domains': ['backend', 'security', 'infrastructure'],
        'dependencies': ['jwt-lib', 'oauth2', 'redis', 'postgres'],
        'external_dependencies': ['auth0', 'keycloak'],
        'parallel_opportunities': 5,
        'sequential_dependencies': 2,
        'risk_indicators': {
            'production_impact': True,
            'security_impact': True,
            'reversibility': False
        }
    }

    print("Task Definition:")
    print(f"  Description: {task['description']}")
    print(f"  Files: {task['scope_indicators']['file_count']}")
    print(f"  Directories: {task['scope_indicators']['dir_count']}")
    print(f"  Operations: {len(task['operations'])}")
    print(f"  Domains: {len(task['domains'])}")
    print()

    # ========================================================================
    # STEP 3: Analyze complexity (8 dimensions)
    # ========================================================================
    print("Analyzing 8-Dimensional Complexity...")
    print("-" * 70)

    decision = await orchestrator.analyze_and_decide(task)

    complexity = decision.complexity
    print(f"Scope:         {complexity.scope:.3f}")
    print(f"Dependencies:  {complexity.dependencies:.3f}")
    print(f"Operations:    {complexity.operations:.3f}")
    print(f"Domains:       {complexity.domains:.3f}")
    print(f"Concurrency:   {complexity.concurrency:.3f}")
    print(f"Uncertainty:   {complexity.uncertainty:.3f}")
    print(f"Risk:          {complexity.risk:.3f}")
    print(f"Scale:         {complexity.scale:.3f}")
    print()
    print(f"TOTAL COMPLEXITY: {complexity.total:.3f}")
    print(f"Threshold Exceeded: {complexity.threshold_exceeded}")
    print()

    # ========================================================================
    # STEP 4: Display orchestration decision
    # ========================================================================
    print("Orchestration Decision:")
    print("-" * 70)
    print(f"Should Orchestrate: {decision.should_orchestrate}")
    print(f"Strategy: {decision.recommended_strategy.value}")
    print(f"Agent Count: {decision.recommended_agent_count}")
    print()

    print("Reasoning:")
    for reason in decision.reasoning:
        print(f"  • {reason}")
    print()

    if decision.warnings:
        print("Warnings:")
        for warning in decision.warnings:
            print(f"  ⚠️  {warning}")
        print()

    # ========================================================================
    # STEP 5: Show what would happen
    # ========================================================================
    if decision.should_orchestrate:
        print("Automatic Wave Orchestration ACTIVATED")
        print("Wave would spawn with:")
        print(f"  • Strategy: {decision.recommended_strategy.value}")
        print(f"  • Agents: {decision.recommended_agent_count}")
        print(f"  • Phases: Review → Plan → Implement → Validate")
    else:
        print("Single-agent execution recommended (complexity below threshold)")

    print()
    print("="*70)
    print("Example Complete!")
    print("="*70)

    # Cleanup
    await orchestrator.cleanup()


# ============================================================================
# EXPECTED OUTPUT:
# ============================================================================
"""
======================================================================
Shannon Framework v2.1 - Basic Wave Orchestration
======================================================================
Complexity Threshold: 0.7
Max Agents: 10

Task Definition:
  Description: Refactor authentication system across microservices
  Files: 25
  Directories: 8
  Operations: 3
  Domains: 3

Analyzing 8-Dimensional Complexity...
----------------------------------------------------------------------
Scope:         0.550
Dependencies:  0.600
Operations:    0.750
Domains:       0.500
Concurrency:   0.457
Uncertainty:   0.000
Risk:          0.900
Scale:         0.000

TOTAL COMPLEXITY: 0.720
Threshold Exceeded: True

Orchestration Decision:
----------------------------------------------------------------------
Should Orchestrate: True
Strategy: validation
Agent Count: 5

Reasoning:
  • Complexity 0.720 exceeds threshold 0.7
  • Selected strategy: validation
  • Recommended agents: 5

Warnings:
  ⚠️  High risk detected - validation strategy recommended

Automatic Wave Orchestration ACTIVATED
Wave would spawn with:
  • Strategy: validation
  • Agents: 5
  • Phases: Review → Plan → Implement → Validate

======================================================================
Example Complete!
======================================================================
"""


if __name__ == '__main__':
    asyncio.run(main())