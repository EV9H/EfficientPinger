import requests
import time
from datetime import datetime

import asyncio
import aiohttp

# TEST
BAD_SITES = []


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
        
class Pinger:
    URL_LIST = []
    def __init__(self):
        self.START = False
    
    # def add_URL(self, input):
    #     self.URL_LIST.append(self.URL(input))
    # def add_URL_list(self, l):
    #     for i in l:
    #         self.URL_LIST.append(self.URL(i))
    # def get_URL_LIST(self):
    #     return self.URL_LIST
    # def print_URL_LIST(self):
    #     for l in self.URL_LIST:
    #         print(l)
    '''
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
    '''
   

    async def get(self,url, session, fetch_timeout = 3):
        t_0 = time.monotonic()
        try: 
            
            async with session.get(url = "http://" + url.address, allow_redirects=True,timeout = fetch_timeout) as response:
                await response.release()
            response_time = time.monotonic() - t_0
            url.ping_list.append(response_time) 
            print(f'{str(url):40s} | response_time = {response_time*1000:4.0f}ms | avg:{url.get_avg_ping() * 1000:4.0f}ms')
            
        except Exception as e:
            # print("ERROR:", e)
            #print(f'{str(url):40s} | Error Message: {e}')
            BAD_SITES.append(url.address)
            pass
       
                    
    async def main(self,urls, wait, timout_seconds = 3):
        session_timeout = aiohttp.ClientTimeout(total=None,sock_connect= timout_seconds,sock_read=timout_seconds)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout = session_timeout) as session:
            tasks = []
            for url in urls:
                tasks.append(
                    self.get(url, session)
                )
            ret = await asyncio.gather(*tasks)
            await asyncio.sleep(wait)
            
            
            # ret = await asyncio.gather(*[self.get(url, session) for url in urls])
    
    def begin(self, urls, loop = 10, wait = 1):
        for i in range(loop):
            asyncio.run(self.main(urls, wait))
            print(' ----- ')
        now = datetime.now().strftime("%H:%M:%S")
        
        # console report
        report = f"========= REPORT (finished on {now}) =========\n"
        for u in urls:
            if(u.address not in BAD_SITES):
                report += (f"{str(u):40s} average response time: {u.get_avg_ping()*1000:4.0f}ms \n")
        print(report)
        
        # txt report  
        with open("report.txt",'w') as f:        
            for u in urls:
                if(u.get_avg_ping() == 0):
                    f.write(f"{str(u):40s} average response time: X \n")
                else:
                    f.write(f"{str(u):40s} average response time: {u.get_avg_ping()*1000:4.0f}  ms \n")
                
            
    
        

            
PINGER = Pinger()
# PINGER.add_URL_list(ADDR_sample)
# PINGER.print_URL_LIST()

#PINGER.start(tries= 5, delay = 0.1, mode = "not-show")

#PINGER.start(tries= 5, delay = 0.1, mode = "show")

# urls = PINGER.URL_LIST

    # start = time.time()
# asyncio.run(PINGER.main(urls))
# end = time.time()
# print("Took {} seconds to pull {} websites.".format(end - start, len(urls)))




#ADDR_sample = ['https://www.google.com','https://www.amazon.com', 'https://www.bing.com' ]

urls = []

with open('urls.txt', 'r') as f:
    urls_list = f.read().split("\n")
    URLS = [URL(u) for u in urls_list]

PINGER.begin(urls = URLS, loop = 1, wait = 0)


## TEST 

# print(BAD_SITES)