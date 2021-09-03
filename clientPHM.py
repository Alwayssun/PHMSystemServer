import os,sys,time,random
try:
    import requests
except IOError:
    print("Failed to import the lib requests!Trying to install it ... ")
    os.system("pip install requests")
    print("Installing the package requests...")

url="http://127.0.0.1:8000/phm/upData/"
data = {"data":12}
headers = {
    'Content-Type':'application/json; charset=UTF-8',
    'Host':'jinbao.pinduoduo.com',
    'Origin':'http://jinbao.pinduoduo.com',
    'Referer':'http://jinbao.pinduoduo.com/',
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}


def postData(reqTime=1):

    count = 0
    xx = 0
    while count < 10:
        try:
            xx = random.randrange(1,100000)
            data['data']= xx
            req = requests.post(url, data,headers = headers)
        except KeyboardInterrupt:
            sys.exit()
        except:
            print("Connecting to the server ...")
            time.sleep(reqTime)
            count = count + 1
            continue

        if req.status_code == 200:
            print("Succeed to transport data!--",xx)
            time.sleep(reqTime)
            break
        else:
            print("No found url",req)
            time.sleep(reqTime)
    else:
        print("Failed to connect to the server!Quiting ...")
        sys.exit()
if __name__ =="__main__":
    while True:
        postData()