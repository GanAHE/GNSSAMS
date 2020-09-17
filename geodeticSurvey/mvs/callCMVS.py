#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
comment: 调用CMVS三维重构扩展exe

@author: GanAH  2020/9/11.
@version 1.0.
@contact: dinggan@whu.edu.cn
"""
import subprocess
import os
def toVmcs():
    rootDir = "../../source/exModule/VMCS/"
    rootDir = os.path.abspath(rootDir)
    print(rootDir)

    # 设置命令
    commend1 = rootDir + "\\cmvs.exe" + " " + rootDir + "\\pmvs\\"
    commend2 = rootDir + "\\genOption.exe" + " " + rootDir + "\\pmvs\\"
    commend3 = rootDir + "\\pmvs2.exe" + " " + rootDir + "\\pmvs\\ option-0000"
    # 执行CMVS
    process = subprocess.Popen(commend1, shell=True, encoding="utf-8")
    process.wait()
    process = subprocess.Popen(commend2, shell=True)
    process.wait()
    process = subprocess.Popen(commend3, shell=True)
    process.wait()

def eSFM():
    rootDir = "../../source/exModule/VMCS/"
    rootDir = os.path.abspath(rootDir)
    main = rootDir+"/VisualSFM.exe"
    r_v = os.system(main)
    print (r_v )

# eSFM()
toVmcs()

