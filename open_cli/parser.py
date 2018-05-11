import shlex

from fire import parser


class CommandParser:
    """Parse command string into client operations and arguments."""

    def __init__(self, client):
        """Initialize parser based on the given client object."""
        self.client = client

    def parse(self, text):
        """Parse command string into operations and arguments."""
        attributes = []
        raw_arguments = []

        # Parse command elements based on the regular expression
        elements = shlex.split(text)

        # Separate elements into attributes and arguments
        for element in elements:
            if element.startswith('--'):
                raw_arguments.append(element)
            else:
                attributes.append(element)

        operation = self.get_operation(attributes=attributes)
        arguments = self.get_arguments_dict(raw_arguments=raw_arguments)

        return operation, arguments

    def get_operation(self, attributes):
        """Return the required operation based on the attribute list."""
        obj = self.client

        for attribute in attributes:
            sub_obj = getattr(obj, attribute, None)
            if sub_obj is None:
                raise ValueError("Illegal operation %r" % attributes)
            obj = sub_obj

        return obj

    def get_arguments_dict(self, raw_arguments):
        """Convert a list of raw arguments into a dictionary format."""
        arguments = {}

        for raw_argument in raw_arguments:
            full_path, value = raw_argument.lstrip("-").split("=")
            self.set_nested(arguments, value, *full_path.split('.'))

        return arguments

    @staticmethod
    def set_nested(dictionary, value, *path):
        """Set the value in the given path to the given nested dictionary."""
        for level in path[:-1]:
            dictionary = dictionary.setdefault(level, {})

        # Use fire parser to convert raw argument into a value
        dictionary[path[-1]] = parser.DefaultParseValue(value)
