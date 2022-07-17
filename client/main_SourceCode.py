import requests
import sys
import time
def getServerIP():
    configFileText=readConfig()
    if configFileText[0]=="none":
        setServerIP()
        getServerIP()
    else:
        return configFileText[0]
def setServerIP():
    ip=input("请输入服务器IP：")
    ip="http://"+ip+":5000"
    configFileText=readConfig()
    configFileText[0]=ip
    writeConfig(configFileText)
    return True
def writeConfig(configFileText):
    with open("config.sso-client-config","w",encoding="utf-8")as configFile:
        for i in configFileText:
            configFile.write(str(i)+"\n")
def readConfig():
    with open("config.sso-client-config","r",encoding="utf-8")as configFile:
        configFileText=configFile.readlines()
    for i in configFileText:
        i=i.strip()[0]
    return configFileText
def login(ip=getServerIP()):
    username=input("请输入用户名：")
    userpwd=input('请输入用户登陆密码：')
    admin=requests.get(ip+'/is_admin/%s/%s'%(username,userpwd)).text
    authLogin=requests.get(ip+'/authLogin/%s/%s'%(username,userpwd)).text
    if admin=='True':#先检查是不是管理员
        main(isAdmin=True)
    else:
        if authLogin=='True':#如果不是 那么继续检查
            main()
        else:
            print("用户名（或密码）错误！")
def main(ip=getServerIP(),isAdmin=False):
    print(requests.get(ip+""+"/menu_text").text%(ip,isAdmin))
    userInput=int(input('>>>'))
    if userInput==1:
        userinput_ID = input('请输入ID:')
        userinput_NAME = input("请输入名称:")
        userinput_chinese = input("请输入语文分数:")
        userinput_english = input("请输入英语分数:")
        userinput_math = input("请输入数学分数:")
        a=requests.get(ip+'/newStudent/%s/%s/%s/%s/%s'%(userinput_NAME,userinput_chinese,userinput_math,userinput_english,userinput_ID))
        if a.status_code==200:
            print("成功添加！")
        main(isAdmin=isAdmin,ip=ip)
    elif userInput==2:
        userinput_ID=input("请输入要查找的学生ID:")
        a=requests.get(ip+'/find/%s'%userinput_ID)
        if not a.text=="False":
            print("ID:%s   名字：%s   语文分数:%s   数学分数：%s   英语分数：%s"%(eval(a.text)['id'],eval(a.text)['studentName'],eval(a.text)['chineseScore'],eval(a.text)['mathScore'],eval(a.text)['englistScore']))
        main(isAdmin=isAdmin,ip=ip)
    elif userInput==3:
        userinput_ID=input("请输入要删除的学生ID:")
        a=requests.get(ip+'/delStudent/%s'%userinput_ID)
        if a.text=='True':
            print("成功！")
        main(isAdmin=isAdmin,ip=ip)
    elif userInput==4:
        a=requests.get(ip+'/getAllData')
        for i in eval(a.text):
            print("ID:%s   名字：%s   语文分数:%s   数学分数：%s   英语分数：%s"%(i['id'],i['studentName'],i['chineseScore'],i['mathScore'],i['englistScore']))
        main(isAdmin=isAdmin,ip=ip)
    elif userInput==5:
        userinput_ID = input('请输入要修改的学生ID:')
        userinput_NAME = input("请输入名称:")
        userinput_chinese = input("请输入语文分数:")
        userinput_english = input("请输入英语分数:")
        userinput_math = input("请输入数学分数:")
        a=requests.get(ip+'/delStudent/%s'%userinput_ID)
        time.sleep(1)
        a=requests.get(ip+'/newStudent/%s/%s/%s/%s/%s'%(userinput_NAME,userinput_chinese,userinput_math,userinput_english,userinput_ID))
        main(isAdmin=isAdmin,ip=ip)
    elif userInput==6:
        login(ip)
    elif userInput==0:
        print("您已退出学生信息管理系统！")
        sys.exit()
    elif str(userInput)[1]=='0':
        if isAdmin:
            if str(userInput)[0]=='1':
                userName=input("请输入用户名：")
                userPwd=input("请输入用户密码：")
                userIsAdmin=input("请输入是否赋予用户管理员权限？（True/False）")
                a=requests.get(ip+'/newUser/%s/%s/%s'%(userName,userPwd,userIsAdmin))
            if str(userInput)[0]=='2':
                userName=input('请输入要删除的人的用户名：')
                requests.get(ip+'/delUser/%s'%userName)
            if str(userInput)[0]=='3':
                userInput=input(':>>')
                exec(userInput)
            if str(userInput)[0]=='4':
                userInput=input('server-:>>')
                a=requests.get(ip+'/execCode/%s'%userInput)
            main(isAdmin=isAdmin,ip=ip)
        else:
            print('您没有管理员权限，无法执行此操作！您可以重新登陆一个有管理员权限的账号执行此操作')
    else:
        main(isAdmin=isAdmin,ip=ip)
if __name__=='__main__':
    login()
