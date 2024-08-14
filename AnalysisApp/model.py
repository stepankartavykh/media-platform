class Metric:
    """
    Metric is the calculated quantity of some article or other entity,
    so system can compare entities between each other.



    1. Number of links in the article. links to base sources.
    2. Factual analysis.
    3. Words distribution. For example phrases like 'It seems'
    """
    # TODO - figure out basic operations. Standards of journalism. How good article identified? Is there a way to
    #  evaluate journalists quality?
    #

    """
    
    """

    def __init__(self, score_value: float, unique_metric_name: int = None):
        self.unique_name: int = unique_metric_name or id(self)
        self.score_value: float = score_value


class Subject:
    physics = 'physics'
    math = 'math'
    economics = 'economics'
    investments = 'investing'
