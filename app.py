import pandas as pd
from cli.parser import parse_arguments
from services.data_service import DataService
from services.analysis import AnalysisService
from services.visualization import VisualizationService


def main():
    args = parse_arguments()
    data, title = DataService.load_data(args)
    analysis = AnalysisService.analyze(data)
    VisualizationService.show(data['Close'], analysis, title)


if __name__ == '__main__':
    main()