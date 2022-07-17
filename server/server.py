import hashlib
from flask import Flask  # 导入flask

server_ = Flask(__name__)

# 输出日志
isOutputLog = True


def log(*str_):
    global isOutputLog
    str__ = ''
    for i in str_:
        str__ += i
    if isOutputLog:
        print('日志输出：'+str__)

# 输出主菜单


@server_.route('/menu_text')
def returnMenuText():
    text = """
    学生信息管理系统-在线
    当前服务器IP:%s
    请使用阿拉伯数字选择功能
    1  录入学生信息
    2  查找学生信息
    3  删除学生信息
    4  显示学生信息
    5  修改学生信息
    6  重新登陆
    0  退出学生系统
    10 添加新用户
    20 删除用户
    30 在此客户端执行Python代码
    40 在服务器执行Python代码
    以0结尾的2位数均为管理员操作
    您现在登陆的账户管理员权限为：%s
    """
    log('正在获取主界面菜单文本')
    return text

# MD5操作 此处定义方便后面效验和计算MD5


def md5(str_):
    return hashlib.md5(str_.encode(encoding='UTF-8')).hexdigest()

# 后端服务器页面获取用户信息配置


def getServerConfig(dataName="users.sso-server-config"):
    with open(dataName, "r", encoding="utf-8")as configFile:  # 打开文件
        configFileText_ = configFile.readlines()  # 读取
    configFileText = []
    for i in configFileText_:  # 循环 去掉\n
        # 经测试确认此处使用for i in configFileText和strip和eval无效 建立新的列表
        configFileText.append(eval(i.strip()))

    return configFileText  # 提供返回值

# 检查用户是不是管理员，在客户端登录时优先被调用 方便操作


@server_.route('/is_admin/<userName>/<userPwd>')
def isAdmin(userName, userPwd):
    log('正在验证其账号是否具有管理员权限（有可能是正在登陆）账号信息为：'+userName+'   '+userPwd)
    configFileText = getServerConfig()  # 获取用户信息配置#见getServerConfig()的注释
    for i in configFileText:  # 遍历配置信息
        if authLogin(userName, userPwd):  # 使用authLogin检查用户给出的信息是否有效
            log('用户给出的用户账户信息有效，正在验证其管理员权限有效性')
            if i['admin'] == True:  # 确认有效 开始确认是否为管理员
                log('给出的用户账户信息为管理员权限')
                return 'True'  # 返回值
            log('给出的用户信息有效 但不是管理员')
            return 'False'  # 和下面一样
        else:
            log('用户给出的账户信息无效')
            return 'False'  # 上一个return返回后会自动停止 如果都不对就返回false
    log('用户给出的账户信息不存在')
    return 'False'

# 用户登录验证


@server_.route('/authLogin/<userName>/<userPwd>')
def authLogin(userName, userPwd):  # 检查输入名称、密码的对错
    configFileText = getServerConfig()  # 获取用户信息配置
    for i in configFileText:  # 遍历信息
        if i['userName'] == userName:
            if i['userPwdMD5'] == md5(userPwd):
                return 'True'
    log('用户给出的账户信息无效')
    return 'False'

# 新建用户


@server_.route("/newUser/<userName>/<userPwd>/<isAdmin>")
def newUser(userName, userPwd, isAdmin):
    with open("users.sso-server-config", "a", encoding="utf-8")as configFile:  # 以追加模式打开用户信息文件
        userinfo = {'userName': userName, "userPwdMD5": md5(
            userPwd), 'admin': bool(isAdmin)}  # 生成信息
        log('管理员正在新建名称为%s,密码为%s，管理员权限为%s的账户' %
            (userName, userPwd, str(isAdmin)))
        configFile.write(str(userinfo)+"\n")  # 写入
    return 'True'

# 获取所有学生信息


@server_.route("/getAllData")
def getAllData():
    log('用户正在获取所有学生信息')
    return str(getServerConfig(dataName="datas.sso-server-config"))

# 添加学生


@server_.route('/newStudent/<name>/<chineseScore>/<mathScore>/<englishScore>/<studentID>')
def newStudent(name, chineseScore, mathScore, englishScore, studentID):
    with open("datas.sso-server-config", "a", encoding="utf-8")as dataFile:  # 打开文件，把URL后面的5个值对应到词典中
        studentInfo = {'studentName': name, "chineseScore": chineseScore,
                       "mathScore": mathScore, "englistScore": englishScore, "id": studentID}
        log('用户正在新建数据为%s的学生' % str(studentInfo))
        dataFile.write(str(studentInfo)+"\n")  # 写入
    return 'True'

# 删除学生


@server_.route("/delStudent/<studentID>")
def delStudent(studentID):
    dataFileText = getServerConfig(dataName="datas.sso-server-config")
    for i in range(len(dataFileText)):  # 遍历 查找要删除的学生
        if dataFileText[i]['id'] == studentID:
            del dataFileText[i]  # 查找到了，使用del删除
            log('用户正在删除ID为%s的学生' % studentID)
    with open('datas.sso-server-config', "w", encoding="utf-8")as dataFile:  # 写入文件
        for i in dataFileText:  # for循环写入文件
            dataFile.write(str(i)+'\n')
    return 'True'

# 查找学生


@server_.route("/find/<studentID>")
def findStudent(studentID):
    log('用户正在查找ID为%s的学生' % studentID)
    dataFileText = getServerConfig(dataName='datas.sso-server-config')
    for i in range(len(dataFileText)):
        if dataFileText[i]['id'] == studentID:
            return dataFileText[i]
    return 'False'

# 编辑学生信息


@server_.route('/editStudent/<id>/<name>/<chinese>/<english>/<maths>')
def editStudent(id, name, chinese, english, maths):
    # 把edit变成删除+新建缩减代码量 不重复造轮子 而且语言文本基本都在客户端 更方便
    log('用户正在编辑ID为%s的学生' % id)
    delStudent(id)
    newStudent(name, chinese, maths, english, id)
    return 'True'

# 删除学生信息


@server_.route('/delUser/<userName>')
def delUser(userName):
    log('管理员正在删除名称为%s的用户' % userName)
    configFileText = getServerConfig(
        dataName='users.sso-server-config')  # for循环+判断 remove移除
    for i in configFileText:
        if i['userName'] == userName:
            configFileText.remove(i)
    with open('users.sso-server-config', "w", encoding='utf-8')as configFile:  # 打开 for循环写入
        for i in configFileText:
            configFile.write(str(i)+'\n')
    return 'True'

# Debug-执行代码


@server_.route('/execCode/<code>')
def execCode(code):
    exec(code)
    return 'True'


if __name__ == '__main__':
    isOutputLog = True  # 是否输出程序内自带的日志
    server_.run(debug=True)  # 是否开启Flask的Debug模式，编译、发布时关闭
