class GeneralConverter:

    """
    This is the base class of all converters.
    """
    def __init__(self, initial_format, final_format, *files):
        """
        The attributes get initlalized in subclasses.
        """
        self.initial_format = initial_format
        self.final_format = final_format
        self.file_batch = [input_file for input_file in files]

    def batch_convert(self):
        file_batch = self.file_batch
        output_files = [self.convert(input_file) for input_file in file_batch]
        return output_files
