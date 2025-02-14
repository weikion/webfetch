import sys
import wx
import os
import json
import time
import requests
import socket
import asyncio
import websockets
import uuid
from io import BytesIO
from libs.login_ui import LoginUI
from multiprocessing import Process


def qrcode_task(session, session_id, status, username):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(request_qrcode(session, session_id, status, username))
    loop.close()

def check_ver(version):
    try:
        t = int(time.time())
        url = 'http://n-user.izb.pub/lZiNUBvTTQ4URe1m.php/ucenter/tool_api/check_ngzb_spider/?ver=%s&t=%d' % (version, t)
        res_byte = requests.get(url)
        json_data = res_byte.json()
        # print(json_data)
        if json_data['code'] == 0:
            return True
        else:
            return False
    except Exception:
        return False

async def request_qrcode(session, session_id, status, username):
    host = 'ws://n-app-admin.ngzb.com.cn/websocket/wx_login/%s' % session_id
    # host = "ws://localhost:9999"
    # print(host)
    async with websockets.connect(host) as websocket:
        recv_text = await websocket.recv()
        # print(f"{recv_text}")
        login_info = json.loads(recv_text)
        if login_info['code'] == 0:
            res_byte = session.post('http://n-app-admin.ngzb.com.cn/admin/wxLogin', {"token": login_info['token']})
            json_data = res_byte.json()
            # print(json_data)
            if json_data['code'] == 1:
                username['name'] = json_data['data']['manager']['name']
                status.value = 1


class LoginFrame(LoginUI):
    def __init__(self, parent, complete_callback, about, session, login_status, login_username):
        LoginUI.__init__(self, parent)
        self.icon = wx.Icon('icon.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon)
        self.callback = complete_callback  # 回调主窗口
        self.about = about  # 关于软件参数
        self.request = session  # 会话句柄
        self.qr_mp = None  # 二维码线程
        self.session_id = None  # 会话session_id
        self.login_status = login_status
        self.login_username = login_username

        # 检查软件版本
        if not check_ver(self.about['version']):
            box = wx.MessageDialog(None, '该版本太旧了，请下载最新版本！', u'提示', wx.OK)
            box.ShowModal()
            box.Destroy()
            self.Destroy()
            sys.exit()

        if os.path.exists('login.json'):
            f = open('login.json', mode='r', encoding='utf-8')
            content = f.read()
            if content:
                login_info = json.loads(content)
                self.username.SetValue(login_info['username'])
                self.password.SetValue(login_info['password'])
            f.close()

    def account_login(self, event):
        self.login_mode_1.Show()
        self.login_mode_2.Hide()
        self.qr_mp.terminate()
        self.m_timer1.Stop()

    def login(self, event):
        # ====================认证开始====================
        # 登录
        aes_key = 'wNFzRNEY4GjHx8wn'
        bet_name = self.about['name']
        version = self.about['version']

        # 获取主机名
        hostname = socket.gethostname()
        # 获取IP
        ip = socket.gethostbyname(hostname)
        # 获取mac
        mac = get_mac_address()
        # cpu 序列号
        cpu_sn = ''

        username = self.username.GetValue()
        password = self.password.GetValue()

        json_data = {}
        try:
            t = int(time.time())
            url = 'http://n-app-admin.ngzb.com.cn/admin/phpLogin?username=%s&password=%s&t=%d' % (username, password, t)
            res_byte = self.request.get(url)
            json_data = res_byte.json()
            # print(json_data)
            if json_data['code'] == 1:
                json_data['error'] = 0
            else:
                json_data['error'] = 3
            json_data['expires'] = '2025-1-1'
        except Exception:
            json_data['error'] = 99

        if json_data['error'] != 0:
            msg = '未知错误！'
            if json_data['error'] == 1:
                msg = '软件过期或者不可用！'
            elif json_data['error'] == 2:
                msg = '用户不存在！'
            elif json_data['error'] == 3:
                msg = '账户密码错误！'
            elif json_data['error'] == 4:
                msg = '该账户已经登录！'
            elif json_data['error'] == 99:
                msg = '网络错误！'

            box = wx.MessageDialog(None, msg, u'提示', wx.OK)
            box.ShowModal()
            box.Destroy()
        else:
            if self.remember.IsChecked():
                f = open('login.json', mode='w', encoding='utf-8')
                f.write(json.dumps({'username': username, 'password': password}))
                f.flush()  # 刷新. 养成好习惯
                f.close()
            else:
                f = open('login.json', mode='w', encoding='utf-8')
                f.write('')
                f.flush()  # 刷新. 养成好习惯
                f.close()

            main_win = self.callback(None, username, json_data['expires'])
            main_win.SetTitle(main_win.GetTitle() + '-' + version)
            main_win.Show()  # 显示主窗口
            self.Destroy()
        # ====================认证结束====================

    def qrcode_login(self, event):
        if not self.session_id:
            response = self.request.get("http://n-app-admin.ngzb.com.cn/admin/wxLoginQrCode")
            session_id = response.cookies.get('JSESSIONID')
            image = wx.Image(BytesIO(response.content))
            bitmap = image.ConvertToBitmap()
            self.m_qrcode.SetBitmap(bitmap)
            self.session_id = session_id

        self.m_timer1.Start(1000)

        self.login_mode_1.Hide()
        self.login_mode_2.Show()

        # 打开socket
        self.qr_mp = Process(target=qrcode_task,
                             args=(self.request, self.session_id, self.login_status, self.login_username,))
        self.qr_mp.daemon = True
        self.qr_mp.start()

    def close(self, event):
        self.Destroy()
        sys.exit()

    def timer_func(self, event):
        # print(self.login_status.value, self.login_username)
        if self.login_status.value == 1:
            version = self.about['version']
            main_win = self.callback(None, self.login_username['name'], '2025-1-1')
            main_win.SetTitle(main_win.GetTitle() + '-' + version)

            # 显示主窗口
            main_win.Show()

            # 停止计时器
            self.m_timer1.Stop()

            # 二维码登录成功，关闭扫码线程
            self.qr_mp.terminate()

            # 注销当前窗口
            self.Destroy()


# 获取Mac地址
def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e + 2] for e in range(0, 11, 2)])
