class GeneralConverter(object):

    """
    This is the base class of all converters.
    """
    def __init__(self, initial_format, final_format, *input_file_paths):
        """
        The attributes get initlalized in subclasses.
        """
        self.initial_format = initial_format
        self.final_format = final_format
        self.file_batch = [
            input_file_path for input_file_path in input_file_pahts]

    def convert(self):
        return [self._single_convert(input_file_path)
                for input_file_path in self.file_batch]
