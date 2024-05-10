from AnalysisApp.model import Metric


class TableMetric:
    pass


class ModelType:
    """
    List of all possible ML models for analysis.
    """
    pass


class TextPacket:
    """
    Article structured in a certain way.
    """
    pass


async def run_comparison(first_text: str, second_text: str, model_type: ModelType) -> Metric:
    pass


async def run_comparison_for_texts_sets(first_set: list[TextPacket], second_set: list[TextPacket]) -> TableMetric:
    pass
