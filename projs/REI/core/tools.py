import wikipediaapi
import asyncio
import os
from dotenv import load_dotenv 

class Tool:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        
    async def use(self, query : str) -> str:
        return 'PARENTAL CLASS NOT IMPLEMENTED' 
    
class EgoSearch(Tool):

    def __init__(self):
        super().__init__(name="GoogleSearch", desc="Дает задачу Ego на поиск огромного кол-ва релевантной информации")
        self.api_key = os.getenv("EGO_SEARCH_API")
        if not self.api_key:
            raise ValueError("--- EGO_SEARCH_API NOT FOUND ---")

    async def use(self, query : str) -> str:
        print(f"EGO Search вызван c {query}")
        return 'gemini answer'
    
class PythonCodeExec(Tool):
    def __init__(self):
        super().__init__(name="PythonCodeExec", desc="Выполняет код Python с несколькими бибилиотеками в безопасном sandbox")
        
    async def use(self, query : str) -> str:
        # вызов sandbox python code exec
        print(f"Python code exec вызван c {query}")
        return 'python code executed'
        
class WikiAPI(Tool):
    def __init__(self):
        super().__init__(name="WikiAPI", desc="Ищет статьи на Википедии")
        
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent="REI agent",
            language="ru", # or en 
            extract_format=wikipediaapi.ExtractFormat.WIKI,
        )
        
    def _search_wiki_sync(self, query : str):
        try:
            wiki_page = self.wiki_wiki.page(query) 
            if wiki_page.exists():
                print("--- Wiki Page EXIST ---")
                print(f'--- WikiAPI ANSWER: {wiki_page.text} ---')
                return wiki_page.text
            else:
                print('--- Wiki Page DOES NOT EXIST ---')
                return 'Wiki Page DOES NOT EXIST'

        except Exception as e:
             print(f"--- WikiAPI CALL ERROR: {e} ---")
             return f'--- WikiAPI ERROR: {e}' 



    async def use(self, query : str):
        print(f"--- WikiAPI CALL WITH QUERY: {query} ---")
        result = await asyncio.to_thread(self._search_wiki_sync, query)
        return result
