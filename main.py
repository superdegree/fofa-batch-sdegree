import base64
import os
import requests
from config import FOFA_EMAIL, FOFA_KEY  # 导入 email 和 key

class FofaAPI(object):
    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.base_url = 'https://fofa.info'
        self.search_api_url = '/api/v1/search/all'
        self.login_api_url = '/api/v1/info/my'
        self.get_userinfo()

    def get_userinfo(self):
        try:
            url = '{url}{api}'.format(url=self.base_url, api=self.login_api_url)
            data = {"email": self.email, 'key': self.key}
            req = requests.get(url, params=data)
            return req.json()
        except requests.exceptions.ConnectionError:
            error_msg = {"error": True, "errmsg": "Connect error"}
            return error_msg

    def get_data(self, query_str='', size=1000, page=1, fields='protocol,host,ip,port,title'):
        try:
            url = '{url}{api}'.format(url=self.base_url, api=self.search_api_url)
            query_str = bytes(query_str, 'utf-8')
            data = {'qbase64': base64.b64encode(query_str), 'email': self.email, 'key': self.key, 'page': page,
                    'size': size,
                    'fields': fields}
            req = requests.get(url, params=data, timeout=10)
            return req.json()
        except requests.exceptions.ConnectionError:
            error_msg = {"error": True, "errmsg": "Connect error"}
            return error_msg

def main():
    while True:
        choice = input("输入0删除'output.txt';\n输入1导入'ip.txt'进行批量查询;\n输入2手动输入你要执行的搜索语句;\n输入3退出;\n输入框: ")

        if choice == '0':
            if os.path.exists("output.txt"):
                os.remove("output.txt")
                print("output.txt已删除。")
            else:
                print("output.txt不存在。")

        elif choice == '1':
            # 从 ip.txt 文件中导入查询语句
            with open('ip.txt', 'r') as f:
                queries = f.readlines()
            email = FOFA_EMAIL  # 使用从 config.py 文件导入的 email
            key = FOFA_KEY  # 使用从 config.py 文件导入的 key
            fofa = FofaAPI(email, key)

            # 对每个查询语句进行操作
            results = []
            for query in queries:
                query = query.strip()  # 去除换行符等空白字符
                result = fofa.get_data(query)
                results.append(result)

            # 将结果保存在 output.txt 中
            with open('output.txt', 'w') as f:
                for result in results:
                    f.write(str(result) + '\n')

        elif choice == '2':
            # 手动输入查询语句
            queries = input("输入你的查询语句（注意:结果不会保存在output.txt中）: ").split('\n')
            email = FOFA_EMAIL  # 使用从 config.py 文件导入的 email
            key = FOFA_KEY  # 使用从 config.py 文件导入的 key
            fofa = FofaAPI(email, key)

            # 对每个查询语句进行操作
            results = []
            for query in queries:
                query = query.strip()  # 去除换行符等空白字符
                result = fofa.get_data(query)
                print(result)  # 直接输出结果

        elif choice == '3':
            print("程序已退出。")
            break

        else:
            print("Invalid choice. Please enter 0, 1, 2, or 3.")

if __name__ == "__main__":
    main()
