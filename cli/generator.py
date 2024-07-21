from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Dict, Any, List, Tuple


TEMPLATE_LOADER = FileSystemLoader(Path(__file__).parent.joinpath('templates'))
ENV = Environment(loader=TEMPLATE_LOADER)


def generate_model_code(json_schema: Dict[str, Any], out_dir: Path, model_name: str):
    tm = ENV.get_template('model.jinja')
    code = tm.render(data=json_schema, model_name=model_name)
    with open(out_dir.joinpath(model_name + '.py'), 'w') as file:
        file.write(code)


def generate_router_code(model_code: List[str], router_file: Path):
    tm = ENV.get_template('router.jinja')

    nested_list_by_classname, model_name = _create_nested_list_by_classname(model_code)
    nested_tree = _create_nested_tree(nested_list_by_classname, model_name)
    code = tm.render(nested_tree=nested_tree, model_name=model_name)
    with open(router_file, 'w', encoding='utf-8') as file:
        file.write(code)


def _remove_unnecessary_lines(model_code: List[str]) -> List[str]:
    code = []
    for i in model_code:
        if not i.isspace() and 'import' not in i:
            code.append(i.strip())
    return code


def _create_nested_list_by_classname(model_code: List[str]) -> Tuple[Dict[str, List[str]], str]:
    clean_code = _remove_unnecessary_lines(model_code)
    
    classes = []
    last_classname = None
    nested_list_by_classname = {}
    for line in clean_code:
        if 'class' in line:
            last_classname = line[6:-12]
            classes.append(last_classname)
        else:
            _, value = line.split(':', maxsplit=1)
            fieldtype, _ = value.split('=', maxsplit=1)
            fieldtype = fieldtype.strip()
            for m in classes:
                if m == fieldtype or f'{m} | None' == fieldtype:
                    if not nested_list_by_classname.get(last_classname):
                        nested_list_by_classname[last_classname] = [m]
                    else:
                        nested_list_by_classname[last_classname].append(m)
                elif f'List[{m}]' == fieldtype or f'List[{m}] | None' == fieldtype:
                    if not nested_list_by_classname.get(last_classname):
                        nested_list_by_classname[last_classname] = [f'List[{m}]']
                    else:
                        nested_list_by_classname[last_classname].append(f'List[{m}]')
    
    return nested_list_by_classname, last_classname


def _create_nested_tree(nested_list: Dict[str, List[str]], classname: str) -> Dict[str, Dict | None]:
    if not nested_list.get(classname):
        return {classname: None}
    nested_tree = {}
    for i in nested_list[classname]:
        if not nested_tree.get(classname):
            nested_tree[classname] = _create_nested_tree(nested_list, i)
        else:
            nested_tree[classname].update(_create_nested_tree(nested_list, i))

    return nested_tree
