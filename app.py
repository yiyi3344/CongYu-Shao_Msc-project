from flask import Flask,jsonify,render_template,request
import requests
import json
import pandas as pd

HEADERS = {
    'Cookie': 'UOR=www.baidu.com,sports.sina.com.cn,; SINAGLOBAL=116.52.95.172_1625447206.451082; U_TRS1=000000ac.997c24cf.60e25da3.b26c7722; UM_distinctid=17a7449adb7e4f-0981a7314c4faa-34647600-384000-17a7449adb81130; __gads=ID=d40ebe68a6fad7e9-225bd0182fca00b7:T=1625448627:RT=1625448627:S=ALNI_MYRhHxOp53MwqIy4DvF6oAwmTLwag; U_TRS2=0000008b.2bf786be.60e3ceff.71a3b4da; Apache=222.221.182.139_1625554151.131443; ULV=1625554154771:4:4:4:222.221.182.139_1625554151.131443:1625554150912; Hm_lvt_35ddcac55ce8155015e5c5e313883b68=1625447205,1625536280,1625563490; vjuids=3ae3e213b.17a7e8cfc20.0.9b306541456a4; vjlast=1625620807; hqEtagMode=1; Hm_lpvt_35ddcac55ce8155015e5c5e313883b68=1625624240',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}


def get_config():
    with open('config.json', encoding='utf-8') as f:
        config = json.loads(f.read())
        return config


app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# 获取Nationality
@app.route('/nationality')
def nationality():
    config = get_config()
    teams = config['teams']
    return jsonify(teams), {'Content-Type': 'application/json'}

# 获取player
@app.route('/player')
def player():
    nid = int(request.args.get("nid", 932))
    df = pd.read_csv('player_all.csv')
    lists = df[(df['mins_played'] > 300) & (df['sl_team_id'] == int(nid))].to_dict(orient='records')
    return jsonify(lists), {'Content-Type': 'application/json'}

# 获取Passes
@app.route('/passes')
def passes():
    pid = int(request.args.get("pid"))
    tid = int(request.args.get("tid", 1))
    df = pd.read_csv('player_all.csv')
    player_info = df[(df['player_id'] == pid)].to_dict(orient='records')[0]
    times = player_info['times']
    if tid == 1:
        total_pass = player_info['total_pass']
        accurate_pass = player_info['accurate_pass']
        total_att_assist = player_info['total_att_assist']
        goal_assist = player_info['goal_assist']
    else:
        total_pass = round(player_info['total_pass']/times, 2)
        accurate_pass = round(player_info['accurate_pass']/times, 2)
        total_att_assist = round(player_info['total_att_assist']/times, 2)
        goal_assist = round(player_info['goal_assist']/times, 2)

    total_pass_lv = 100
    if total_pass > 0:
        accurate_pass_lv = round(accurate_pass / total_pass, 2) * 100
        total_att_assist_lv = round(total_att_assist / total_pass, 2) * 100
        goal_assist_lv = round(goal_assist / total_pass, 2) * 100
    else:
        accurate_pass_lv = 0
        total_att_assist_lv = 0
        goal_assist_lv = 0
    data = [
        {'value': total_pass, 'name': 'Total Passes', 'c': '{}%'.format(total_pass_lv)},
        {'value': accurate_pass, 'name': 'Pass Success', 'c': '{}%'.format(accurate_pass_lv)},
        {'value': total_att_assist, 'name': 'Key Passes', 'c': '{}%'.format(total_att_assist_lv)},
        {'value': goal_assist, 'name': 'Assists', 'c': '{}%'.format(goal_assist_lv)},
    ]
    return jsonify(data), {'Content-Type': 'application/json'}

# 获取Offensive
@app.route('/offensive')
def offensive():
    nid = int(request.args.get("nid", 932))
    tid = int(request.args.get("tid", 1))
    df = pd.read_csv('player_all.csv')
    lists = df[(df['mins_played'] > 300) & (df['sl_team_id'] == nid)].to_dict(orient='records')
    data = {'xAxisData': [], 'goals': [], 'shots_on_target': [], 'total_shots': []}
    for item in lists:
        times = item['times']
        goals = item['goals']
        shots_on_target = item['ontarget_scoring_att']-item['goals']
        total_shots = item['total_scoring_att'] - item['ontarget_scoring_att']
        if goals > 0 or shots_on_target > 0 or total_shots > 0:
            data['xAxisData'].append(item['player_name'])
            if tid == 1:
                data['goals'].append(goals)
                data['shots_on_target'].append(shots_on_target)
                data['total_shots'].append(total_shots)
            else:
                data['goals'].append(goals/times)
                data['shots_on_target'].append(shots_on_target/times)
                data['total_shots'].append(total_shots/times)

    return jsonify(data), {'Content-Type': 'application/json'}

# 获取comprehensive
@app.route('/comprehensive')
def comprehensive():
    nid = int(request.args.get("nid", 932))
    tid = int(request.args.get("tid", 1))
    player_id = int(request.args.get("playerid", 0))
    df = pd.read_csv('player_all.csv')
    if player_id > 0:
        lists = df[(df['player_id'] == player_id)]
    else:
        lists = df[(df['mins_played'] > 300) & (df['sl_team_id'] == int(nid))]

    player_names = lists['player_name'].to_list()
    lists = lists.to_dict(orient='records')
    infos = []
    for item in lists:
        if tid == 1:
            #Break Through
            won_contest = item['won_contest']
            total_contest = item['total_contest']
            if total_contest > 0:
                won_contest_lv = round(won_contest / total_contest, 2) * 100
            else:
                won_contest_lv = 0

            #Fouls
            fouls = item['fouls']

            #Fouled
            fouled = item['was_fouled']

            #Clearances
            total_clearance = item['total_clearance']

            #Tackles
            won_tackle = item['won_tackle']
            total_tackle = item['total_tackle']
            if total_tackle > 0:
                won_tackle_lv = round(won_tackle / total_tackle, 2) * 100
            else:
                won_tackle_lv = 0
        else:
            times = item['times']
            # Break Through
            won_contest = round(item['won_contest']/times, 2)
            total_contest = round(item['total_contest']/times, 2)
            if total_contest > 0:
                won_contest_lv = round(won_contest/total_contest, 2) * 100
            else:
                won_contest_lv = 0

            # Fouls
            fouls = round(item['fouls']/times, 2)

            # Fouled
            fouled = round(item['was_fouled']/times, 2)

            # Clearances
            total_clearance =  round(item['total_clearance']/times, 2)

            # Tackles
            won_tackle = round(item['won_tackle']/times, 2)
            total_tackle = round(item['total_tackle']/times, 2)
            if total_tackle > 0:
                won_tackle_lv = round(won_tackle/total_tackle, 2) * 100
            else:
                won_tackle_lv = 0

        c = [won_contest_lv, 0, 0, 0, won_tackle_lv]
        value = [won_contest, fouls, fouled, total_clearance, won_tackle]
        infos.append({
            "c": c,
            "value": value,
            "name": item['player_name']
        })

    data = {
        'legend': player_names,
        'data': infos,
    }
    return jsonify(data), {'Content-Type': 'application/json'}

# 获取关键球员
@app.route('/keyplayer')
def keyPlayer():
    nid = int(request.args.get("nid", 932))
    df = pd.read_csv('player_all.csv')
    lists = df[(df['mins_played'] > 300) & (df['sl_team_id'] == int(nid))]
    player_names = []
    lists = lists.to_dict(orient='records')
    info = {
        'averageGoals': [],
        'averageGoalsMax': 0,
        'averageGoalsMin': 1000,
        'averageAssists': [],
        'averageAssistsMax': 0,
        'averageAssistsMin': 1000,
        'averageKeyPasses': [],
        'averageKeyPassesMax': 0,
        'averageKeyPassesMin': 1000,
        'averageBreakThrough': [],
        'averageBreakThroughMax': 0,
        'averageBreakThroughMin': 1000,
        'averageClearance': [],
        'averageClearanceMax': 0,
        'averageClearanceMin': 1000,
        'averageTackle': [],
        'averageTackleMax': 0,
        'averageTackleMin': 1000,
        'averagePasses': [],
        'averagePassesMax': 0,
        'averagePassesMin': 1000,
        'averagePassSuccess': [],
        'averagePassSuccessMax': 0,
        'averagePassSuccessMin': 1000,
    }


    for i in range(len(lists)):
        if lists[i]['averageGoals'] > 0 or lists[i]['averageAssists'] > 0 or lists[i]['averageKeyPasses'] > 0 or lists[i]['averageBreakThrough'] > 0 or lists[i]['averageClearance'] > 0 or lists[i]['averageTackle'] > 0 or lists[i]['averagePasses'] > 0 or lists[i]['averagePassSuccess'] > 0:
            player_names.append(lists[i]['player_name'])
            averageGoals = [0, i, lists[i]['averageGoals']]
            averageAssists = [1, i, lists[i]['averageAssists']]
            averageKeyPasses = [2, i, lists[i]['averageKeyPasses']]
            averageBreakThrough = [3, i, lists[i]['averageBreakThrough']]
            averageClearance = [4, i, lists[i]['averageClearance']]
            averageTackle = [5, i, lists[i]['averageTackle']]
            averagePasses = [6, i, lists[i]['averagePasses']]
            averagePassSuccess = [7, i, lists[i]['averagePassSuccess']]

            if lists[i]['averageGoals'] > info['averageGoalsMax']:
                info['averageGoalsMax'] = lists[i]['averageGoals']
            if lists[i]['averageAssists'] > info['averageAssistsMax']:
                info['averageAssistsMax'] = lists[i]['averageAssists']
            if lists[i]['averageKeyPasses'] > info['averageKeyPassesMax']:
                info['averageKeyPassesMax'] = lists[i]['averageKeyPasses']
            if lists[i]['averageBreakThrough'] > info['averageBreakThroughMax']:
                info['averageBreakThroughMax'] = lists[i]['averageBreakThrough']
            if lists[i]['averageClearance'] > info['averageClearanceMax']:
                info['averageClearanceMax'] = lists[i]['averageClearance']
            if lists[i]['averageTackle'] > info['averageTackleMax']:
                info['averageTackleMax'] = lists[i]['averageTackle']
            if lists[i]['averagePasses'] > info['averagePassesMax']:
                info['averagePassesMax'] = lists[i]['averagePasses']
            if lists[i]['averagePassSuccess'] > info['averagePassSuccessMax']:
                info['averagePassSuccessMax'] = lists[i]['averagePassSuccess']


            if lists[i]['averageGoals'] < info['averageGoalsMin']:
                info['averageGoalsMin'] = lists[i]['averageGoals']
            if lists[i]['averageAssists'] < info['averageAssistsMin']:
                info['averageAssistsMin'] = lists[i]['averageAssists']
            if lists[i]['averageKeyPasses'] < info['averageKeyPassesMin']:
                info['averageKeyPassesMin'] = lists[i]['averageKeyPasses']
            if lists[i]['averageBreakThrough'] < info['averageBreakThroughMin']:
                info['averageBreakThroughMin'] = lists[i]['averageBreakThrough']
            if lists[i]['averageClearance'] < info['averageClearanceMin']:
                info['averageClearanceMin'] = lists[i]['averageClearance']
            if lists[i]['averageTackle'] < info['averageTackleMin']:
                info['averageTackleMin'] = lists[i]['averageTackle']
            if lists[i]['averagePasses'] < info['averagePassesMin']:
                info['averagePassesMin'] = lists[i]['averagePasses']
            if lists[i]['averagePassSuccess'] < info['averagePassSuccessMin']:
                info['averagePassSuccessMin'] = lists[i]['averagePassSuccess']


            info['averageGoals'].append(averageGoals)
            info['averageAssists'].append(averageAssists)
            info['averageKeyPasses'].append(averageKeyPasses)
            info['averageBreakThrough'].append(averageBreakThrough)
            info['averageClearance'].append(averageClearance)
            info['averageTackle'].append(averageTackle)
            info['averagePasses'].append(averagePasses)
            info['averagePassSuccess'].append(averagePassSuccess)


    keyLists = df[(df['times'] >= 4) & (df['sl_team_id'] == int(nid)) & (df['is_key'] == 1)].to_dict(orient='records')
    keys = []
    for key in keyLists:
        keys.append('<a href="/info?playerid={}&nid={}">{}</a>'.format(key['player_id'], key['sl_team_id'], key['player_name']))
    data = {
        'player': player_names,
        'data': info,
        'html': ', '.join(keys),
        'keyLists': keyLists
    }
    return jsonify(data), {'Content-Type': 'application/json'}


@app.route('/info')
def info():
    playerid = int(request.args.get("playerid", 132015))
    nid = int(request.args.get("nid", 932))
    return render_template('info.html', playerid=playerid, nid=nid)


# 初始化球员和比赛信息
@app.route('/team')
def team():
    player_id = request.args.get("player_id", "0")
    config = get_config()
    teams = config['teams']
    for i in range(len(teams)):
        matches = []
        for matche in config['matches']:
            if teams[i]['id'] == matche['teamId']:
                matches.append(matche)
        teams[i]['matches'] = matches

    if player_id != "0":
        data = None
        for team in teams:
            if team['player_id'] == player_id:
                data = team
                break
        return jsonify(data), {'Content-Type': 'application/json'}
    else:
        return jsonify(teams), {'Content-Type': 'application/json'}

# 初始化比赛信息
@app.route('/matche')
def matche():
    config = get_config()
    nid = request.args.get("nid", "932")
    matches = []
    for matche in config['matches']:
        if nid == matche['teamId']:
            matches.append(matche)
    return jsonify(matches), {'Content-Type': 'application/json'}


# 折线图数据
@app.route('/infoLine')
def infoLine():
    config = get_config()
    nid = request.args.get("nid", "932")
    player_id = request.args.get("playerid", "0")
    xAxis = []
    ontarget_scoring_att = []
    total_att_assist = []
    won_contest = []
    was_fouled = []
    won_tackle = []
    total_clearance = []
    accurate_pass = []
    df = pd.read_csv('./player_info.csv')
    for matche in config['matches']:
        if nid == matche['teamId']:
            player = df[(df['player_id'] == int(player_id)) & (df['config_match_id'] == int(matche['id']))].to_dict(orient='records')[0]
            xAxis.append(matche['date'])
            ontarget_scoring_att.append(player['ontarget_scoring_att'])
            total_att_assist.append(player['total_att_assist'])
            won_contest.append(player['won_contest'])
            was_fouled.append(player['was_fouled'])
            won_tackle.append(player['won_tackle'])
            total_clearance.append(player['total_clearance'])
            accurate_pass.append(player['accurate_pass'])

    re = {'xAxis': xAxis, 'data': [
        {"name": 'Shot on target', "type": 'line', "stack": 'all', "data": ontarget_scoring_att},
        {"name": 'Assists', "type": 'line', "stack": 'all', "data": total_att_assist},
        {"name": 'Contests', "type": 'line', "stack": 'all', "data": won_contest},
        {"name": 'Fouled', "type": 'line', "stack": 'all', "data": was_fouled},
        {"name": 'Tackles', "type": 'line', "stack": 'all', "data": won_tackle},
        {"name": 'Clearances', "type": 'line', "stack": 'all', "data": total_clearance},
        {"name": 'Successful Passes', "type": 'line', "stack": 'all', "data": accurate_pass}
    ]}
    return jsonify(re), {'Content-Type': 'application/json'}

# 获取热力图数据
@app.route('/hotmap')
def hotmap():
    matche_id = request.args.get("matche_id")
    player_id = request.args.get("player_id")
    url = 'https://api.sports.sina.com.cn/?p=sports&s=sport_client&a=index&_sport_t_=livecast&_sport_a_=heatmap&match_id={}&player_id={}'.format(matche_id, player_id)
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        res_json = res.json()
        data = res_json['result']['data']
        lists = []
        if len(data) > 0:
            try:
                for i in range(len(data)):
                    lists.append({
                        'x': data[i]['y'] * 3.44 + 8,
                        'y': data[i]['x'] * 5.14 + 23,
                        'value': 30
                    })
                return jsonify(lists), {'Content-Type': 'application/json'}
            except:
                return jsonify([{"x": 0, "y": 0, "value": 0}]), {'Content-Type': 'application/json'}
        else:
            return jsonify([{"x": 0, "y": 0, "value": 0}]), {'Content-Type': 'application/json'}
    else:
        print('新浪未返回数据，可能被反扒了！')
        return jsonify([{"x": 0, "y": 0, "value": 0}]), {'Content-Type': 'application/json'}


# 获取行动图数据
@app.route('/action')
def action():
    matche_id = request.args.get("matche_id")
    player_id = request.args.get("player_id")
    at = request.args.get("at")
    url = 'http://api.sports.sina.com.cn/?p=sports&s=sport_client&a=index&_sport_t_=livecast&_sport_a_=eventDetails&match_id={}&player_id={}'.format(matche_id, player_id)
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        res_json = res.json()
        data = res_json['result']['data']
        if len(data) > 0:
            if len(at) > 0:
                at = at.split(',')
                lists = []
                for d in data:
                    print(str(d['type']), )
                    if str(d['type']) in at:
                        lists.append(d)
                return jsonify(lists), {'Content-Type': 'application/json'}
            else:
                return jsonify(data), {'Content-Type': 'application/json'}
        else:
            return jsonify([{"x": 0, "y": 0, "value": 0}]), {'Content-Type': 'application/json'}
    else:
        print('新浪未返回数据，可能被反扒了！')
        return jsonify([{"sx":0,"sy":0,"ex":0,"ey":0,"type":0}]), {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run()