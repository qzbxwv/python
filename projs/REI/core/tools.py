import wikipediaapi
import asyncio
import os
import docker
import tempfile



class Tool:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        
    async def use(self, query : str) -> str:
        return 'PARENTAL CLASS NOT IMPLEMENTED' 
    
class EgoSearch(Tool):

    def __init__(self):
        super().__init__(name="EgoSearch", desc="Ego uses GoogleSearch grounding to find all information needed")

    async def use(self, query : str) -> str:
        print(f"EGO Search вызван c {query}")
        return 'Ego Seach not IMPLEMENTED as tool use'
    
class AlterEgo(Tool):
    def __init__(self):
        super().__init__(name="AlterEgo", desc="AlterEgo takes over Ego")
    
    async def use(self, query: str) -> str:
        print(f'AlterEgo вызван c {query}')
        return "AlterEgo not implemented as tool use"

class EgoCode(Tool):
    def __init__(self):
        super().__init__(name="EgoCode", desc="Executes Python code for accurate calculations with libraries (NumPy, SymPy, SciPy) in a secure EgoBox."
        )
        try:
            
            self.docker_client = docker.from_env()
            self.docker_client.ping()
            print("--- Docker-client EgoBox READY. ---")
        except Exception as e:
            print("--- Docker-client NOT READY---")
            print(f"--- ERROR: {e} ---")
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

            # except docker.errors.ContainerError as e:

                # error_output = e.stderr.decode('utf-8').strip()
                # return f"Ошибка выполнения кода в EgoBox:\n{error_output}"
            
            #  except docker.errors.ImageNotFound:
                #  raise EgoBoxExecutionError("Образ 'egobox:latest' не найден. Соберите его командой 'docker build ...'")

            except Exception as e:

                return f"Docker ERROR: {e}"


    async def use(self, query: str) -> str:
        print(f"--- EGO, CODE! with query: {query}---")

        return await asyncio.to_thread(self._execute_in_docker_sync, query)
        
class EgoWiki(Tool):
    def __init__(self):
        super().__init__(name="EgoWiki", desc="Ego uses WikiAPI lib to find every Wiki information needed")
        
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent="EGO knowledge",
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
