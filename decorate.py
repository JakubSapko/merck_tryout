from functools import wraps
from typing import Optional


class MessageCatcher:

    def print_message(self, message):
        print(message)


def emit_messages(starting_message, ending_message):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            MessageCatcher().print_message(starting_message)
            result = method(self, *args, **kwargs)
            MessageCatcher().print_message(ending_message)
            return result
        return wrapper
    return decorator


class CaseProcessingHandler():

    @emit_messages(starting_message="Starting to determine COI", ending_message="Finished determining COI")
    def determine_country_of_incidence(self, row: Optional[str] = None) -> str:
        coi = "Poland" if row else "USA"
        return coi


if __name__ == "__main__":
    cph = CaseProcessingHandler()
    cph.determine_country_of_incidence()
