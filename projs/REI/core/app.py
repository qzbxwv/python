from fastapi import FastAPI

app = FastAPI()

@app.get('/usr/me')
async def read_usr_me():
    return {'user': 'current user'}

@app.get('/usr/{usrid}')
async def read_usr_id(usrid : str):
    return {'user': usrid}


