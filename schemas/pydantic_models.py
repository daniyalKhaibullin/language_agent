from pydantic import BaseModel, Field
from typing import List, Optional

class Flashcard(BaseModel):
    german_word: str = Field(description="The new German word or phrase.")
    english_translation: str = Field(description="The English translation.")
    example_sentence: str = Field(description="An example sentence in German using the word.")

class Mistake(BaseModel):
    user_error: str = Field(description="The incorrect German phrase used by the user.")
    correction: str = Field(description="The grammatically correct German phrase.")
    explanation: str = Field(description="Brief English explanation of the grammar rule.")

class ExtractionRecord(BaseModel):
    new_vocabulary: List[Flashcard] = Field(description="List of new vocabulary taught or used.")
    grammatical_mistakes: List[Mistake] = Field(description="List of mistakes made by the user.")

class RouterDecision(BaseModel):
    is_new_user: bool = Field(description="True if the user has no past sessions, False otherwise.")
