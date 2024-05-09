# TODO make analysis on problem


class Analyzer:
    def __init__(self, structure):
        self.structure = structure

    def make_general_analysis(self):
        return self


class Subject:
    pass


class CollectedDataObject:
    pass


def get_subjects_for_user() -> list[Subject]:
    pass


def collect_data_on_subjects(subjects) -> CollectedDataObject:
    """Extract data from cache system and """
    pass


class DataAfterAnalysis:
    pass


def make_analysis_of_current_data(current_data_on_subjects) -> DataAfterAnalysis:
    """
    Function to initialize begin
    @param current_data_on_subjects:
    @return:
    """
    pass


class FormedMessage:
    pass


def comprise_message(filtered_data) -> FormedMessage:
    pass


def send_message_to_bot(message):
    pass


def make_general_algorithm():
    subjects = get_subjects_for_user()
    current_data_on_subjects = collect_data_on_subjects(subjects)
    filtered_data = make_analysis_of_current_data(current_data_on_subjects)
    message = comprise_message(filtered_data)
    send_message_to_bot(message)


if __name__ == '__main__':
    pass
