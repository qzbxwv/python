class Tool:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        
    def use(self, query : str):
        pass
    
class GoogleSearch(Tool):
    def __init__(self):
        super().__init__(name="GoogleSearch", desc="Дает задачу LLM на поиск огромного кол-ва релевантной информации")
        # поиск ключа
        
    def use(self, query : str):
        # вызов апи гугла
        print(f"Google Search вызван c {query}")
    
class PythonCodeExec(Tool):
    def __init__(self):
        super().__init__(name="PythonCodeExec", desc="Выполняет код Python с несколькими бибилиотеками в безопасном sandbox")
        
    def use(self, query : str):
        # вызов sandbox python code exec
        print(f"Python code exec вызван c {query}")
        
class WikiAPI(Tool):
    def __init__(self):
        super().__init__(name="WikiAPI", desc="Ищет статьи на Википедии")
        
    def use(self, query : str):
        # вызов wiki api
        print(f"WikiAPI вызван c {query}")
        