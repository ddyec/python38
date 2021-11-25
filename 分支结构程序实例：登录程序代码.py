
#输入账号和密码
user=input("请输入账号：")
pwd=input("请输入密码：")

#判断输入的账号和密码是否正确
if user=="admin" and pwd== "Python@16":
    print("登录成功！")
else:
    print("账号或密码有误！")

