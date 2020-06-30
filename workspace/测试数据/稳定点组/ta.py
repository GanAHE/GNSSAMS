import random
measure_I = []
with open("I.xyz","r") as f:
    count = 0
    index = 0
    for line in f:
        if index == count:
            measure_I.append(line.split(","))
            count = index+random.randint(1,5)
            print(count)
        index+= 1
        if len(measure_I) == 20:
            break
with open("I_dot.xyz","w") as G:
    for i in range(len(measure_I)):
        lineData = ["GanAH"+str(i+1),measure_I[i][1],measure_I[i][2],measure_I[i][3]]
        for h in range(4):
            if h ==3:
                pass
                G.write(lineData[h])
            else:
                G.write(lineData[h]+",")
        
        