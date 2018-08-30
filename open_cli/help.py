HELP_KEYWORDS = ["help", "h"]


def is_requested(arguments):
    """Returns True if a help argument is present.

    :param dict arguments: argument dictionary.
    :returns bool: True if a help keyword is present in arguments
    """
    for help_keyword in HELP_KEYWORDS:
        if help_keyword in arguments:
            return True

    return False


def show(operation):
    """Display the operation help string.

    :param callable operation: requested operation.
    """
    print("\n{}\n".format(operation.__doc__))
