import requests
import os
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


api_key = os.environ['API_KEY']
api_url = 'https://api.clockify.me/api/v1'
headers = {'X-Api-Key': api_key}


def get_workspace_id():
    url = api_url + '/workspaces'
    res = requests.get(url, headers=headers)
    res = res.json()
    return res[0]['id']


def get_project_id(workspace_id, project_name):
    url = api_url + '/workspaces/' + workspace_id + '/projects'
    res = requests.get(url, headers=headers)
    res = res.json()
    for project in res:
        if project['name'] == project_name:
            return project['id']
        else:
            continue
    else:
        raise ValueError('No projects found with specified name')


def get_all_tasks(workspace_id, project_id):
    url = api_url + '/workspaces/' + workspace_id + '/projects/' + project_id + '/tasks'
    res = requests.get(url, headers=headers)
    res = res.json()
    return res


if __name__=='__main__':
    workspace_id = get_workspace_id()
    project_id = get_project_id(workspace_id, 'Daily CLI reporter')
    tasks = get_all_tasks(workspace_id, project_id)
    print(tasks)
