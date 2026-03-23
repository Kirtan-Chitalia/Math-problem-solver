import argparse
import uvicorn


def main():
    parser = argparse.ArgumentParser(description="AI Math Solver")
    
    subparsers = parser.add_subparsers(dest="command")
    
    # --- Command: serve ---
    serve_parser = subparsers.add_parser("serve", help="Start API server")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--host", type=str, default="0.0.0.0")
    
    # --- Command: solve ---
    solve_parser = subparsers.add_parser("solve", help="Solve from image")
    solve_parser.add_argument("image", type=str, help="Path to image")
    
    args = parser.parse_args()
    
    if args.command == "serve":
        uvicorn.run("src.api.app:app", host=args.host, port=args.port, reload=True)
    
    elif args.command == "solve":
        from src.agents.orchestrator import run_pipeline
        from rich.console import Console
        from rich.panel import Panel

        console = Console()
        
        with console.status("[bold green]Solving math problem...[/bold green]"):
            result = run_pipeline(args.image)
            
        console.print(f"\n[bold cyan]📝 OCR Text:[/bold cyan] {result.get('ocr_text')}")
        console.print(f"[bold magenta]📂 Problem Type:[/bold magenta] {result.get('problem_type', 'Unknown').replace('_', ' ').title()}\n")
        
        solution = result.get('llm_solution', 'No solution found.')
        console.print(Panel(solution, title="[bold yellow]🧮 Step-by-Step Solution[/bold yellow]", border_style="yellow", expand=False))
        
        verified = result.get('verification', {}).get('verified', 'N/A')
        v_color = "green" if str(verified).lower() == "true" else "red"
        console.print(f"[{v_color}]✅ Verified: [bold]{verified}[/bold][/{v_color}]\n")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
