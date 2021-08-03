# coding=utf-8
# 运行spider.py文件获取球员5场比赛的数据并进行清洗
import os
import json
import requests
import pandas as pd

HEADERS = {
    'Cookie': 'UOR=www.baidu.com,sports.sina.com.cn,; SINAGLOBAL=116.52.95.172_1625447206.451082; U_TRS1=000000ac.997c24cf.60e25da3.b26c7722; UM_distinctid=17a7449adb7e4f-0981a7314c4faa-34647600-384000-17a7449adb81130; __gads=ID=d40ebe68a6fad7e9-225bd0182fca00b7:T=1625448627:RT=1625448627:S=ALNI_MYRhHxOp53MwqIy4DvF6oAwmTLwag; U_TRS2=0000008b.2bf786be.60e3ceff.71a3b4da; Apache=222.221.182.139_1625554151.131443; ULV=1625554154771:4:4:4:222.221.182.139_1625554151.131443:1625554150912; Hm_lvt_35ddcac55ce8155015e5c5e313883b68=1625447205,1625536280,1625563490; vjuids=3ae3e213b.17a7e8cfc20.0.9b306541456a4; vjlast=1625620807; hqEtagMode=1; Hm_lpvt_35ddcac55ce8155015e5c5e313883b68=1625624240',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}


# 在指定的csv文件中添加数据
def to_csv(name, show_list):
    df = pd.DataFrame(show_list)
    df.to_csv('./{}.csv'.format(name), mode='a', header=True, index=False, encoding='utf-8-sig')


# 获取配置文件
def get_config():
    with open('./config.json', encoding='utf-8') as f:
        config = json.loads(f.read())
        return config


# 发起请求
def set_requests(url):
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res
    else:
        return set_requests(url)

# 每次运行先删除之前生成的球员数据
def delete(filename):
    if os.path.exists('./{}.csv'.format(filename)):
        os.remove('./{}.csv'.format(filename))

# 获取比赛中球员成绩
def run():
    player_name_position_info = pd.read_excel('./player_name_position_info.xls')
    filename = 'player_info'
    delete(filename)
    config = get_config()
    show_list = []
    for team in config['teams']:
        for match in config['matches']:
            teamId = team['id']
            if teamId == match['teamId']:
                print(team['name'], match['name'], '...')
                url = 'https://api.sports.sina.com.cn/?p=sports&s=sport_client&a=index&_sport_t_=football&_sport_s_=opta&_sport_a_=matchplayerstatics&id={}'.format(
                    match['id'])
                print(url)
                res = set_requests(url)
                res_json = res.json()
                player_list = res_json['result']['data'][teamId]
                for player_id in player_list:
                    player_info = player_list[player_id]
                    criteria = (player_name_position_info['player_name_cn'] == player_info['player_name_cn'])
                    position_info = player_name_position_info[criteria].to_dict(orient='records')[0]
                    player_info['player_name_en'] = position_info['player_name']
                    player_info['position_en'] = position_info['position']
                    player_info['config_match_id'] = match['id']
                    player_info['nationality'] = team['name']
                    show_list.append(player_info)
    to_csv(filename, show_list)


# 数据清洗合并
def do():
    df = pd.read_csv('./player_info.csv')
    d = df.to_dict(orient='records')
    player_ids = []
    lists = {}
    for item in d:
        if item['mins_played'] > 0:
            if item['player_id'] not in player_ids:
                player_ids.append(item['player_id'])
                lists[item['player_id']] = {
                    'times': 1,  # 比赛场次
                    'player_id': item['player_id'], # 球员id
                    'sl_team_id': item['sl_team_id'], # 球员所属国家
                    'match_id': [item['match_id']], # 球员比赛id
                    'player_name': item['player_name_en'], # 球员名字
                    'position_en': item['position_en'], # 球员位置
                    'nationality': item['nationality'],
                    'shirt_number': item['shirt_number'],  # shirt_number
                    'total_scoring_att': item['total_scoring_att'],
                    'ontarget_scoring_att': item['ontarget_scoring_att'],
                    'goals': item['goals'],
                    'goal_assist': item['goal_assist'],
                    'total_att_assist': item['total_att_assist'],
                    'total_contest': item['total_contest'],
                    'won_contest': item['won_contest'],
                    'fouls': item['fouls'], #犯规数
                    'was_fouled': item['was_fouled'], #被犯规数
                    'total_clearance': item['total_clearance'], # 总解围数
                    'saves': item['saves'],
                    'won_tackle': item['won_tackle'], #成功抢断数
                    'total_tackle': item['total_tackle'], #总抢断数
                    'accurate_pass': item['accurate_pass'], #精准传球
                    'total_pass': item['total_pass'], #总传球
                    'mins_played': item['mins_played'], #上场时间 分钟
                }
            else:
                lists[item['player_id']]['times'] = lists[item['player_id']]['times'] + 1
                lists[item['player_id']]['match_id'].append(item['match_id'])
                lists[item['player_id']]['total_scoring_att'] = lists[item['player_id']]['total_scoring_att'] + item['total_scoring_att']
                lists[item['player_id']]['ontarget_scoring_att'] = lists[item['player_id']]['ontarget_scoring_att'] + item['ontarget_scoring_att']
                lists[item['player_id']]['goals'] = lists[item['player_id']]['goals'] + item['goals']
                lists[item['player_id']]['goal_assist'] = lists[item['player_id']]['goal_assist'] + item['goal_assist']
                lists[item['player_id']]['total_att_assist'] = lists[item['player_id']]['total_att_assist'] + item['total_att_assist']
                lists[item['player_id']]['total_contest'] = lists[item['player_id']]['total_contest'] + item['total_contest']
                lists[item['player_id']]['won_contest'] = lists[item['player_id']]['won_contest'] + item['won_contest']
                lists[item['player_id']]['fouls'] = lists[item['player_id']]['fouls'] + item['fouls']
                lists[item['player_id']]['was_fouled'] = lists[item['player_id']]['was_fouled'] + item['was_fouled']
                lists[item['player_id']]['total_clearance'] = lists[item['player_id']]['total_clearance'] + item['total_clearance']
                lists[item['player_id']]['saves'] = lists[item['player_id']]['saves'] + item['saves']
                lists[item['player_id']]['won_tackle'] = lists[item['player_id']]['won_tackle'] + item['won_tackle']
                lists[item['player_id']]['total_tackle'] = lists[item['player_id']]['total_tackle'] + item['total_tackle']
                lists[item['player_id']]['accurate_pass'] = lists[item['player_id']]['accurate_pass'] + item['accurate_pass']
                lists[item['player_id']]['total_pass'] = lists[item['player_id']]['total_pass'] + item['total_pass']
                lists[item['player_id']]['mins_played'] = lists[item['player_id']]['mins_played'] + item['mins_played']

    filename = 'player_all'
    delete(filename)
    show_list = []
    for p in lists:
        show_list.append(lists[p])
    to_csv(filename, show_list)


# 关键球员计算
def keyPlayer():
    df = pd.read_csv('./player_all.csv')
    config = get_config()
    lists = []
    for team in config['teams']:
        plist = df[(df['sl_team_id'] == int(team['id']))].to_dict(orient='records')
        for item in plist:
            times = item['times']
            if item['mins_played'] > 300:
                averageGoals = round(item['goals'] / times, 2)
                averageAssists = round(item['goal_assist'] / times, 2)
                averageKeyPasses = round(item['total_att_assist'] / times, 2)
                averageBreakThrough = round(item['won_contest'] / times, 2)
                averageClearance = round(item['total_clearance'] / times, 2)
                averageTackle = round(item['won_tackle'] / times, 2)
                averagePasses = round(item['accurate_pass'] / times, 2)
                if item['total_pass'] > 0:
                    averagePassSuccess = round((item['accurate_pass'] / times) / (item['total_pass'] / times),2)
                else:
                    averagePassSuccess = 0
            else:
                averageGoals = 0
                averageAssists = 0
                averageKeyPasses = 0
                averageBreakThrough = 0
                averageClearance = 0
                averageTackle = 0
                averagePasses = 0
                averagePassSuccess = 0

            item['averageGoals'] = averageGoals
            item['averageAssists'] = averageAssists
            item['averageKeyPasses'] = averageKeyPasses
            item['averageBreakThrough'] = averageBreakThrough
            item['averageClearance'] = averageClearance
            item['averageTackle'] = averageTackle
            item['averagePasses'] = averagePasses
            item['averagePassSuccess'] = averagePassSuccess
            lists.append(item)

    delete('player_all')
    to_csv('player_all', lists)

    df = pd.read_csv('player_all.csv')

    show_list = []
    for team in config['teams']:
        plist = df[(df['sl_team_id'] == int(team['id']))].to_dict(orient='records')
        cl = ['averageGoals', 'averageAssists', 'averageKeyPasses', 'averageBreakThrough', 'averageClearance', 'averageTackle', 'averagePasses', 'averagePassSuccess']
        for c in cl:
            plist = sorted(plist, key=lambda i: i[c], reverse=True)
            for i in range(len(plist)):
                if i == 0:
                    fen = 3
                elif i == 1:
                    if plist[1][c] == plist[0][c]:
                        fen = 3
                    else:
                        fen = 2
                elif i == 2:
                    if plist[2][c] == plist[0][c]:
                        fen = 3
                    elif plist[2][c] == plist[1][c]:
                        fen = 2
                    else:
                        fen = 1
                else:
                    fen = 0
                plist[i][f'{c}_fen'] = fen


        for i in range(len(plist)):
            plist[i]['total_fen'] = plist[i]['averageGoals_fen']+plist[i]['averageAssists_fen']+plist[i]['averageKeyPasses_fen']+plist[i]['averageBreakThrough_fen']+plist[i]['averageClearance_fen']+plist[i]['averageTackle_fen']+plist[i]['averagePasses_fen']+plist[i]['averagePassSuccess_fen']

        total_fens = [item['total_fen'] for item in plist]
        total_fen_max = max(total_fens)
        for item in plist:
            if item['total_fen'] == total_fen_max:
                item['is_key'] = 1
            else:
                item['is_key'] = 0
            show_list.append(item)

    delete('player_all')
    to_csv('player_all', show_list)


if __name__ == '__main__':
    # print('爬虫开始...')
    # run()
    print('爬虫结束，正在清洗并合并数据...')
    do()
    print('数据清洗结束，正在计算关键球员...')
    keyPlayer()
    print('数据准备结束')