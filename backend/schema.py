from pydantic import BaseModel


class UserInput(BaseModel):
    user_input: str


class TeprolinTokenizationData:
    text: str
    exec: str

    def __init__(self, text, exec):
        self.text = text
        self.exec = exec


class PreprocessedInput:
    _bner: str
    _lemma: str
    _ctg: str
    _deprel: str

    def __init__(self, _bner, _lemma, _ctg, _deprel):
        self._bner = _bner
        self._lemma = _lemma
        self._ctg = _ctg
        self._deprel = _deprel