"""
Shannon CLI Output Formatters

Provides multiple output format options for Shannon analysis results:
- JSON (for automation/API integration)
- Markdown (for documentation)
- Rich Tables (for terminal display)
- Summary (for quick one-line output)

Author: Shannon Framework
"""

from typing import Dict, Any, Optional, List
import json
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class OutputFormatter:
    """Format Shannon results in multiple output modes"""

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize the output formatter.

        Args:
            console: Optional Rich Console instance. If None, creates a new one.
        """
        self.console = console or Console()

    def format_json(self, result: Dict[str, Any], pretty: bool = True) -> str:
        """
        Output as JSON (for automation).

        Args:
            result: Shannon analysis result dictionary
            pretty: If True, format with indentation. If False, compact JSON.

        Returns:
            JSON string representation of the result

        Example:
            >>> formatter = OutputFormatter()
            >>> result = {"complexity_score": 0.68, "interpretation": "COMPLEX"}
            >>> json_output = formatter.format_json(result)
        """
        if pretty:
            return json.dumps(result, indent=2, sort_keys=False)
        return json.dumps(result, separators=(',', ':'))

    def format_markdown(self, result: Dict[str, Any]) -> str:
        """
        Output as Markdown (for docs).

        Format:
        # Complexity: 0.68 (COMPLEX)

        ## 8D Breakdown
        | Dimension | Score | Weight |
        |-----------|-------|--------|
        | Structural | 0.55 | 12% |
        ...

        Args:
            result: Shannon analysis result dictionary

        Returns:
            Markdown-formatted string

        Example:
            >>> formatter = OutputFormatter()
            >>> md_output = formatter.format_markdown(analysis_result)
            >>> print(md_output)
        """
        complexity_score = result.get('complexity_score', 0.0)
        interpretation = result.get('interpretation', 'UNKNOWN')

        md = f"# Complexity: {complexity_score:.3f} ({interpretation})\n\n"

        # 8D Breakdown section
        if 'dimension_scores' in result:
            md += "## 8D Breakdown\n\n"
            md += "| Dimension | Score | Weight |\n"
            md += "|-----------|-------|--------|\n"

            for dim, data in result['dimension_scores'].items():
                score = data.get('score', 0.0) or 0.0
                weight = data.get('weight', 0.0) or 0.0
                md += f"| {dim.capitalize()} | {score:.3f} | {weight:.0%} |\n"

            md += "\n"

        # Domain percentages section
        if 'domain_percentages' in result:
            md += "## Domain Distribution\n\n"
            md += "| Domain | Percentage |\n"
            md += "|--------|------------|\n"

            for domain, percentage in result['domain_percentages'].items():
                md += f"| {domain.capitalize()} | {percentage}% |\n"

            md += "\n"

        # Recommendations section
        if 'recommendations' in result and result['recommendations']:
            md += "## Recommendations\n\n"
            for i, rec in enumerate(result['recommendations'], 1):
                md += f"{i}. {rec}\n"
            md += "\n"

        # Warnings section
        if 'warnings' in result and result['warnings']:
            md += "## Warnings\n\n"
            for warning in result['warnings']:
                md += f"⚠️ {warning}\n"
            md += "\n"

        return md

    def format_table(self, result: Dict[str, Any]) -> Table:
        """
        Output as Rich Table (for terminal).

        Args:
            result: Shannon analysis result dictionary

        Returns:
            Rich Table object ready for console output

        Example:
            >>> formatter = OutputFormatter()
            >>> table = formatter.format_table(analysis_result)
            >>> formatter.console.print(table)
        """
        complexity_score = result.get('complexity_score', 0.0)
        interpretation = result.get('interpretation', 'UNKNOWN')

        title = f"Shannon Analysis - Complexity: {complexity_score:.3f} ({interpretation})"
        table = Table(title=title, show_header=True, header_style="bold magenta")

        table.add_column("Dimension", style="cyan", no_wrap=True)
        table.add_column("Score", justify="right", style="green")
        table.add_column("Weight", justify="right", style="yellow")

        if 'dimension_scores' in result:
            for dim, data in result['dimension_scores'].items():
                score = data.get('score', 0.0) or 0.0
                weight = data.get('weight', 0.0) or 0.0

                # Color-code scores: red for high complexity, green for low
                score_style = "red" if score > 0.7 else "yellow" if score > 0.4 else "green"
                score_text = Text(f"{score:.3f}", style=score_style)

                table.add_row(
                    dim.capitalize(),
                    score_text,
                    f"{weight:.0%}"
                )

        return table

    def format_summary(self, result: Dict[str, Any]) -> str:
        """
        One-line summary for quick display.

        Args:
            result: Shannon analysis result dictionary

        Returns:
            Compact one-line summary string

        Example:
            >>> formatter = OutputFormatter()
            >>> summary = formatter.format_summary(analysis_result)
            >>> print(summary)
            Complexity: 0.68 (COMPLEX) | Domains: structural:30%, semantic:25%, ...
        """
        complexity_score = result.get('complexity_score', 0.0)
        interpretation = result.get('interpretation', 'UNKNOWN')

        summary = f"Complexity: {complexity_score:.3f} ({interpretation})"

        if 'domain_percentages' in result:
            domains = ', '.join(
                f"{k}:{v}%"
                for k, v in result['domain_percentages'].items()
            )
            summary += f" | Domains: {domains}"

        return summary

    def format_detailed(self, result: Dict[str, Any]) -> Panel:
        """
        Create a detailed Rich Panel with full analysis information.

        Args:
            result: Shannon analysis result dictionary

        Returns:
            Rich Panel object with comprehensive analysis details

        Example:
            >>> formatter = OutputFormatter()
            >>> panel = formatter.format_detailed(analysis_result)
            >>> formatter.console.print(panel)
        """
        complexity_score = result.get('complexity_score', 0.0)
        interpretation = result.get('interpretation', 'UNKNOWN')

        content = []

        # Header
        content.append(f"[bold cyan]Complexity Score:[/bold cyan] {complexity_score:.3f}")
        content.append(f"[bold cyan]Interpretation:[/bold cyan] {interpretation}")
        content.append("")

        # Dimension scores
        if 'dimension_scores' in result:
            content.append("[bold yellow]8D Breakdown:[/bold yellow]")
            for dim, data in result['dimension_scores'].items():
                score = data.get('score', 0.0) or 0.0
                weight = data.get('weight', 0.0) or 0.0
                content.append(f"  • {dim.capitalize()}: {score:.3f} (weight: {weight:.0%})")
            content.append("")

        # Domain percentages
        if 'domain_percentages' in result:
            content.append("[bold yellow]Domain Distribution:[/bold yellow]")
            for domain, percentage in result['domain_percentages'].items():
                content.append(f"  • {domain.capitalize()}: {percentage}%")
            content.append("")

        # Recommendations
        if 'recommendations' in result and result['recommendations']:
            content.append("[bold green]Recommendations:[/bold green]")
            for rec in result['recommendations']:
                content.append(f"  • {rec}")
            content.append("")

        # Warnings
        if 'warnings' in result and result['warnings']:
            content.append("[bold red]Warnings:[/bold red]")
            for warning in result['warnings']:
                content.append(f"  ⚠️  {warning}")

        panel = Panel(
            "\n".join(content),
            title="[bold]Shannon Analysis Results[/bold]",
            border_style="blue"
        )

        return panel

    def output(
        self,
        result: Dict[str, Any],
        format_type: str = "table",
        **kwargs
    ) -> Optional[str]:
        """
        Main output method that handles all format types.

        Args:
            result: Shannon analysis result dictionary
            format_type: One of 'json', 'markdown', 'table', 'summary', 'detailed'
            **kwargs: Additional arguments passed to specific formatters

        Returns:
            Formatted string for text formats, None for Rich objects (printed directly)

        Raises:
            ValueError: If format_type is not recognized

        Example:
            >>> formatter = OutputFormatter()
            >>> formatter.output(result, format_type="json")
            >>> formatter.output(result, format_type="table")
        """
        format_type = format_type.lower()

        if format_type == "json":
            output = self.format_json(result, **kwargs)
            self.console.print(output)
            return output

        elif format_type == "markdown":
            output = self.format_markdown(result)
            self.console.print(output)
            return output

        elif format_type == "table":
            table = self.format_table(result)
            self.console.print(table)
            return None

        elif format_type == "summary":
            output = self.format_summary(result)
            self.console.print(output)
            return output

        elif format_type == "detailed":
            panel = self.format_detailed(result)
            self.console.print(panel)
            return None

        else:
            raise ValueError(
                f"Unknown format type: {format_type}. "
                f"Must be one of: json, markdown, table, summary, detailed"
            )


# Convenience function for quick formatting
def format_output(
    result: Dict[str, Any],
    format_type: str = "table",
    console: Optional[Console] = None
) -> Optional[str]:
    """
    Convenience function for quick output formatting.

    Args:
        result: Shannon analysis result dictionary
        format_type: Output format type
        console: Optional Rich Console instance

    Returns:
        Formatted string or None (if printed directly)

    Example:
        >>> from shannon.ui.formatters import format_output
        >>> format_output(analysis_result, format_type="json")
    """
    formatter = OutputFormatter(console=console)
    return formatter.output(result, format_type=format_type)
