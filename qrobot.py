from flask import Flask, request
import requests
'''这是导入的另一个文件，下面会讲到'''

app = Flask(__name__)


class API:
    @staticmethod
    def send(message, group_id):
        url = "http://127.0.0.1:5700/send_msg"
        params = {
            "message_type": 'group',
            "group_id": group_id,
            "message": message
        }
        requests.get(url, params=params)

    @staticmethod
    def get_jx3_kaifu(server, group_id):
        url = "https://www.jx3api.com/data/server/check"
        params = {
            "server": server
        }
        a = requests.get(url, params=params)

        if a.json()["data"]["status"] == 1:
            message = '服务器：[' + server + ']已开服'
        else:
            message = '服务器：[' + server + ']未开服'
        print(message)
        API.send(message, group_id)

    @staticmethod
    def get_jx3_richang(server, group_id):
        url = "https://www.jx3api.com/data/active/current"
        params = {
            "server": server
        }
        a = requests.get(url, params=params).json()["data"]

        message = '时间：' + a["date"] + "\n大战：" + a["war"] + "\n战场：" + a["battle"] + "\n宠物：" + a["luck"][0] + '，' + a["luck"][1] + '，' + a["luck"][2]
        print(message)
        API.send(message, group_id)

@app.route('/', methods=["POST"])
def post_data():
    """下面的request.get_json().get......是用来获取关键字的值用的，关键字参考上面代码段的数据格式"""
    data = request.get_json()
    print(data)
    if data['post_type'] == 'message':
        message = data['message']
        group_id = data['group_id']
        if message.startswith('小伍同学 '):
            print('放行')
            API.send()
        elif message.startswith('开服查询 '):
            server = message.split()[1]
            print(server, group_id)
            print('查询开服状态，放行')
            API.get_jx3_kaifu(server, group_id)
        elif message.startswith('日常查询 '):
            server = message.split()[1]
            print(server, group_id)
            print('查询日常，放行')
            API.get_jx3_richang(server, group_id)
        else:
            print(message, '，无关键字，不处理')
    else:
        print("暂不处理")

    return "OK"



if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置
    # server = pywsgi.WSGIServer(('0.0.0.0', 5700), app)
    # server.serve_forever()
    app.run(host='0.0.0.0', port=5708, debug=True)  # 保证和我们在配置里填的一致