class GeneralConverter(object):

    """
    This is the base class of all converters.
    """
    def __init__(self, initial_format, final_format, input_file_objects):
        """
        The attributes get initlalized in subclasses.
        """
        self.initial_format = initial_format
        self.final_format = final_format
        self.file_batch = input_file_objects
  
    def convert(self):
        return [self._single_convert(input_file_object)
                for input_file_object in self.file_batch]
