import subprocess
import click
import json
from pathlib import Path
from generator import generate_model_code, generate_router_code
from jsonschema import Draft202012Validator, SchemaError

FILE_DIR = Path(__file__).parent
CWD = Path().cwd()

@click.group()
def cli():
    pass


@cli.command('gen-model')
@click.option(
    '--json-schema', '-j', 
    type=click.Path(exists=True, dir_okay=False, path_type=Path), 
    required=True
)
@click.option(
    '--out-dir', '-o', 
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path), 
    required=True, 
    default=FILE_DIR.parent.joinpath('rest', 'models')
)
@click.option('--name', type=str)
def gen_model(json_schema: Path, out_dir: Path, name: str | None):
    path_to_json_schema = CWD.joinpath(json_schema)
    with open(path_to_json_schema, 'r') as file:
        schema = json.load(file)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as e:
        click.echo(f'Ошибка валидации JSON Schema:\n {str(e)}')
    
    if name:
        model_name = name
    elif n := schema.get('properties').get('kind').get('default'):
        model_name = n
    else:
        model_name = json_schema.name[:-5]

    generate_model_code(schema, out_dir, model_name.replace('-', '_'))


@cli.command('gen-rest')
@click.option(
    '--models', '-m', 
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path), 
    required=True, 
    default=FILE_DIR.parent.joinpath('rest', 'models')
)
@click.option(
    '--rest-routers', '-r', 
    type=click.Path(exists=True, dir_okay=True, file_okay=False, path_type=Path),
    required=True, default=FILE_DIR.parent.joinpath('rest', 'routers')
)
def gen_rest(models: Path, rest_routers: Path):
    for m in models.iterdir():
        if m.suffix == '.py':
            with open(m, 'r') as file:
                model_code = file.readlines()
            generate_router_code(model_code, rest_routers.joinpath(m.name))


@cli.command('save')
@click.argument('version')
@click.option('--message', '-m', type=str, default='')
def commit_changes_and_create_tag(version: str, message: str):
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        subprocess.run(['git', 'tag', version], check=True)
        subprocess.run(['git', 'push', 'origin', version], check=True)
        click.echo(f'Изменения созранены. Добавлен тэг: {version}')
    except subprocess.CalledProcessError as e:
        click.echo(str(e))


if __name__ == '__main__':
    cli()