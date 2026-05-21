import os
from agent.orchestrator.core.graph import main_agent

def generate_graph_diagram():
    """Renders the master orchestrator LangGraph as a visual PNG diagram."""
    print("🎨 Rendering LangGraph topology...")
    try:
        # draw_mermaid_png calls the mermaid.ink API under the hood,
        # which means it works seamlessly without requiring local Graphviz system packages!
        png_bytes = main_agent.get_graph().draw_mermaid_png()
        
        output_filename = "orchestrator_graph.png"
        with open(output_filename, "wb") as f:
            f.write(png_bytes)
            
        print(f"🎉 Graph diagram successfully generated and saved to: '{os.path.abspath(output_filename)}'")
        
    except Exception as e:
        print(f"⚠️ Could not generate PNG directly: {e}")
        print("\nFallback: Printing raw Mermaid Markdown. You can paste this in any Mermaid viewer (like mermaid.live):")
        print("=" * 60)
        print(main_agent.get_graph().draw_mermaid())
        print("=" * 60)

if __name__ == "__main__":
    generate_graph_diagram()
