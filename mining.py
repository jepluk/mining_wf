import requests as r
import json, re, random, time, pickle
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

soup = lambda x: BeautifulSoup(x, 'html.parser')

class Mission:
    def __init__(self, session) -> None:
        self.session = session
        self.session.headers.update({'Accept': '*/*','Accept-Encoding': 'gzip, deflate','Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7','Connection': 'keep-alive','Content-Type': 'application/x-www-form-urlencoded','Host': 'kingdomlikes.com','Referer': 'https://kingdomlikes.com/free_points/facebook-followers','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36','X-Requested-With': 'XMLHttpRequest','sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Linux"'})
        self.base = 'https://kingdomlikes.com/'

    def tasks(self, idtype: int) -> tuple:
        try:
            source = self.session.get(self.base +'/free_points/facebook-likes').text
            params = {'idtype': idtype, 'order': str(random.randrange(1, 9)),'token': re.search(r'name="_token" value="(.*?)"', source).group(1),'session': re.search(r'"(.*?=)";', source).group(1),'addon': 'false'}
            send = self.session.get(self.base +'free_points/page3', params=params).json()
        except: 
            send = []
        
        if len(send) != 0: 
            return self.work(send[0], params['token'], params['session'])
        else:
            return (False, None, None)

    def work(self, task_data: dict, token: str, session: str) -> tuple:
        params = {'token': task_data['idef'],'type': '4','csf': token,'addon': 'false'}
        count_ = self.session.get(self.base +'free_points/count', params=params).json()

        if count_['success']:
            payload = {'token': count_['count'],'id': params['token'],'check': '0','csf': token,'session': session,'addon': 'false','value': 'false','addonversion': '','type': '4'}
            send = self.session.post(self.base +'free_points/check4', data=payload).json()
            try:
                if send['success']:
                    return (True, send['CPC'], send['points'])
            except KeyError:
                print(send)
                pass
        
        return (False, None, None)

acc = [pickle.loads(open('account1.ses', 'rb').read()), pickle.loads(open('account2.ses', 'rb').read())]
for i in acc:
    for x in range(23):
        status, rewards, balance = Mission(session=i).tasks(idtype=str(x))
        if status:
            print(str(balance) +' coin')
