import wikipediaapi
import asyncio
import os
import docker
import tempfile
from typing import TYPE_CHECKING, List, Dict

if TYPE_CHECKING:
    from .llm_backend import LLMBackend
    from google.genai import types

class Tool:
    def __init__(self, name: str, desc: str):
        self.name = name
        self.desc = desc
        
    async def use(self, query: str, backend: 'LLMBackend') -> str:
        raise NotImplementedError("Родительский класс 'Tool' не предназначен для использования.")

class EgoSearch(Tool):
    def __init__(self):
        super().__init__(name="EgoSearch", desc="Ego использует Google Search для поиска информации.")

    async def use(self, query: str, backend: 'LLMBackend') -> str:
        from .prompts import EGO_SEARCH_PROMPT_RU
        from google.genai import types
        
        print(f"--- EGO SEARCH QUERY: {query} ---")
        egosearch_tool = types.Tool(google_search=types.GoogleSearch())
        return await backend.generate(prompt_parts=query, temp=0.1, sys_inst=EGO_SEARCH_PROMPT_RU, tools=[egosearch_tool])

class AlterEgo(Tool):
    def __init__(self):
        super().__init__(name="AlterEgo", desc="AlterEgo берет на себя управление, чтобы проанализировать мысль.")
    
    async def use(self, query: str, backend: 'LLMBackend') -> str:
        from .prompts import ALTER_EGO_PROMPT_RU
        print(f"--- ALTER TAKES OVER EGO WITH QUERY: {query} ---")
        response = await backend.generate(prompt_parts=query, temp=0.9, sys_inst=ALTER_EGO_PROMPT_RU)
        print(f"--- ALTER RESPONSE: {response} ---")
        return response

class EgoCode(Tool):
    def __init__(self):
        super().__init__(name="EgoCode", desc="Выполняет Python код в безопасной песочнице EgoBox.")
        try:
            self.docker_client = docker.from_env()
            self.docker_client.ping()
            print("--- Docker-client EgoBox READY. ---")
        except Exception as e:
            print(f"--- Docker-client NOT READY: {e} ---")
            self.docker_client = None
   
    def _execute_in_docker_sync(self, code_string: str) -> str:
        if not self.docker_client:
            return "--- EGOBOX IS UNREACHABLE ---"

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=True) as tmp_file:
            tmp_file.write(code_string)
            tmp_file.flush() 
            host_path = tmp_file.name
            filename = os.path.basename(host_path)
            container_path = f"/sandbox/{filename}"
            volume_mapping = {host_path: {'bind': container_path, 'mode': 'ro'}}
            try:
                container = self.docker_client.containers.run(
                    image="egobox:latest",
                    command=["python", container_path], 
                    volumes=volume_mapping,
                    remove=True,
                    mem_limit="128m",
                    cpu_shares=512
                )
                return container.decode('utf-8').strip()
            except Exception as e:
                return f"Docker ERROR: {e}"

    async def use(self, query: str, backend: 'LLMBackend') -> str:
        print(f"--- EGO, CODE! with query: {query}---")
        return await asyncio.to_thread(self._execute_in_docker_sync, query)
        
class EgoWiki(Tool):
    def __init__(self):
        super().__init__(name="EgoWiki", desc="Использует Wikipedia для поиска точной информации.")
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent="EGO knowledge",
            language="ru",
            extract_format=wikipediaapi.ExtractFormat.WIKI,
        )
        
    def _search_wiki_sync(self, query: str):
        try:
            wiki_page = self.wiki_wiki.page(query) 
            if wiki_page.exists():
                return wiki_page.text
            else:
                return f"Страница '{query}' на Википедии не найдена."
        except Exception as e:
             return f'Ошибка при вызове WikiAPI: {e}'

    async def use(self, query: str, backend: 'LLMBackend') -> str:
        print(f"--- WikiAPI CALL WITH QUERY: {query} ---")
        return await asyncio.to_thread(self._search_wiki_sync, query)