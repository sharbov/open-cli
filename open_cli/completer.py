import shlex

from prompt_toolkit.completion import Completer, Completion


class CommandCompleter(Completer):
    """Manage completion suggestions to the CLI."""

    def __init__(self, client):
        """Create a CLI commands completer based on the client object."""
        self.client = client
        self.definitions = client.swagger_spec.definitions

    def get_completions(self, document, complete_event):
        """Yields CLI completion based on the input text and the client object."""
        for completion, position in self._text_to_completions(document.text):
            yield Completion(completion, start_position=-position)

    def _text_to_completions(self, text):
        """Convert raw text into completion suggestions."""
        try:
            words = shlex.split(text)
        except ValueError:
            words = text.split(" ")

        operation, text = self._extract_operation(words=words)

        if callable(operation):
            return self._get_operation_params_completions(operation=operation, text=text)

        return self._get_completion(text=text, options=dir(operation))

    def _extract_operation(self, words):
        """Get the required client operation and separate it from the remaining text."""
        operation = self.client

        for word in words:
            attr = getattr(operation, word, None)
            if attr is None:
                return operation, words[-1]

            operation = attr

        return operation, ""

    def _get_operation_params_completions(self, operation, text):
        """Get suggestions based on operation and remaining text."""
        completion_offset = 0

        # Strip argument prefix
        if text.startswith("--"):
            text = text[2:]
            completion_offset = 2

        # Handel definition type argument completions
        if "." in text:
            return self._get_definition_completions(operation, text)

        return [("--" + attribute, len(text) + completion_offset)
                for attribute in operation.operation.params
                if attribute.startswith(text) and not attribute.startswith("_")]

    def _get_definition_completions(self, operation, text):
        """Get suggestions based on definition and remaining text."""
        param_words = text.split(".")

        # Only two words parameter completion are supported
        if len(param_words) != 2:
            return []

        param_name, sub_name = param_words
        if param_name not in operation.operation.params:
            return []

        param_object = operation.operation.params[param_name]
        param_schema = param_object.param_spec.get("schema")
        if not param_schema:
            return []

        param_ref = param_schema.get("$ref")
        if not param_ref:
            return []

        definition_name = param_ref.split('/')[-1]
        definition = self.definitions.get(definition_name)

        if not definition:
            return []

        return self._get_completion(text=sub_name, options=dir(definition()))

    @staticmethod
    def _get_completion(text, options):
        """Get completion properties based on text and possible options."""
        return [(option, len(text)) for option in options
                if option.startswith(text) and not option.startswith("_")]
