#获取用户桌面地址
import winreg
def getDesktopPath():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key,"Desktop")[0]

#定义路径
trackerUrl=["https://trackerslist.com/all.txt",
"https://ngosang.github.io/trackerslist/trackers_all.txt",
"https://at.raxianch.moe/?type=AT-all"]
trackerPath=getDesktopPath()+'/tracker.txt'
trackeroutPath=getDesktopPath()+'/BT Tracker.txt'

#删除文件
import os
def delFile(path):
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError as e:
            print("Error:  %s : %s" % (path, e.strerror))

#下载tracker内容
import urllib3
import re
def getTracker(url):
    https=urllib3.PoolManager()
    r=https.request('GET',url)
    return bytes.decode(r.data)

#对URL头部进行处理并写入tracker.txt文件
urlTypes=['http://','udp://','wss://','https://']
def TrackerProcess(str):
    with open(trackerPath,'w+',encoding='UTF-8') as f:
        t=str
        t=re.sub('wss://.*','',t)#删除BitComet不支持的wss链接
        for urlType in urlTypes:
            t=t.replace(urlType,' '+urlType)
        tt=t.split(' ')
        tracker=''
        for line in tt:
            if line != 'udp://tracker.leechers-\n':#处理这个错误源
                tracker+=line+'\n'
        f.write(tracker)

#处理重复行和空行
def delRepet():
    with open(trackerPath,'r',encoding='utf-8') as file:
        with open(trackeroutPath,'w+',encoding='UTF-8') as out:
            lines_list=set()
            for line in file:
                if line not in lines_list and line !="\n":
                    out.write(line)
                    lines_list.add(line)

#主函数
import os
def main():
    print("使用开源订阅源 可以免费使用!\n正在检测文件状态......\n")
    # isExists(trackeroutPath)
    print("开始下载数据......\n")
    #tracker下载到变量
    trackerlist=str()
    for url in trackerUrl:
        trackerlist+=(getTracker(url))
    print("正在保存文件......\n")
    TrackerProcess(trackerlist)
    delRepet()
    delFile(trackerPath)
    print("下载完成，请去桌面查看!\n")
    os.system("pause")

if __name__ == "__main__":
    main()