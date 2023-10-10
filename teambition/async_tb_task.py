#! /bin/python3
# coding = utf-8
"""该脚本统计网端缺陷信息并生成曲线图"""

import time
import jwt
import httpx
from datetime import datetime

from pyecharts import options as opts
from pyecharts.charts import Page, Line, Pie, Bar, Grid
from pyecharts.globals import ThemeType


def get_apptoken(_appid, _secret):
    """生成token"""
    now_time = int(time.time())
    expire_time = now_time + 3600
    token_dict = {'_appId': _appid, 'iat': now_time, 'exp': expire_time}
    headers = {'typ': 'jwt', 'alg': 'HS256'}
    encode = jwt.encode(payload=token_dict, key=_secret, headers=headers,
                        algorithm='HS256')
    return bytes.decode(encode)


# 获取企业成员
def get_orgmembers():
    params = {'orgId': '5b4ff29669269300014f47a3', 'pageSize': 150}
    res = client.get(url=host + '/api/org/member/list', params=params)
    org_members = {}
    for i in res.json()['result']:
        org_members[i['userId']] = i['name']
    return org_members


# 获取部门成员
def get_members():
    params = {
        'orgId': '5b4ff29669269300014f47a3',
        'deptId': '62859fd92c1198b62bfe7ac5',
        'pageSize': 30}
    res = client.get(url=host+'/api/org/department/members', params=params)
    mem_list = {}
    for i in res.json()['result']:
        mem_list[i['userId']] = i['name']
    return mem_list


# 获取用户参与的项目
def get_usertask(userId):
    params = {'pageSize': 50}
    header2 = {'x-operator-id': userId}
    res = client.get(url=host+'/api/v3/project/user-joined', headers=header2,
                     params=params)
    return res.json()['result']


# 获取项目自定义字段
def get_customfield(projectId):
    res = client.get(
        url=host + '/api/v3/project/%s/customfield/search'
        % (projectId), headers=header)
    customfield_list = {}
    for i in res.json()['result']:
        customfield_list[i['id']] = i['name']
    return customfield_list


# 获取项目工作流状态
def get_taskflowstatus(projectId):
    res = client.get(
        url=host + '/api/v3/project/%s/taskflowstatus/search'
        % (projectId))
    taskflowstatus_list = {}
    for i in res.json()['result']:
        taskflowstatus_list[i['id']] = i['name']
    return taskflowstatus_list


# 获取项目的任务类型
def get_tasktype(projectId):
    res = client.get(
        url=host + '/api/v3/project/%s/scenariofieldconfig/search'
        % (projectId))
    tasktype_list = {}
    for i in res.json()['result']:
        tasktype_list[i['name']] = i['id']
    return tasktype_list


# 获取项目标签
def get_tag(projectId):
    res = client.get(url=host + '/api/v3/project/%s/tag/search' % (projectId))
    tag_list = {}
    for i in res.json()['result']:
        tag_list[i['id']] = i['name']
    return tag_list


# 指定项目中每个人的任务
def get_task(client, TQL, projectId):
    customfield_list = get_customfield(projectId)
    taskflowstatus_list = get_taskflowstatus(projectId)
    org_members = get_orgmembers()
    tasktype_list = get_tasktype(projectId)
    sfcId = tasktype_list.get('网端缺陷')
    if not sfcId:
        sfcId = tasktype_list.get('缺陷')
    params = {'pageSize': 1000, 'q': 'TQL: sfcId=%s %s' % (sfcId, TQL)}
    res = client.get(
        url=host+'/api/v3/project/%s/task/query'
        % (projectId), params=params)
    if res.json()['count'] == 0:
        return 0
    else:
        count = res.json()['count']
    # bug_name = []
    time_sum = {}
    done_bug_sum = {}
    taskstatus_sum = {}
    user_sum = {}
    bugtype_sum = {}
    buglevel_sum = {}
    bugorigin_sum = {}
    bugenv_sum = {}
    bugback_sum = {}
    for i in res.json()['result']:
        # bug_name.append(i['content'])
        bug_status = i['isDone']
        create_time = datetime.strptime(
            i['created'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y/%m/%d')
        update_time = datetime.strptime(
            i['updated'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y/%m/%d')
        time_sum[create_time] = time_sum.get(create_time, 0) + 1
        if bug_status:
            done_bug_sum[update_time] = done_bug_sum.get(update_time, 0) + 1
        for field in i['customfields']:
            if customfield_list.get(field['cfId']) == '缺陷类型':
                bugtype = field['value'][0]['title']
                bugtype_sum[bugtype] = bugtype_sum.get(bugtype, 0) + 1
            elif customfield_list.get(field['cfId']) == '严重程度':
                buglevel = field['value'][0]['title']
                buglevel_sum[buglevel] = buglevel_sum.get(buglevel, 0) + 1
            elif customfield_list.get(field['cfId']) == '缺陷来源':
                bugorigin = field['value'][0]['title']
                bugorigin_sum[bugorigin] = bugorigin_sum.get(bugorigin, 0) + 1
            elif customfield_list.get(field['cfId']) == '环境信息':
                bugenv = field['value'][0]['title']
                bugenv_sum[bugenv] = bugenv_sum.get(bugenv, 0) + 1
            elif customfield_list.get(field['cfId']) == '前/后端':
                bugback = field['value'][0]['title']
                bugback_sum[bugback] = bugback_sum.get(bugback, 0) + 1
        username = org_members.get(i['executorId'])
        user_sum[username] = user_sum.get(username, 0) + 1

        taskstatus = taskflowstatus_list.get(i['tfsId'])
        taskstatus_sum[taskstatus] = taskstatus_sum.get(taskstatus, 0) + 1
        # tag = tag_list.get(i['tagIds'][0])
        # tag_sum[tag] = tag_sum.get(tag, 0) + 1
    return count, time_sum, done_bug_sum, taskstatus_sum,\
        user_sum, bugtype_sum, buglevel_sum, bugorigin_sum,\
        bugenv_sum, bugback_sum


# 获取不同项目数据
def project_analysis(project_dict: dict):
    project_count = {}
    project_time_sum = {}
    project_donebug_sum = {}
    project_status_sum = {}
    project_user_sum = {}
    project_bugtype_sum = {}
    project_buglevel_sum = {}
    project_bugorigin_sum = {}
    project_bugenv_sum = {}
    project_bugback_sum = {}
    for name, projectId in project_dict.items():
        if name == '任务流程规范化':
            TQL = 'AND (stageId=6392a4feccb00b0040efa25a OR \
            stageId=63e468e1a1053d001899eb44)'
        elif name == '开机自检':
            TQL = 'AND tasklistId=637f067025d55600403ca0e2'
        elif name == '无人车管理平台Web':
            TQL = 'AND (tasklistId=63c0c43648e35f0018f53cd7 OR \
                    tasklistId=639a8e4b7697d90041644251)'
        elif name == '运营APP':
            TQL = 'AND tasklistId=639a8f86a348fe0040ad39cc'
        else:
            TQL = ''
        count, time_sum, done_bug_sum, taskstatus_sum, user_sum,\
            bugtype_sum, buglevel_sum, bugorigin_sum, bugenv_sum,\
            bugback_sum = get_task(client, TQL, projectId)
        project_count[name] = count
        project_time_sum[name] = time_sum
        project_donebug_sum[name] = done_bug_sum
        project_status_sum[name] = taskstatus_sum
        project_user_sum[name] = user_sum
        project_bugtype_sum[name] = bugtype_sum
        project_buglevel_sum[name] = buglevel_sum
        if name != '监控中心' and name != '开机自检':
            project_bugorigin_sum[name] = bugorigin_sum
            project_bugenv_sum[name] = bugenv_sum
            project_bugback_sum[name] = bugback_sum
    return project_count, project_time_sum, project_donebug_sum,\
        project_status_sum, project_user_sum, project_bugtype_sum,\
        project_buglevel_sum, project_bugorigin_sum, project_bugenv_sum,\
        project_bugback_sum


# 生成折线图
def line_chart(data1: dict, data2: dict, title, chart_id):
    x_data = set()
    y1_data = []
    y2_data = []
    y3_data = []
    for name in data1.keys():
        x_data.add(name)
    for name in data2.keys():
        x_data.add(name)
    x_data = sorted(x_data)
    for i in x_data:
        y1_data.append(data1.get(i, 0))
        y2_data.append(data2.get(i, 0))
    for i, _ in enumerate(y1_data):
        y3_data.append(sum(y1_data[:i+1]) - sum(y2_data[:i+1]))

    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.DARK, chart_id=chart_id))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title,
                subtitle='缺陷数量统计',
                title_textstyle_opts=opts.TextStyleOpts(
                    font_family="Microsoft YaHei"),
                pos_left="center"),
            legend_opts=opts.LegendOpts(pos_left="left"),
            xaxis_opts=opts.AxisOpts(
                name="数量",
                axislabel_opts=opts.LabelOpts(rotate=-15)),
            yaxis_opts=opts.AxisOpts(name="日期", is_scale=True),
            )
        .add_xaxis(x_data)
        .add_yaxis("创建BUG数", y1_data, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(width=3))
        .add_yaxis("解决BUG数", y2_data, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(width=3))
        .add_yaxis("剩余BUG数", y3_data, is_smooth=True,
                   linestyle_opts=opts.LineStyleOpts(width=3))
            )
    return c


# 生成饼图
def pie_chart(project_count: dict, title, chart_id):
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK, chart_id=chart_id))
        .add(
            "",
            [list(z) for z in project_count.items()],
            center=["60%", "50%"])
        .set_global_opts(title_opts=opts.TitleOpts(
                             title=title,
                             pos_left="center"),
                         legend_opts=opts.LegendOpts(
                             orient="vertical",
                             pos_top="5%",
                             pos_left="2%"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            )
    return c


# 绘制条形图
def bar_chart(data: dict, title, chart_id):
    x_data = set()
    for items in data.values():
        for name in items.keys():
            x_data.add(name)
    y_data = list(data.keys())
    all_data = []
    for i in y_data:
        y1_data = []
        for name in x_data:
            y1_data.append(data[i].get(name, 0))
        all_data.append(y1_data)

    c = (
        Bar(init_opts=opts.InitOpts(width=1000, chart_id=chart_id))
        .add_xaxis(x_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title, subtitle=' '),
            yaxis_opts=opts.AxisOpts(name="缺陷数量"),
            xaxis_opts=opts.AxisOpts(
                name=title[:4],
                axislabel_opts=opts.LabelOpts(rotate=-15)
                ),
            legend_opts=opts.LegendOpts(
                type_="scroll",
                pos_left="2%",
                pos_top='5%',
                orient="vertical")
            )
        )
    for n, name in enumerate(y_data):
        c_ = (
            Bar()
            .add_xaxis(x_data)
            .add_yaxis(name, all_data[n])
                )
        c.overlap(c_)
    grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    grid.add(
        c,
        grid_opts=opts.GridOpts(pos_left="25%")
    )
    return grid


# 添加文字标题
def text_chart(text: str, size: int, chart_id):
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK, chart_id=chart_id))
        .set_global_opts(title_opts=opts.TitleOpts(
                             title=text,
                             title_textstyle_opts=opts.TextStyleOpts(
                                 font_size=size,
                                 color='#FFFFFF')),
                         legend_opts=opts.LegendOpts(is_show=False))
        )
    return c


# 将每日数据转换成每月数据
def month_transform(project_day_sum: dict):
    project_month_sum = {}
    for item in project_day_sum.values():
        for key, num in item.items():
            new_key = key[:-3]
            project_month_sum[new_key] = \
                project_month_sum.get(new_key, 0) + num
    return project_month_sum


if __name__ == '__main__':
    start_time = time.time()
    token = get_apptoken('63ad342a6aa592f07643d034',
                         'BMeIMuNiCPtaelXcbfoznWjzABuXldeg')
    host = 'https://open.teambition.com'
    header = {
        'Authorization': 'Bearer '+token,
        'X-Tenant-Type': 'organization',
        'X-Tenant-Id': '5b4ff29669269300014f47a3'}
    projectId = '63218086700e621f7bd2748e'
    project_dict = {
        '任务流程规范化': '62dfab5fd51a977b23f51970',
        '开机自检': '63218086700e621f7bd2748e',
        '监控中心': '62a9afb92ed5566088cc0840',
        '无人车不同模式': '62df473b376ec29c45950b63',
        '无人车管理平台Web': '616ce28fccce3c69eca1b933',
        '运营APP': '600173319b9da85382df80ed',
        '大屏展示解决方案': '63218048a0263948c1901ffb'}
    with httpx.Client(headers=header) as client:
        project_count, project_time_sum, project_donebug_sum,\
            project_status_sum, project_user_sum, project_bugtype_sum,\
            project_buglevel_sum, project_bugorigin_sum, project_bugenv_sum,\
            project_bugback_sum = project_analysis(project_dict)
    page = Page(layout=Page.DraggablePageLayout, page_title="缺陷管理")
    n = 0
    for project in project_dict.keys():
        page.add(line_chart(project_time_sum[project],
                            project_donebug_sum[project], project, n+1))
        n += 1
    project_month_bug = month_transform(project_time_sum)
    project_month_donebug = month_transform(project_donebug_sum)
    page.add(line_chart(project_month_bug, project_month_donebug, "总体项目", n+1),
             pie_chart(project_count, "缺陷总计", n+2),
             bar_chart(project_bugtype_sum, "缺陷类型统计", n+3),
             bar_chart(project_status_sum, "缺陷状态统计", n+4),
             bar_chart(project_buglevel_sum, "缺陷等级统计", n+5),
             bar_chart(project_user_sum, "开发人员统计", n+6),
             bar_chart(project_bugorigin_sum, "缺陷来源统计", n+7),
             bar_chart(project_bugenv_sum, "缺陷环境统计", n+8),
             bar_chart(project_bugback_sum, "缺陷归属统计", n+9),
             text_chart("网端项目任务总览", 30, n+10))
    page.render("temp.html")
    page.save_resize_html('temp.html',
                          cfg_file='chart_config.json', dest='index.html')
    end_time = time.time()
    print('\033[32mProgram time consuming: %s\033[0m'% (end_time - start_time))
