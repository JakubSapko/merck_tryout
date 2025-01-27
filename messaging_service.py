import enum
import argparse

from abc import ABC, abstractmethod
from typing import Any, Optional


class MessageLevel(enum.Enum):
    NO_MSG = 0
    INFO = 1
    DEBUG = 2


GLOBAL_DEBUG_FLAG: MessageLevel = MessageLevel.NO_MSG


class MessagingService(ABC):

    @abstractmethod
    def message(self, message: Any, level: int):
        ...

    def log_to_file(self, message: str):
        print(f"Saving {message} to file abc.txt")


class GUIMessagingService(MessagingService):

    def __init__(self, gui):
        self.gui = gui

    def message(self, message: Any, level: int):
        if level > GLOBAL_DEBUG_FLAG.value:
            return
        if level >= MessageLevel.DEBUG.value:
            self.log_to_file(message)
            return
        if level >= MessageLevel.INFO.value:
            self.gui.set_gui_message(message)
            return


class STDMessagingService(MessagingService):

    def message(self, message: Any, level: int):
        if level > GLOBAL_DEBUG_FLAG.value:
            return
        if level >= MessageLevel.DEBUG.value:
            self.log_to_file(message)
            return
        if level >= MessageLevel.INFO.value:
            print(message)
            return


# MVP - skipping all other dependencies
class CaseProcessingHandler():

    def __init__(self, messaging_service: MessagingService):
        self.ms = messaging_service

    def determine_country_of_incidence(self, row: Optional[str] = None) -> str:
        # Note that this will only launch when in "DEBUG" mode
        self.ms.message("Starting to determine country of incidence", level=MessageLevel.INFO.value)
        coi = "Poland" if row else "USA"
        self.ms.message(row, level=MessageLevel.DEBUG.value)
        self.ms.message("Country of Incidence determined", level=MessageLevel.INFO.value)
        return coi


class GUI:
    def set_gui_message(self, message: str):
        print(f"I'm setting a GUI message {message}")


if __name__ == "__main__":
    # Get the debug level parsed
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "debug",
            nargs="?",
            help="Set the debug level",
            default="DEBUG=0"
            )

    args = parser.parse_args()

    if args.debug.startswith("DEBUG="):
        try:
            level = int(args.debug.split("=")[1])
            GLOBAL_DEBUG_FLAG = MessageLevel(level)
        except ValueError:
            raise ValueError("Expected 'DEBUG=<int>' format")
    else:
        raise ValueError("Expected 'DEBUG=<int>' format")

    gui = GUI()
    ms = STDMessagingService()
    # ms = GUIMessagingService(gui)
    cph = CaseProcessingHandler(ms)
    cph.determine_country_of_incidence()
