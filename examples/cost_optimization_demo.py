#!/usr/bin/env python3
"""Demonstration of Shannon CLI V3 cost optimization features.

This script demonstrates the complete cost optimization pipeline:
- Smart model selection based on complexity
- Pre-execution cost estimation
- Budget enforcement
- Achieving 30-50% cost savings
"""

from shannon.optimization import ModelSelector, CostEstimator, BudgetEnforcer


def demo_model_selection():
    """Demonstrate smart model selection."""
    print("=" * 70)
    print("MODEL SELECTION DEMONSTRATION")
    print("=" * 70)
    print()

    selector = ModelSelector()

    # Example agents with varying complexity
    test_cases = [
        {
            'name': 'Config Writer',
            'complexity': 0.25,
            'context_size': 12000,
            'estimated_tokens': 20000
        },
        {
            'name': 'Test Creator',
            'complexity': 0.35,
            'context_size': 18000,
            'estimated_tokens': 30000
        },
        {
            'name': 'Backend Builder',
            'complexity': 0.65,
            'context_size': 45000,
            'estimated_tokens': 60000
        },
        {
            'name': 'Architecture Analyzer',
            'complexity': 0.80,
            'context_size': 250000,  # Large context
            'estimated_tokens': 100000
        }
    ]

    print("Agent Analysis:")
    print("-" * 70)
    for agent in test_cases:
        result = selector.select_optimal_model(
            agent_complexity=agent['complexity'],
            context_size_tokens=agent['context_size'],
            budget_remaining=50.00,
            estimated_tokens=agent['estimated_tokens']
        )

        print(f"\n{agent['name']}:")
        print(f"  Complexity: {agent['complexity']} ({_complexity_label(agent['complexity'])})")
        print(f"  Context: {agent['context_size']/1000:.0f}K tokens")
        print(f"  Model: {result.model}")
        print(f"  Reason: {result.reason}")
        print(f"  Cost: ${result.estimated_cost:.4f}")
        if result.savings_vs_sonnet > 0:
            print(f"  Savings: ${result.savings_vs_sonnet:.4f} vs sonnet")


def demo_wave_savings():
    """Demonstrate wave cost savings with optimization."""
    print("\n" + "=" * 70)
    print("WAVE COST OPTIMIZATION DEMONSTRATION")
    print("=" * 70)
    print()

    selector = ModelSelector()

    # Realistic wave with mixed complexity agents
    wave_agents = [
        {'complexity': 0.70, 'context_size': 50000, 'estimated_tokens': 70000},  # Complex
        {'complexity': 0.25, 'context_size': 15000, 'estimated_tokens': 20000},  # Simple
        {'complexity': 0.30, 'context_size': 20000, 'estimated_tokens': 30000},  # Simple
        {'complexity': 0.45, 'context_size': 30000, 'estimated_tokens': 40000},  # Moderate
        {'complexity': 0.65, 'context_size': 40000, 'estimated_tokens': 55000},  # Complex
    ]

    print("Wave 1: Foundation (5 agents)")
    print("-" * 70)
    print()

    savings = selector.estimate_wave_savings(wave_agents)

    print("Cost Comparison:")
    print(f"  Original (all sonnet): ${savings['original_cost']:.2f}")
    print(f"  Optimized (smart selection): ${savings['optimized_cost']:.2f}")
    print(f"  Savings: ${savings['savings_usd']:.2f} ({savings['savings_percent']:.0f}%)")
    print()

    print("Model Selections:")
    for idx, model, reason in savings['model_selections']:
        agent = wave_agents[idx]
        print(f"  Agent {idx+1} (complexity {agent['complexity']:.2f}): {model}")


def demo_budget_enforcement():
    """Demonstrate budget enforcement and tracking."""
    print("\n" + "=" * 70)
    print("BUDGET ENFORCEMENT DEMONSTRATION")
    print("=" * 70)
    print()

    # Set up budget enforcer
    enforcer = BudgetEnforcer(budget_limit=15.00)
    estimator = CostEstimator()

    print(f"Budget Limit: ${enforcer.budget_limit:.2f}")
    print()

    # Simulate operations
    operations = [
        ('spec-analysis', 1500, None),
        ('wave-1', [
            {'complexity': 0.65, 'context_size': 45000, 'estimated_tokens': 60000},
            {'complexity': 0.25, 'context_size': 12000, 'estimated_tokens': 20000}
        ], None),
        ('wave-2', [
            {'complexity': 0.55, 'context_size': 35000, 'estimated_tokens': 50000},
            {'complexity': 0.30, 'context_size': 18000, 'estimated_tokens': 25000},
            {'complexity': 0.40, 'context_size': 25000, 'estimated_tokens': 35000}
        ], None)
    ]

    for op_name, op_data, _ in operations:
        print(f"Operation: {op_name}")
        print("-" * 70)

        # Estimate cost
        if op_name == 'spec-analysis':
            estimate = estimator.estimate_spec_analysis(spec_size_lines=op_data)
        else:
            estimate = estimator.estimate_wave_cost(op_data)

        # Check budget
        check = enforcer.pre_execution_check(op_name, estimate.estimated_cost_usd)

        print(f"  Estimated Cost: ${estimate.estimated_cost_usd:.2f}")
        print(f"  Budget Remaining: ${check['remaining_before']:.2f}")

        if check['allowed']:
            print(f"  Status: ✓ Allowed (remaining after: ${check['remaining_after']:.2f})")
            enforcer.record_operation(op_name, estimate.estimated_cost_usd, estimate.model, estimate.estimated_tokens)
        else:
            print(f"  Status: ✗ Blocked (would exceed budget by ${abs(check['remaining_after']):.2f})")
            print("\n  Suggestions:")
            suggestions = enforcer.suggest_optimizations(estimate.estimated_cost_usd, estimate.model)
            for suggestion in suggestions:
                print(f"    - {suggestion}")

        print()

    # Final summary
    summary = enforcer.get_spending_summary()
    print("Final Budget Summary:")
    print("-" * 70)
    print(f"  Total Spent: ${summary['total_spent']:.2f}")
    print(f"  Remaining: ${summary['remaining']:.2f}")
    print(f"  Operations: {summary['operation_count']}")
    print()
    print("  Spending by Model:")
    for model, cost in summary['by_model'].items():
        print(f"    {model}: ${cost:.2f}")


def demo_cost_estimation():
    """Demonstrate cost estimation accuracy."""
    print("\n" + "=" * 70)
    print("COST ESTIMATION DEMONSTRATION")
    print("=" * 70)
    print()

    estimator = CostEstimator()

    # Spec analysis
    print("Spec Analysis Estimates:")
    print("-" * 70)
    for size, complexity in [(500, 0.30), (1500, 0.60), (3000, 0.80)]:
        estimate = estimator.estimate_spec_analysis(size, complexity)
        print(f"  {size} lines (complexity {complexity:.2f}): ${estimate.estimated_cost_usd:.2f} "
              f"({estimate.estimated_tokens} tokens, {estimate.confidence} confidence)")
    print()

    # Context reuse benefits
    print("Context Reuse Impact:")
    print("-" * 70)
    agents = [
        {'complexity': 0.50, 'context_size': 50000, 'estimated_tokens': 50000},
        {'complexity': 0.50, 'context_size': 50000, 'estimated_tokens': 50000}
    ]

    for reuse_type in ['different_project', 'sequential_waves', 'same_wave']:
        estimate = estimator.estimate_wave_cost(agents, context_reuse=reuse_type)
        print(f"  {reuse_type}: ${estimate.estimated_cost_usd:.2f} "
              f"({estimate.estimated_tokens} tokens)")
    print()


def _complexity_label(complexity: float) -> str:
    """Get human-readable complexity label."""
    if complexity < 0.30:
        return "simple"
    elif complexity < 0.60:
        return "moderate"
    else:
        return "complex"


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("SHANNON CLI V3 - COST OPTIMIZATION DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demonstration shows:")
    print("  1. Smart model selection (haiku vs sonnet)")
    print("  2. Wave cost savings (30-50% reduction)")
    print("  3. Budget enforcement and tracking")
    print("  4. Pre-execution cost estimation")
    print()

    demo_model_selection()
    demo_wave_savings()
    demo_cost_estimation()
    demo_budget_enforcement()

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  - Smart model selection saves 30-50% on typical waves")
    print("  - Simple agents (complexity < 0.30) use haiku (80% cheaper)")
    print("  - Complex agents (complexity >= 0.60) use sonnet for quality")
    print("  - Budget enforcement prevents overspending")
    print("  - Context reuse reduces costs for sequential operations")
    print()


if __name__ == '__main__':
    main()
