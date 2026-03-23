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
        result = run_pipeline(args.image)
        print(f"📝 OCR: {result.get('ocr_text')}")
        print(f"📂 Type: {result.get('problem_type')}")
        print(f"🧮 Solution:\n{result.get('llm_solution', 'N/A')}")
        print(f"✅ Verified: {result.get('verification', {}).get('verified', 'N/A')}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
