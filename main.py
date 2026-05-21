import sys
from uuid import uuid4
from langchain_core.messages import HumanMessage
from agent.orchestrator.core.graph import main_agent 

def main():
    print("================================================================")
    print("🚀 Master Financial Orchestrator Connected (RAG + Web + Finance)")
    print("   Type 'exit' or 'quit' to end the session.")
    print("================================================================\n")

    while True:
        try:
            # 1. Capture user input
            user_query = input("👤 User: ").strip()
            
            if user_query.lower() in ["exit", "quit", "q"]:
                print("\nGoodbye! 👋")
                break
                
            if not user_query:
                continue

            # 2. Initialize the master state
            #config = {"configurable": {"thread_id": str(uuid4())}}
            initial_state = {
                "messages": [HumanMessage(content=user_query)],
                "user_query": user_query,
                "rag_query" : user_query,
                "tavily_query" : user_query,
                "document_chunks": [],
                "web_results": [],
                "stock_data": ""
            }

            print("\n⚙️  Orchestrator Processing Flow:")
            
            final_state = None
            
            # 3. Stream graph updates node-by-node
            for event in main_agent.stream(initial_state, stream_mode="updates"):
                for node_name, node_output in event.items():
                    print(f"   ↳ 🟩 Executed Node: [{node_name}]")
                    
                    # Capture the latest state update so we can read the final output
                    final_state = node_output

            # 4. Extract and print the structured Pydantic report cleanly
            if final_state and "final_report" in final_state:
                report = final_state["final_report"]
                
                print("\n" + "="*60)
                print("📋 FINAL SYNTHESIZED REPORT")
                print("="*60)
                
                if report.rag_section:
                    print(f"\n📚 [2025 Annual Report Analysis]\n{report.rag_section}")
                    print("-" * 40)
                    
                if report.finance_section:  # checks if finance data was written
                    print(f"\n📈 [Live Market Performance]\n{report.finance_section}")
                    print("-" * 40)
                    
                if report.web_section:
                    print(f"\n🌐 [Recent Web Intelligence]\n{report.web_section}")
                    print("-" * 40)
                    
                print(f"\n🧠 [Executive Summary]\n{report.combined_summary}")
                print("="*60 + "\n")
            else:
                print("\n⚠️  Processing completed, but no structured report was returned.\n")
                        
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye! 👋")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")
        

if __name__ == "__main__":
    main()