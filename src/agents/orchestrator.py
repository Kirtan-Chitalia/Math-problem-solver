from langgraph.graph import StateGraph , END
from src.agents.state import PipelineState
from src.agents.ocr_agent import ocr_agent
from src.agents.classifier_agent import classifier_agent
from src.agents.solver_agent import solver_agent
from src.agents.verifier_agent import verifier_agent
from src.utils import get_logger

logger = get_logger(__name__)

def build_pipeline():
    """Build and compile the LangGraph pipeline."""

    graph = StateGraph(PipelineState)

    # add nodes
    graph.add_node("ocr",ocr_agent)
    graph.add_node("classifier",classifier_agent)
    graph.add_node("solver",solver_agent)
    graph.add_node("verifier",verifier_agent)

    # define edges
    graph.set_entry_point("ocr")
    graph.add_edge("ocr", "classifier")
    graph.add_edge("classifier","solver")
    graph.add_edge("solver","verifier")
    graph.add_edge("verifier",END)
    
    # compile
    pipeline = graph.compile()
    logger.info("Pipeline built and compiled successfully")
    return pipeline

def run_pipeline(image_path:str)->dict:
    """Run the full math solver pipeline on an image."""
    logger.info(f"Running pipeline for: {image_path}")

    pipeline = build_pipeline()

    result = pipeline.invoke(
        {
        "image_path": image_path
        })
    logger.info("Pipeline completed")
    return result

