import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

FILE_DIR = Path(__file__).parent

app = FastAPI(title='json-cli-rest')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def include_all_routers(app: FastAPI):
    for r in FILE_DIR.joinpath('routers').iterdir():
        if r.suffix == '.py':
            module_name = r.name[:-3]
            
            module = importlib.import_module(f'rest.routers.{module_name}')
            app.include_router(module.router)


include_all_routers(app)
