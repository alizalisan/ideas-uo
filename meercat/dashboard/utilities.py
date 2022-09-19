import ast
import re
import requests
from subprocess import check_output
from datetime import datetime
from pathlib import Path

from django.conf import settings
from database.models import EventLog
from database.utilities import get_repo_owner


def save_debug_event(log, json='', pull_request=None, request=None):

    if request is not None:
        uri = request.build_absolute_uri()
        view_name = request.resolver_match.view_name
        if request.user.is_anonymous:
            user = None
        else:
            user = request.user
    else:
        uri = ''
        view_name = ''
        user = None

    debug_event = EventLog(
        user=user,
        uri=uri,
        view_name=view_name,
        event_type=EventLog.EventTypeChoices.DEBUGGING,
        datetime=datetime.today(),
        log=log,
        json=json,
        pull_request=pull_request
    )
    debug_event.save()


def get_branches_with_status(project): # only works with public repos for now
    repo_owner = get_repo_owner(project)
    repo_name = project.name

    pulls_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls?state=all"
    branches_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches"

    pulls = requests.get(pulls_url).json()
    branches = requests.get(branches_url).json()

    branch_names = [branch['name'] for branch in branches]
    processed_branches = []
    branches_with_status = []

    # Process branches with pull request
    for pr in pulls:
        branch_name = pr['head']['ref']
        if branch_name in branch_names and branch_name not in processed_branches:
            branches_with_status.append({'branch': branch_name, 'status': pr['state']})
            processed_branches.append(branch_name)

    # Process branches without pull request
    for branch_name in branch_names:
        if branch_name not in processed_branches:
            branches_with_status.append({'branch': branch_name, 'status': 'No Pull Request'})

    return branches_with_status


def get_file_dirs(file_path):
    dirs = []
    aux_dir = ''

    for directory in file_path.split('/')[:-1]:
        aux_dir += directory + '/'
        dirs.append(aux_dir)
    
    return dirs


def list_project_files(project):
    project_directory = settings.BASE_DIR.parent / project.name
    project_path = Path(project_directory)
    output_bytes = check_output(["git", "ls-files"], cwd=project_path)

    file_paths = output_bytes.decode('utf-8').split('\n')[:-1]
    return file_paths


def list_project_files_directories(project_files):
    project_directories = []

    for file_path in project_files:
        file_dirs = get_file_dirs(file_path)
        for directory in file_dirs:
            if directory not in project_directories:
                project_directories.append(directory)
    
    return project_directories
            

def get_git_index(project):

    files = list_project_files(project)
    directories = list_project_directories(files)

    return {"directories": directories, "files": files}
    

python_doxygen_base_template = """\"\"\"!
    @brief Starts a paragraph that serves as a brief description.
    A brief description ends when a blank line or another sectioning command is encountered.

    @details A longer description.

    @author name

    @callgraph
    
"""

    
def get_type_hints(tree):
    arguments = []
    return_type = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for argument in node.args.args:
                arguments.append({ 'name': argument.arg, 'type': argument.annotation.id if argument.annotation else '-'})
            return_type = node.returns.id if node.returns else '-'
    
    return arguments, return_type


def python_doxygen_template(function_definition):
    pass_str = " pass" if function_definition[-1] == ':' else ': pass'
    tree = ast.parse(function_definition + pass_str, type_comments=True)
    arguments, return_type = get_type_hints(tree)
    template = python_doxygen_base_template
    
    for argument in arguments:
        template += f"    @param {argument['name']} [{argument['type']}] Description of parameter.\n"
        
    template += f"\n    @return [{return_type}] Description of returned value.\n\"\"\""
    
    return template


fortran_doxygen_base_template = """
!> @copyright Copyright 2022 UChicago Argonne, LLC and contributors
!!
!! @licenseblock
!! Licensed under the Apache License, Version 2.0 (the "License");
!! you may not use this file except in compliance with the License.
!!
!! Unless required by applicable law or agreed to in writing, software
!! distributed under the License is distributed on an "AS IS" BASIS,
!! WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
!! See the License for the specific language governing permissions and
!! limitations under the License.
!! @endlicenseblock
!!
!! @brief brief description.
!!
!! @details longer description
!!
"""

def get_parameters(subroutine:str) -> list:
    params = []
    m = re.match("subroutine (?P<subroutine>[a-zA-Z]\w{0,30})\((?P<params>[\s\S]*?)\)", subroutine)
    for param in m.group('params').split(','):
      param = param.replace('&', '');
      params.append(param.strip())
    
    return params


def fortran_doxygen_template(subroutine):
    template = fortran_doxygen_base_template
    parameters = get_parameters(subroutine)

    for parameter in parameters:        
        template += f"!! @param {parameter} Descirption\n"
            
    template += '!!\n'
    return template