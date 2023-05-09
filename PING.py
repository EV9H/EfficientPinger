import requests
import time
from datetime import datetime

import asyncio
import aiohttp


ADDR_sample = ['https://www.google.com','https://www.amazon.com', 'https://www.bing.com' ]

class Pinger:
    URL_LIST = []
    def __init__(self):
        self.START = False
    
    def add_URL(self, input):
        self.URL_LIST.append(self.URL(input))
    def add_URL_list(self, l):
        for i in l:
            self.URL_LIST.append(self.URL(i))
    def get_URL_LIST(self):
        return self.URL_LIST
    def print_URL_LIST(self):
        for l in self.URL_LIST:
            print(l)
    
    def ping(self, URL, timeout = 1):
        response = requests.get(URL.address, timeout = timeout)
        return response
    
    def start(self, tries = 5,  delay = 1, mode = "show"):
        self.START = True
        if len(self.URL_LIST) == 0 :
            print("Empty URL targets")
            return -1 
        cnt = 0
        report = ""
        if mode == "show":
            while self.START:
                print(f'{datetime.now().strftime("%Y/%M/%D: %H:%M:%S")} ======================= ({cnt+1}/{tries})')
                for u in self.URL_LIST:
                    output = f"------ {u.address}  "
                    try:
                        response = self.ping(u)
                        ms_elapsed = int(response.elapsed.total_seconds() * 1000)
                        u.ping_list.append(ms_elapsed)
                        output = f'{output:40s} | ping: {ms_elapsed:4.0f} | avg: {u.get_avg_ping():4.2f}'
                    except requests.exceptions.Timeout as e:
                        output = f'{output:20s} | timeout ( ms)'
                    except requests.exceptions.RequestException as e:
                        output = f'{output:20s} | no internet'
                    
                    print(output)
                    

                time.sleep(delay)  

                cnt += 1
                if(cnt >= tries):
                    self.START = False
        elif mode == "not-show":
            while self.START:
                for u in self.URL_LIST:
                    try:
                        response = self.ping(u)
                        ms_elapsed = int(response.elapsed.total_seconds() * 1000)
                        u.ping_list.append(ms_elapsed)
                    except requests.exceptions.Timeout as e:
                        pass
                    except requests.exceptions.RequestException as e:
                        pass
                time.sleep(delay)  
                cnt += 1
                if(cnt >= tries):
                    self.START = False
        for u in self.URL_LIST:
            report += f"{u} avg: {u.get_avg_ping():4.2f} \n"
        print(report)

    async def get(self,url, session):
        try: 
            t_0 = time.monotonic()
            async with session.get(url = url.address) as response:
                res = await response.release()
            response_time = time.monotonic() - t_0
            url.ping_list.append(response_time) 
            print(f'{str(url):40s} | response_time = {response_time*1000:4.0f}ms | avg:{url.get_avg_ping() * 1000:4.0f}ms')
            return res
        except Exception as e:
            print(str(e))
            
            
    async def main(self,urls, wait):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                tasks.append(
                    self.get(url, session)
                )
            ret = await asyncio.gather(*tasks)
            await asyncio.sleep(wait)
            
            
            # ret = await asyncio.gather(*[self.get(url, session) for url in urls])
    
    def begin(self, loop = 10, wait = 1):
        for i in range(loop):
            asyncio.run(self.main(self.URL_LIST, wait))
            print(' ----- ')
        now = datetime.now().strftime("%H:%M:%S")
        report = f"========= REPORT (finished on {now}) =========\n"
        for u in self.URL_LIST:
            report += (f"{str(u):40s} average response time: {u.get_avg_ping()*1000:4.0f}ms \n")
        print(report)
            
    class URL:
        def __init__(self, address):
            self.address = address
            self.avg = None   
            self.ping_list = []
        def get_avg_ping(self):
            if(len(self.ping_list)> 0):
                return( sum(self.ping_list) / len(self.ping_list))
            return 0 
        def __str__(self) -> str:
            return self.address
        

            
PINGER = Pinger()
PINGER.add_URL_list(ADDR_sample)
# PINGER.print_URL_LIST()

#PINGER.start(tries= 5, delay = 0.1, mode = "not-show")

#PINGER.start(tries= 5, delay = 0.1, mode = "show")

urls = PINGER.URL_LIST

# start = time.time()
# asyncio.run(PINGER.main(urls))
# end = time.time()
# print("Took {} seconds to pull {} websites.".format(end - start, len(urls)))

PINGER.begin(wait = 0.2)