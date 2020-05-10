
import random
print("开始转换...")
# 稳定点组编号
index = [2,16,39]
print("稳定点组编号：",index)
measure_I = []
with open("I.xyz","r") as openF:
    for line in openF:
        lineData = line.split(",")
        measure_I.append(lineData)
        #print("line ",lineData)
openF.close()

with open("II.xyz","w") as saveF:
    for i in range(len(measure_I)):
        lineData = measure_I[i]
        if i == index[0] or i == index[1] or i == index[2]:
            # 稳定点小随机数
            randomData = random.uniform(-0.0036,0.0036)
        else:
            # 大随机数
            randomData = random.uniform(-0.00546,0.0569)
        lineData = [lineData[0],str(round(float(lineData[1])+randomData,4)),str(round(float(lineData[2])+randomData,4)),str(round(float(lineData[3])+randomData,4))]
        # 逐行写入
        for h in range(4):
            if h ==3:
                saveF.write(lineData[h]+"\n")
            else:
                saveF.write(lineData[h]+",")
saveF.close()

print("完成转换.")
