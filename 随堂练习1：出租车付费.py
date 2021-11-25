#出租车计费程序

#输入路程
s=float(input("请输入行驶路程："))
if int(s)!=s:
    s=round(s+0.5)

#计算金额
if s<=3:
    m=10 
else:  
                     #程序填空
print(s,"千米，","付费",m,"元。")
