from abc import ABC, abstractmethod

class ITranslator(ABC):
    @abstractmethod
    def translate(self, file_path: str) -> str | None:
        """Translates content from a file."""
        pass

class IFileManager(ABC):
    @abstractmethod
    def store_translated_text(self, file_name: str, text: str, output_folder: str) -> None:
        """Stores translated text to a file."""
        pass
    
    @abstractmethod
    def combine_translated_files(self, input_folder: str, output_folder: str) -> str:
        """Combines multiple translated files into one."""
        pass