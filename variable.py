#coding=utf-8
from mirai import Mirai
import datetime
import time
from mirai import Mirai, Plain, MessageChain, Friend, Image, Group, protocol, Member, At, Face, JsonMessage
import json

memberSetuNet={}         #每个群每个成员要的网络setu计数（限制每人五张）
memberSetuFobidden={}       #每个群被禁止要setu的成员id
memberPicCount={}           #每个群成员要setu/real的次数
group_repeat={}             #每个群判断是否复读的dict
group_repeat_switch={}      #每个群的复读开关
timeDisable={}              #关闭setu开关的时间
searchReady={}              #接下来要进行搜图的id
pmlimit={}                  #setu/real限制每分钟张数人员记录
limitQuantity={}            #各群限制setu/real每分钟张数
blacklist=[]

localtime = time.localtime(time.time())
day_set=localtime.tm_mday

setuCount=0         #网络setu编号
count=0             #setu保存编号
bizhiCount=0        #网络壁纸编号
setuCalled=0        #响应setu请求次数
bizhiCalled=0       #响应壁纸请求次数
weatherCalled=0     #响应天气请求次数
realCalled=0        #响应real请求次数
responseCalled=0    #响应请求次数
dragonId=[]         #龙王id（可能有多个）
dragon={}           #各群今日是否已宣布龙王
groupR18={}         #各群组r18开关
management={}       #拥有管理权限的用户id
searchCount=0       #搜图编号
city=[]             #全国城市（地区）列表

n_time = datetime.datetime.now()    #目前时间
start_time = 0    #程序启动时间
d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:00', '%Y-%m-%d%H:%M')   #龙王宣布时间

setuSrc=""                   #setu api地址
bizhiSrc=""                                           #壁纸api地址
zuanHighSrc=""                           #祖安（High）api地址
zuanLowSrc=""                  #祖安（Low）api地址
rainbowSrc=""                             #彩虹屁api地址
searchSrc="https://saucenao.com/"                                                       #搜图网址
translateSrc=""          #翻译地址
weatherSrc="" #天气api地址
chatSrc=""

weatherCalledDist="S:\MiRai_QQRobot\info\weather.txt"           #天气调用数据存储路径
setuCalledDist="S:\MiRai_QQRobot\info\setu.txt"                 #setu调用数据存储路径
bizhiCalledDist="S:\MiRai_QQRobot\info\\bizhi.txt"              #壁纸调用数据存储路径
realCalledDist="S:\MiRai_QQRobot\info\\real.txt"                #real调用数据存储路径
responseCalledDist="S:\MiRai_QQRobot\info\\responseCount.txt"   #响应数据存储路径

setuDist="M:\\Pixiv\\pxer_new\\"                                  #setu存储路径
setu18Dist="M:\\Pixiv\\pxer18_new\\"                              #setuR18存储路径
bizhiDist="M:\\Pixiv\\bizhi\\"                                   #壁纸存储路径
realDist="M:\\Pixiv\\reality\\"                                  #真人setu存储路径
timeDist="M:\\pixiv\\time\\"                                     #时间图片文件夹存储路径
responseDist="S:\MiRai_QQRobot\info\\response.txt"              #日志存储路径
responseOldDist="S:\MiRai_QQRobot\info\\oldResponse.txt"        #旧日志存储路径
adminDist="S:\MiRai_QQRobot\info\\admin.txt"                    #管理员数据存储路径

angryDist="S:\\MiRai_QQRobot\\img\\angry.jpg"                   #生气图片绝对路径
dragonDist="S:\MiRai_QQRobot\info\dragon.txt"                  #龙王数据记录
searchCountDist="S:\MiRai_QQRobot\info\searchCount.txt"        #搜索编号存储路径
setuBotDist="M:\pixiv\\botImage\\"                              #涩图机器人监听保存图片路径
searchDist="M:\pixiv\\search\\"                                 #涩图机器人搜图保存图片路径
clockPreviewDist="M:\pixiv\\time\preview\\"                     #表盘预览图存储路径
clockSaveDist="S:\MiRai_QQRobot\info\\clockChoice.txt"        #表盘选择数据存储路径
predictDist="M:\pixiv\\predict\\"

reply_word=["啧啧啧","确实","giao","？？？","???","芜湖","是谁打断了复读？","是谁打断了复读?","老复读机了","就这","就这？","就这?"]     #复读关键词
non_reply=["setu","bizhi","","别老摸了，给爷冲！","real","几点了","几点啦","几点啦?","几点了?","冲？","今天我冲不冲？"]      #不复读关键词
setuCallText=["[Image::A3C91AFE-8834-1A67-DA08-899742AEA4E5]","[Image::A0FE77EE-1F89-BE0E-8E2D-62BCD1CAB312]","[Image::04923170-2ACB-5E94-ECCD-953F46E6CAB9]","[Image::3FFFE3B5-2E5F-7307-31A4-2C7FFD2F395F]","[Image::8A3450C7-0A98-4E81-FA24-4A0342198221]","setu","车车","开车","来点色图","来点儿车车"]
searchCallText=["search","搜图"]
timeCallText=["几点啦","几点了","几点啦？","几点了？","time"]
setuBot=[]
setuGroup=[]
repeatBot=[]

with open("W:\linux-command-master\dist\data.json","r",encoding='utf-8') as f:
    linuxJsonStr=f.read()
linuxDict=json.loads(linuxJsonStr)

command="""command:
    打开setu开关:
        setting.setuEnable
    关闭setu开关:
        setting.setuDisable
    打开r18开关:
        setting.r18Enable
    关闭r18开关:
        setting.r18Disable
    允许某成员要setu:
        setting.memberSetuEnable@member
    禁止某成员要setu:
        setting.memberSetuDisable@member
    设置模式为'normal/zuanHigh/zuanLow/rainbow':
        setting.setMode.'normal/zuanHigh/zuanLow/rainbow'
    设置setu功能关闭时间:
        setting.timeDisable HH:MM to HH:MM
    设置setu功能全天开放:
        setting.timeAllDay
    获取目前全部信息:
        check.all
    获取某成员setu索取计数:
        check.memberSetuCount@member
    获取本群内群成员setu索取计数:
        check.memberSetuCountAll
    获取所有管理人员:
        check.allAdmin"""

hostCommand="""Host Command:
    本地setu:
        setting.setSetuLocal
    网络setu:
        setting.setSetuNet
    本地bizhi:
        setting.setBizhiLocal
    网络bizhi:
        setting.setBizhiNet
    关闭机器人:
        setting.offline
    打开机器人(offline状态下):
        setting.online
    添加管理员:
        setting.addAdmin@member
    删除管理员:
        setting.deleteAdmin@member
    查看系统信息:
        info.sys"""

info="""info:
            setu调用次数：info.setuCount
            bihzi调用次数:info.bizhiCount
            天气调用次数:info.weatherCount"""

menu="""menu:
    1.营销号生成器(暂时关闭)
    2.问我问题
    3.碧蓝航线wiki舰娘/装备查询
    4.天气查询
    5.setu
    6.bizhi
    7.p站搜图
    使用 @机器人 编号 查询使用方法"""

mode="""mode:
    1.normal - 普通模式
    2.zuanHigh - 祖安模式(高能)
    3.zuanLow - 祖安模式(低能)
    4.rainbow - 彩虹屁模式
    使用 @机器人 编号 调用
"""

# Wiki内容
secondFLevelDirectory=["img","weather","yxh","blhx","ask","translate","speakMode","mute"]
wikiSetu=[Plain(text="\nsetu使用方式：\n直接在群中发送setu即可")]

wikiReal=[Plain(text="\nreal使用方式：\n直接在群中发送real即可")]

wikiBizhi=[Plain(text="\nbizhi使用方式：\n直接在群中发送bizhi即可")]

wikiSearch=[Plain(text="\n搜图使用方式：\n在群中发送搜图或search，等待机器人响应，待获得机器人“请发送要搜索的图片呐~”的回复过后直接发送要搜索的图片即可。\n注意：本搜图功能仅可搜索到大部分p站的画师作品，发送表情包，其他无关图片等可能会导致机器人卡死。")]

wikiPredict=[Plain(text="\n预测图片使用方式：\n在群中发送这张图里是什么，等待机器人响应，待获得机器人“请发送要预测的图片呐(推荐真实图片呐)~”的回复过后直接发送要搜索的图片即可。\n注意：本预测功能仅可对真实照片进行识别，发送表情包、动漫图片或其他阴间图片等识别正确率极低。")]

wikiWeather=[
    Plain(text="\n天气功能使用方式：\n在群中发送@bot 天气+中国城市/部分地区\n"),
    Plain(text="如：@bot 天气北京")
]

wikiYxh=[
    Plain(text="\n营销号生成器功能使用方式：\n在群中发送@bot 营销号、主体、事件、事件的另一种说法\n"),
    Plain(text="如：@bot 营销号、开水、不能直接喝、非常烫嘴不能直接喝")
]

wikiBlhx=[
    Plain(text="\nblhxWiki功能使用方式：\n在群中发送@bot blhx：舰娘/装备名称（注意要全名）\n"),
    Plain(text="如：@bot blhx：欧根亲王")
]

wikiAsk=[
    Plain(text="\n提问功能使用方式：\n在群中发送@bot 问你点儿事儿：问题\n"),
    Plain(text="如：@bot 问你点儿事儿：全球有多少个国家")
]

wikiTranslate=[
    Plain(text="\n翻译功能使用方式：\n在群中发送@bot text用目标语言怎么说\n"),
    Plain(text="如：@bot 你好用英文怎么说\n"),
    Plain(text="注：目前源语言只支持中英日韩四种，目标语言支持中文、英文、日文、韩文、法文、西班牙文、意大利文、德文、土耳其文、俄文、葡萄牙文、越南文、印度尼西亚文、马来西亚文、泰文")
]

wikiSpeakMode=[
    Plain(text="\n此功能由管理员管理\n"),
    Plain(text="normal模式下对除命令和功能以外的@bot不作响应\n"),
    Plain(text="zuanLow模式下对@bot作低浓度祖安语回复\n"),
    Plain(text="zuanHigh模式下对@bot作高浓度祖安语回复(慎用)\n"),
    Plain(text="rainbow模式下对@bot作彩虹屁回复\n"),
    Plain(text="chat模式下对@bot作智能AI回复(很傻)\n"),
    Plain(text="管理员管理详情请发送@bot wiki:speakModeSetting")
]

wikiMute=[
    Plain(text="\nmute功能使用方式：\n"),
    Plain(text="1.@bot 晚安/精致睡眠(获得8小时禁言)\n"),
    Plain(text="2.@bot 万籁俱寂(全员禁言)\n"),
    Plain(text="3.@bot 春回大地(全员解除禁言)\n"),
    Plain(text="注：本功能需机器人为群管理员才可实现")
]

wikiLinux=[
    Plain(text="\nlinux命令查询功能使用方式：\n在群中发送@bot linux:命令名称（完整命令）\n"),
    Plain(text="如：@bot linux:sudo\n"),
    Plain(text="注：本功能并未收录全部命令，会有许多命令查询不到")
]

setuSetting=[
    Plain(text="\nsetu功能设置：\n"),
    Plain(text="@bot setting.setu.Enable/Disable\n"),
    Plain(text="Enable:开  Disable:关")
]

r18Setting=[
    Plain(text="\nr18功能设置：\n"),
    Plain(text="@bot setting.r18.Enable/Disable\n"),
    Plain(text="Enable:开  Disable:关"),
    Plain(text="注：谨慎使用，程序自动设置10秒后撤回r18图片，以防万一，请开启时务必有管理员在场，以免撤回功能失效带来的不必要的损失")
]

realSetting=[
    Plain(text="\nreal功能设置：\n"),
    Plain(text="@bot setting.real.Enable/Disable\n"),
    Plain(text="Enable:开  Disable:关")
]

bizhiSetting=[
    Plain(text="\nbizhi功能设置：\n"),
    Plain(text="@bot setting.bizhi.Enable/Disable\n"),
    Plain(text="Enable:开  Disable:关")
]

searchSetting=[
    Plain(text="\nsearch功能设置：\n"),
    Plain(text="@bot setting.search.Enable/Disable\n"),
    Plain(text="Enable:开  Disable:关")
]

countLimitSetting=[
    Plain(text="\ncountLimit功能设置：\n"),
    Plain(text="@bot setting.countLimit.Enable/Disable\n"),
    Plain(text="Enable:开  Disable:关\n"),
    Plain(text="注：需要最高权限")
]

limitSetting=[
    Plain(text="\nlimit功能设置：\n"),
    Plain(text="@bot setting.limit.number\n"),
    Plain(text="number:每分钟限制要图次数(仅包括setu和real)\n"),
    Plain(text="注：需要最高权限")
]

blacklistSetting=[
    Plain(text="\nblacklist功能设置：\n"),
    Plain(text="@bot setting.blacklist.add @member\n"),
    Plain(text="注：需要最高权限")
]

repeatSetting=[
    Plain(text="\nrepeat功能设置：\n"),
    Plain(text="@bot setting.repeat.Enable/Disable\n"),
    Plain(text="Enable:开  Disable:关\n")
]

speakModeSetting=[
    Plain(text="\nspeakMode功能设置：\n"),
    Plain(text="@bot setting.speakMode.mode\n"),
    Plain(text="mode分为五种：\n"),
    Plain(text="1.normal 对@bot不作响应\n"),
    Plain(text="2.zuanLow 对@bot作低浓度祖安响应\n"),
    Plain(text="3.zuanHigh 对@bot作高浓度祖安响应(极度慎用)\n"),
    Plain(text="4.rainbow 对@bot作彩虹屁响应\n"),
    Plain(text="5.chat 对@bot作智能AI回答响应(很傻，试试得了)\n"),
    Plain(text="如：@bot setting.speakMode.normal")
]

requirements=[
    Plain(text="\nrequirements:\n"),
    Plain(text="PyMySQL==0.9.3\n"),
    Plain(text="kuriyama==0.3.6\n"),
    Plain(text="Keras==2.3.1\n"),
    Plain(text="numpy==1.18.5\n"),
    Plain(text="matplotlib==3.2.2\n"),
    Plain(text="requests==2.24.0\n"),
    Plain(text="nvidia_ml_py3==7.352.0\n"),
    Plain(text="WMI==1.5.1\n"),
    Plain(text="mirai==0.1.5\n"),
    Plain(text="Pillow==7.2.0\n"),
    Plain(text="pynvml==8.0.4\n"),
    Plain(text="record==3.5\n"),
]

repeatInfo=[
    Plain(text="\nrepeatInfo：\n"),
    Plain(text="@bot info.repeat\n")
]

setuLocalInfo=[
    Plain(text="\nsetuLocalInfo：\n"),
    Plain(text="@bot info.setuLocal\n")
]

bizhiLocalInfo=[
    Plain(text="\nbizhiLocalInfo：\n"),
    Plain(text="@bot info.bizhiLocal\n")
]

countLimitInfo=[
    Plain(text="\ncountLimitInfo：\n"),
    Plain(text="@bot info.countLimit\n")
]

setuInfo=[
    Plain(text="\nsetuInfo：\n"),
    Plain(text="@bot info.setu\n")
]

realInfo=[
    Plain(text="\nrealInfo：\n"),
    Plain(text="@bot info.real\n")
]

bizhiInfo=[
    Plain(text="\nbizhiInfo：\n"),
    Plain(text="@bot info.bizhi\n")
]

r18Info=[
    Plain(text="\nr18Info：\n"),
    Plain(text="@bot info.r18\n")
]

speakModeInfo=[
    Plain(text="\nspeakModeInfo：\n"),
    Plain(text="@bot info.speakMode\n")
]

switchInfo=[
    Plain(text="\nswitchInfo：\n"),
    Plain(text="@bot info.switch\n")
]

sysInfo=[
    Plain(text="\nsysInfo：\n"),
    Plain(text="@bot info.sys\n")
]

groupInfo=[
    Plain(text="\ngroupInfo：\n"),
    Plain(text="@bot info.group\n")
]

allInfo=[
    Plain(text="\nallInfo：\n"),
    Plain(text="@bot info.all\n")
]
