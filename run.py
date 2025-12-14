import os
import paramiko
import requests
import json
from datetime import datetime, timezone, timedelta

sckey = os.getenv('SCKEY', '')


def ssh_multiple_connections(hosts_info, command):
    users = []
    hostnames = []
    for host_info in hosts_info:
        hostname = host_info['hostname']
        username = host_info['username']
        password = host_info['password']
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=22, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command)
            user = stdout.read().decode().strip()
            users.append(user)
            hostnames.append(hostname)
            ssh.close()
        except Exception as e:
            print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
    return users, hostnames

ssh_info_str = os.getenv('SSH_INFO', '[]')
hosts_info = json.loads(ssh_info_str)

command = 'whoami'
user_list, hostname_list = ssh_multiple_connections(hosts_info, command)
user_num = len(user_list)
content = "SSH服务器登录信息：\n"
for user, hostname in zip(user_list, hostname_list):
    content += f"用户名：{user}，服务器：{hostname}\n"
beijing_timezone = timezone(timedelta(hours=8))
time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')
loginip = requests.get('https://api.ipify.org?format=json').json()['ip']
content += f"本次登录用户共： {user_num} 个\n登录时间：{time}\n登录IP：{loginip}"


def server_send(msg):
    if sckey == '':
        print("未配置SCKEY，跳过推送")
        return
    server_url = "https://sctapi.ftqq.com/" + str(sckey) + ".send"
    data = {
        'text': msg,
        'desp': msg
    }
    try:
        response = requests.post(server_url, data=data)
        if response.status_code == 200:
            print("推送成功")
        else:
            print(f"推送失败，状态码：{response.status_code}，响应：{response.text}")
    except Exception as e:
        print(f"推送异常：{e}")


server_send(content)
