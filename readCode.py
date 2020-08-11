#!usr/bin/env python
# -*- coding: utf-8 -*-
import os         
def all_path(dirname,fileFilter = None):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if fileFilter is None:
                result.append(apath)
            else:
                if apath[-len(fileFilter):] == fileFilter:
                    result.append(apath)
    return result
    
fileDir = r"E:\CodePrograme\Python\EMACS"
fileFilterList = all_path(fileDir,"py")

print(fileFilterList)

# 开始逐个打开并写入一个txt文件
resultF = open("Code.txt","w",encoding='UTF-8')
for i in range(len(fileFilterList)):
    with open(fileFilterList[i],"r",encoding='UTF-8') as f:
        print("now write:",fileFilterList[i])
        for line in f:
            resultF.write(line)
    f.close()
print("finish write Files")
resultF.close()

