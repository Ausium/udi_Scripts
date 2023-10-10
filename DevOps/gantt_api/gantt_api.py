#! /usr/bin/python3
# coding=utf-8

from flask import Flask, jsonify, request
import logging
from flask_cors import cross_origin
import time
import jwt
import httpx

# 生成token
def get_apptoken(_appid, _secret):
    now_time = int(time.time())
    expire_time = now_time + 3600
    token_dict = {'_appId': _appid, 'iat': now_time, 'exp': expire_time}
    headers = {'typ': 'jwt', 'alg': 'HS256'}
    encode = jwt.encode(payload=token_dict, key=_secret,
                        headers=headers, algorithm='HS256')
    return encode.decode()


# 获取企业成员
def get_orgmembers(client, host):
    params = {'orgId': '5b4ff29669269300014f47a3', 'pageSize': 200, 'filter': 'all'}
    res = client.get(url=host + '/api/org/member/list', params=params)
    org_members = {}
    for i in res.json()['result']:
        org_members[i['userId']] = i['name']
    return org_members


# 获取任务
def get_task(client, host, projectId):
    org_members = get_orgmembers(client, host)
    params = {'pageSize': 1000}
    res = client.get(url=host+'/api/v3/project/%s/task/query' %(projectId),
                     params=params)
    if res.status_code == 200:
        tasks = res.json()['result']
    else:
        print('Error fetching tasks data: ', res.text)
        tasks = []
    def build_task_tree(tasks, parent_task_id=None):
        task_tree = []
        for task in tasks:
            if task.get('parentTaskId') == parent_task_id:
                task_node = {'id': task['id'],
                             'content': task['content'],
                             'executor': org_members.get(task['executorId']),
                             'startDate': task['startDate'],
                             'endDate': task['dueDate'],
                             'children': build_task_tree(tasks, task['id'])}
                task_tree.append(task_node)
        return task_tree
    task_tree = build_task_tree(tasks)
    return task_tree


app = Flask(__name__)
# 设置日志级别和格式
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(message)s'
)
log = logging.getLogger('werkzeug')
log.disabled = True
@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    elapsed_time = time.time() - request.start_time
    msg = f'{request.remote_addr} -- {request.method} {request.path} \
{response.status_code} {request.environ["SERVER_PROTOCOL"]} \
{elapsed_time:.5f}s {request.user_agent}'
    app.logger.info(msg)
    return response

@app.route('/api/tasks', methods=['GET'])
@cross_origin()
def get_json_tasks():
    token = get_apptoken('63ad342a6aa592f07643d034',
                         'BMeIMuNiCPtaelXcbfoznWjzABuXldeg')
    host = 'https://open.teambition.com'
    header = {'Authorization': 'Bearer '+token,
              'X-Tenant-Type': 'organization',
              'X-Tenant-Id': '5b4ff29669269300014f47a3'}
    with httpx.Client(headers=header) as client:
        json_data = get_task(client, host, '6481388237f08e292980c6b2')
        
    return jsonify(json_data)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8000)
