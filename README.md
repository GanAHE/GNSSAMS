<<<<<<< HEAD
# 基于PyQt5开发的前后端GUI桌面、导航定位与测量综合系统软件

[原文详情](https://dgzc.ganahe.top/ganahe/2020/kyppkfdgkskfkj.html)

# 一、背景与说明
## （一）应用场景
当前框架已经实现了多场景的复用测试，有如下：

------------
1.[百度网盘链接有效性检测软件下载 Official 2.0.0 GUI交互版](https://dgzc.ganahe.top/ganahe/2020/bdwpljyxxjcrjogjhb.html "百度网盘链接有效性检测软件下载 Official 2.0.0 GUI交互版")

[![](https://dgzc.ganahe.top/wp-content/uploads/2020/10/2020100209163913.png)](https://dgzc.ganahe.top/wp-content/uploads/2020/10/2020100209163913.png)

2.导航定位与测量综合系统（GNSSAMS Offcial X version）

![file](https://dgzc.ganahe.top/wp-content/uploads/2020/10/post-600-5f910b90de707.png)

![file](https://dgzc.ganahe.top/wp-content/uploads/2020/10/post-600-5f910b95504e6.png)

3.基于YOLO3+本框架的交通场景智能监控系统（ITSMS）

![file](https://dgzc.ganahe.top/wp-content/uploads/2020/10/post-600-5f910b999aad5.png)

------------


## （二）实际检验

------------


1.参加2020第九届中国软件杯获得三等奖，武汉大学：小小搬运工开发组（JoeyforJoy,WHU222huan,GanAHE）,采用本前端框架，能够多场景应用，证明该框架相对成熟，原框架演示地址：https://www.bilibili.com/video/BV1DV411U787/ 

2.参加武汉大学某学院内部竞赛，获得综合系统开发赛三等奖

------------

# 二、开源计划

------------


1. 开放测试版软件供体验；
2.  前端开源供学习；
3.  后端部分开源（合作开发内容需要协商确定）。
4.拟定出本 PyQt5 GUI 框架开发应用教程；
5.采用 C++/Qt 重写，用于正式版

------------




4、开源以及产品上线等，一方面当前安排较多，尚未来得及着手于相关的工作。不过会抽空逐步上线的，感谢大家的支持与关注。[大笑]
5、指定代理发布：https://dgzc.ganahe.top 

开源时间对照表如下：

|      日期      |                             计划                             |             备注             |
| :------------: | :----------------------------------------------------------: | :--------------------------: |
| 2020年10月22日 | 开源中国软件杯参赛三等奖作品——交通场景智能监控系统的前端源代码 |       前端框架基本完备       |
|  2020年12月底  |             GNSSAMS前后端源代码及各提交版本代码              | 前后端不同G it版本代码，齐全 |
|    其他待定    |                              -                               |              -               |

# 三、开源进程
 - [x]第一阶段，开源部分前端代码
 - [ ]2020年12月底，开源GNSSAMS软件前端、后段所有提交历程代码
# 四、商用授权许可申请
## （一）版权所有

------------

### 4.1.1 交通场景智能监控综合系统（ITSMS）
版权所有：武汉大学：小小搬运工开发组（JoeyforJoy,WHU222huan,GanAHE）
![file](https://dgzc.ganahe.top/wp-content/uploads/2020/10/post-600-5f910b9d18a76.png)

### 4.1.2 导航定位与测量综合系统（GNSSAMS）
版权所有：
![file](https://dgzc.ganahe.top/wp-content/uploads/2020/10/post-600-5f910ba028483.png)

### 4.1.3 百度网盘链接有效性检测软件
### 4.1.4 12306 Tickets自动化购票软件

------------

## （二）商用授权申请
如有商用期许，请于`2020年12月底`后通过站长邮箱联系，感谢您的支持与认同。
# 五、开源地址
（一）[Github](https://github.com/GanAH/GNSSANS "Github")
（二）Gitee
# 六、开源协议
## （一）版权著作人协议条款
### 条款一、未经许可不得用于商业用途
### 条款二、不得应用与违法犯罪用途
### 条框三、更改软件并发布后，请保留原版权所有者信息：GanAHE，DGZC
## （二）GPL v3开源协议
=======
---
title: GNSS导航定位与测量综合系统（GNSSAMS Official 1.1.0）使用说明书
type: categories
copyright: true
categories: 我的软件
tags:
  - Python
  - PyQt5
  - 软件
comments: true
top: false
abbrlink: https://dgzc.ganahe.top/
date: 2020-08-03 21:10:49
updated:
---

# GNSS导航定位与测量综合系统 
## 操 作 说 明 书
>### @Copyright by GanAHE,DGZC
>

# 一、软件安装
以Official version1.0版本为例，打开下载的安装包，双击选择安装，弹出如下协议界面，本软件遵循GPL v3 协议，不得将软件用于违法犯罪、商业获利等用途，否则将承担法律责任。
点击同意协议`I accept the agreement`:
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731132105702.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)

<!--more-->

同意协议后，自定义安装路径：
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020073113211720.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
选择是否创建桌面快捷方式：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731132127765.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
解压安装包，等待安装：

安装完成，点击桌面或是菜单栏的GNSSAMS Official 1.0，打开软件，进入欢迎界面：

# 二、标准单点定位
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731141619803.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731114557820.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731114721175.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731120131727.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731120402516.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731120508622.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731120659407.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731120924474.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731121057708.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731121217801.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731121755631.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731122019134.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731122154149.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020073112241110.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731122529579.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731122734911.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020073112281462.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731122956986.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731123138902.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731123302518.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731123448303.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731124115498.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731124256510.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731124357595.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731124549853.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731124638294.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731124659281.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731125044913.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731125209594.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731130310419.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731130510212.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731130609397.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731130707841.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731130833621.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731130930747.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731131029386.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200731131241141.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjY0NjEwMw==,size_16,color_FFFFFF,t_70)

>>>>>>> 0367410d2d6020c98991c05162feaad2ccc434fb
