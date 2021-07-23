import requests
import os
import logging
import re
import sys

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


api_key = os.environ['API_KEY']
api_url = 'https://api.clockify.me/api/v1'
headers = {'X-Api-Key': api_key}


def format_time(string):
    string = re.search(r'T([\d\S]*?)Z', string)
    return string.group(1)


def get_workspace_id():
    '''Returns workspace id'''
    url = api_url + '/workspaces'
    res = requests.get(url, headers=headers)
    res = res.json()
    return res[0]['id']


def get_user_id(workspace_id):
    '''Takes workspace_id and returns user_id'''
    url = api_url + '/user'
    res = requests.get(url, headers=headers)
    res = res.json()
    return res['id']


def get_time_entries(workspace_id, user_id):
    '''Returns all time entries from user workspace'''
    url = api_url + '/workspaces/' + workspace_id + '/user/' + user_id + '/time-entries'
    res = requests.get(url, headers=headers)
    res = res.json()
    return res


def group_entries(report):
    '''Groups all entries by date'''
    report_dict = {}
    for entry in report:

        try:
            report_dict[entry['date']].append(entry)
        except:
            report_dict[entry['date']] = [entry]
    return report_dict


def form_report(time_entries):
    '''Forms data for printing the report'''
    report_list = []
    for entry in time_entries:
        if entry['timeInterval']['end']:
            entry_dict = {}
            entry_dict['description'] = entry['description']
            date = re.search(r'([\d\S]*?)T', entry['timeInterval']['end'])
            entry_dict['date'] = date.group(1)
            entry_dict['time'] = re.sub('PT', '', entry['timeInterval']['duration'])
            entry_dict['start_time'] = format_time(entry['timeInterval']['start'])
            entry_dict['end_time'] = format_time(entry['timeInterval']['end'])
            report_list.append(entry_dict)
        else:
            continue
    report_list = group_entries(report_list)
    return report_list


def print_report(report):
    '''Prints report with stdout'''
    for date in report:
        sys.stdout.write('Date: ' + date + '\n')
        for task in report[date]:
            sys.stdout.write('Description: ' + task['description'] + '. Time spent: ' + task['time'] + '. '
                            'Started at: ' + task['start_time'] + '. Finished at: ' + task['end_time'] + '\n')


if __name__ == '__main__':
    workspace_id = get_workspace_id()
    user_id = get_user_id(workspace_id)
    time_entries = get_time_entries(workspace_id, user_id)
    print_report(form_report(time_entries))
