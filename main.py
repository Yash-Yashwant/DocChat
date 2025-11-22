import argparse
import sys
from src.ingestion import ingest_pdf
from src.graph import graph

def main():
    parser = argparse.ArgumentParser(description="DocChat RAG Application")
    parser.add_argument("--ingest", type=str, help="Path to PDF file to ingest")
    parser.add_argument("--chat", action="store_true", help="Start chat mode")
    
    args = parser.parse_args()
    
    if args.ingest:
        ingest_pdf(args.ingest)
        
    elif args.chat:
        print("Starting Chat... (Type 'exit' to quit)")
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["exit", "quit"]:
                    break
                
                for step in graph.stream(
                    {"messages": [{"role": "user", "content": user_input}]},
                    stream_mode="values",
                ):
                    step["messages"][-1].pretty_print()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
