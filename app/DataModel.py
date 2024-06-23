from pydantic import BaseModel

class DataModel(BaseModel):
    """
    DataModel represents the structure for the input data with a single text field.
    
    Attributes:
        text (str): The text input for analysis.
    """
    text: str

class DataModel_2(BaseModel):
    """
    DataModel_2 represents the structure for the input data with text and additional feature field.
    
    Attributes:
        text (str): The text input for analysis.
        feature (str): Additional feature related to the text.
    """
    text: str
    feature: str
