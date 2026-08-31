"""Interactive demo: doctor types patient info, agent responds in real-time."""

from __future__ import annotations

import logging

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.prompt import Prompt

app = typer.Typer()
console = Console()


@app.command()
def demo(
    model: str = typer.Option("Qwen/Qwen3-32B", help="Orchestrator model name"),
    base_url: str = typer.Option("http://localhost:8000/v1", help="LLM API base URL"),
    api_key: str = typer.Option("not-needed", help="API key"),
    enable_rules: bool = typer.Option(True, help="Enable hospital rules"),
    rules_dir: str = typer.Option("config/hospital_rules", help="Hospital rules directory"),
) -> None:
    """Interactive NeuroAgent demo for presentations and debugging."""
    logging.basicConfig(
        level=logging.WARNING,
        handlers=[RichHandler(console=console)],
    )

    from neuroagent.agent.orchestrator import AgentConfig, AgentOrchestrator
    from neuroagent.tools.tool_registry import ToolRegistry
    from neuroagent.rules.rules_engine import RulesEngine

    config = AgentConfig(base_url=base_url, api_key=api_key, model=model)

    rules_engine = None
    if enable_rules:
        rules_engine = RulesEngine(rules_dir)

    # In demo mode, tools return "not available" since there's no mock case loaded
    tool_registry = ToolRegistry.create_default_registry(mock_server=None)

    agent = AgentOrchestrator(
        config=config,
        tool_registry=tool_registry,
        rules_engine=rules_engine,
    )

    console.print(Panel(
        "[bold]NeuroAgent Interactive Demo[/bold]\n\n"
        "Enter patient information and the agent will reason through the case.\n"
        "Note: In demo mode without a loaded case, tool calls will return 'not available'.\n"
        "For full evaluation, use run_single_case.py with a NeuroBench case file.\n\n"
        "Type 'quit' to exit.",
        border_style="blue",
    ))

    while True:
        patient_info = Prompt.ask("\n[bold]Patient Info[/bold]")
        if patient_info.lower() in ("quit", "exit", "q"):
            break

        console.print("\n[dim]Running agent...[/dim]\n")
        trace = agent.run(patient_info=patient_info)

        for i, turn in enumerate(trace.turns):
            is_last_turn = i == len(trace.turns) - 1
            if turn.role == "assistant" and turn.content:
                if is_last_turn and not turn.tool_calls and trace.final_response:
                    continue
                console.print(Panel(turn.content, title="Agent"))
            if turn.tool_calls:
                for tc in turn.tool_calls:
                    console.print(f"  [cyan]→ Tool Call:[/cyan] {tc}")
            if turn.tool_results:
                for tr in turn.tool_results:
                    console.print(f"  [green]← Result:[/green] {tr}")

        if trace.final_response:
            console.print(Panel(trace.final_response, title="Assessment", border_style="green"))

    console.print("[dim]Goodbye.[/dim]")


if __name__ == "__main__":
    app()
