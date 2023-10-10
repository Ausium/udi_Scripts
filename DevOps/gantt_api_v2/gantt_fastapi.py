#! /usr/bin/python3
# coding=utf-8

import copy
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import jwt
import httpx
import uvicorn
import logging
from colorlog import ColoredFormatter
import threading
from  datetime import datetime
from jsonpath import jsonpath
import json


host = 'https://open.teambition.com'

# 生成token
def get_apptoken(_appid, _secret):
    now_time = int(time.time())
    expire_time = now_time + 60
    token_dict = {'_appId': _appid, 'iat': now_time, 'exp': expire_time}
    headers = {'typ': 'jwt', 'alg': 'HS256'}
    encode = jwt.encode(payload=token_dict, key=_secret,
                        headers=headers, algorithm='HS256')
    return encode

# 获取企业成员
def get_orgmembers(client):
    params = {'orgId': '5b4ff29669269300014f47a3', 'pageSize': 200, 'filter': 'all'}
    res = client.get(url=host + '/api/org/member/list', params=params)
    org_members = {}
    for i in res.json()['result']:
        org_members[i['userId']] = i['name']
    return org_members

# 获取任务分组
def get_tasklist(client, projectId):
    res = client.get(host+f'/api/v3/project/{projectId}/tasklist/search')
    tasklist = {}
    if res.is_success:
        for item in res.json()['result']:
            tasklist[item['id']] = item['title']
    return tasklist

# 获取任务列表
def get_stage(client, projectId, tasklistId):
    params = {'pageSize': 50, 'tasklistId': tasklistId}
    res = client.get(host+f'/api/v3/project/{projectId}/stage/search',
                     params=params)
    stagelist = {}
    if res.is_success:
        for item in res.json()['result']:
            stagelist[item['id']] = item['name']
    return stagelist
    
            

# 获取任务依赖关系,前置依赖,后置依赖
def get_task_depend(client, tasks):
    task_depend_name = {}
    task_depend_id = {}
    taskid_list = ""
    task_len = len(tasks)
    n = 0
    for task in tasks:
        if taskid_list:
            taskid_list += "," + task['id']
        else:
            taskid_list = task['id']
        if n >= 50 or task_len < 50:   
            param = {"taskId": taskid_list, "pageSize": 100}
            res = client.get(url=host+'/api/v3/task/dependency', params=param)
            result = res.json()['result']
            if result:
                for item in result:
                    fromTaskId = item['fromTaskId']
                    fromTaskName = jsonpath(tasks,
                                            f'$..?(@.id == "{fromTaskId}").content')
                    task_depend_name[item['toTaskId']] = fromTaskName[0]
                    task_depend_id[item['toTaskId']] = fromTaskId
            task_len -= 50
            n = 0
            taskid_list = ""
        else:
            n += 1
    return task_depend_name, task_depend_id

    

# 获取任务
def get_task(client, projectId, TQL, org_members):
    params = {"pageSize": 1000, "q": TQL}
    try:
        res = client.get(url=host+'/api/v3/project/%s/task/query' %(projectId),
                        params=params)
    except Exception as e:
        logger.error("Exception occurred: %s" % (e))
        return 0
    if res.status_code == 200:
        tasks = res.json()['result']
    else:
        print('Error fetching tasks data: ', res.text)
        tasks = []

    task_depend_name, task_depend_id = get_task_depend(client, tasks)
    def build_task_tree(tasks, parent_task_id=None):
        task_tree = []
        for task in tasks:
            if task.get('parentTaskId') == parent_task_id:
                involveMembers = ''
                for memberId in task['involveMembers']:
                    sub_member = org_members.get(memberId, False)
                    if involveMembers and sub_member:
                        involveMembers += ', ' + sub_member
                    elif (not involveMembers) and sub_member:
                        involveMembers = sub_member
                    else:
                        involveMembers = ""
                if task['dueDate']:
                    endDate_obj = datetime.strptime(task['dueDate'],
                                                "%Y-%m-%dT%H:%M:%S.%fZ")
                    if task['isDone']:
                        color = "gray"
                    elif endDate_obj > datetime.now():
                        color = "green"
                    elif endDate_obj <= datetime.now():
                        color = "red"
                    else:
                        color = ''
                else:
                    color = ''
                fromTaskId = task_depend_id.get(task['id'], "")
                fromTaskName = task_depend_name.get(task['id'], "")
                task_node = {'id': task['id'],
                             'content': task['content'],
                             'executor': involveMembers,
                             'startDate': task['startDate'],
                             'endDate': task['dueDate'],
                             'collapsed': 'ture',
                             'color': color,
                             'fs': fromTaskName,
                             'fsId': fromTaskId,
                             'children': build_task_tree(tasks, task['id'])}
                task_tree.append(task_node)
        return task_tree
    task_tree = build_task_tree(tasks)
    return task_tree


# 通过任务分组和任务列表过滤任务
def filter_task(projectName, projectId, client, n):
    # 定义单个项目的json内容
    api_data = {"content": projectName, "children": []}
    org_members = get_orgmembers(client)
    # 获取任务分组字典
    tasklist = get_tasklist(client, projectId)
    for tasklistId, tasklistName in tasklist.items():
        stagelist = get_stage(client, projectId, tasklistId)
        stage_data = []
        for stageId, stageName in stagelist.items():
            TQL = f"TQL: tasklistId={tasklistId} AND stageId={stageId}"
            task_tree = get_task(client, projectId, TQL, org_members)
            stage_data.append({"content": stageName, "collapsed": "ture",
                               "children": task_tree})
        api_data["children"].append({"content": tasklistName, "children": stage_data})
    if n is False:
        json_data.append(api_data)
    else:
        json_data[n] = api_data
            



app = FastAPI()
# 允许跨域
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

logger = logging.getLogger("access")
logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(levelname)s: [%(asctime)s] -- %(message)s")
# 输出到文件中
# handler = logging.FileHandler("access.log")
# 输出到终端
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s: [%(asctime)s] -- %(log_color)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.middleware("http")
async def log_access(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f'{request.client.host} - "{request.method} {request.url.path} \
{request.scope["http_version"]}" {response.status_code}  {process_time:.3f}s \
{request.headers["User-Agent"]}')
    return response


@app.get("/api/tasks")
async def tasks(name=None):
    if name:
        filter_data = jsonpath(json_data, f'$...?("{name}" in @.executor)')
        if type(filter_data) != list:
            return []
        else:
            filter_data_copy = copy.deepcopy(filter_data)
            for item in filter_data_copy:
                if item['children']:
                    item['children'] = []
            return filter_data_copy
    else:
        if 'json_data' in globals():
            return json_data
        else:
            return "not data"

def run_scheduler():
    while True:
        with open("./project.json", 'r', encoding='utf-8') as file:
            projectItem = json.load(file)
        global json_data
        if 'json_data' not in globals():
            json_data = []
            n = False
        else:
            n = 0
        token = get_apptoken('63ad342a6aa592f07643d034',
                         'BMeIMuNiCPtaelXcbfoznWjzABuXldeg')
        header = {'Authorization': 'Bearer '+token,
              'X-Tenant-Type': 'organization',
              'X-Tenant-Id': '5b4ff29669269300014f47a3'}
        logger.debug('开始同步接口')
        with httpx.Client(headers=header) as client:
            for projectName, projectId in projectItem.items():
                filter_task(projectName, projectId, client, n)
                # get_task(projectName, projectId, n)
                if n is not False:
                    n += 1
        logger.debug('接口同步成功')
        time.sleep(60)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_scheduler)
    t2 = threading.Thread(target=uvicorn.run,
                          kwargs={"app":app, "host":"0.0.0.0",
                                  "port": 8000, "access_log": False})
    # uvicorn.run(app=app, host="0.0.0.0", port=8001, access_log=False)
    # t1.start()
    t2.start()
    while True:
        if not t1.is_alive():
            t1 = threading.Thread(target=run_scheduler)
            t1.start()
            print("t1 start")
        time.sleep(30)
