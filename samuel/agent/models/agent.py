# Written by Juan Pablo Gutiérrez
# 23 01 2025

class Agent:
    _instance = None 

    accepted_files: list[str] = []
    accept_text: bool = True
    rag: bool = True
    name: str = ""
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Agent, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: str, accepted_files: list[str] = [], accept_text: bool = True, rag: bool = True):
        self.name = name
        self.accepted_files = accepted_files
        self.accept_text = accept_text
        self.rag = rag

    def get_accepted_files(self):
        return self.accepted_files

    def get_rag(self):
        return self.rag

    def get_accept_text(self):
        return self.accept_text