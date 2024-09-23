# Bilibili实时粉丝数监视器

#### 注意
现在BFO在使用上有一些问题，原因是B站API更新了一些限制。这些问题已在未来的1.0.1的版本中的源代码被解决，但没有打包成发行版本，您可以自行使用代码，但打包发行将被推迟。

#### 介绍
基于Python的B站粉丝实时监视软件，完全开源。已用Pyinstaller打包，可直接运行exe，无需环境支持。最新发行版本：v1.0.0！

#### 安装教程

完全解压下载好的.zip文件，将所有解压的文件放在同一路径下。即可视为安装完成。

#### 使用说明

1. 先运行BFO.exe，在输入框内输入UID值和监视频率值，然后点击“开始抓取”
2. 再打开OBS，新建一个文本源
3. 右键单击文本源，打开属性编辑页面
4. 勾选“从文件读取”，并将读取文件选定为BFO目录下的output.txt
5. 确定

#### 示例图片
![这是一张使用说明的示例图片](screenshots/example.png)

#### 应用场景
[2019 B站一哥争夺战](https://www.bilibili.com/video/BV114411i7wS "敖犬战蕾蝗")
![敖犬战蕾蝗](screenshots/Ao-VS-Lex.png)
[2018 类似的 YouTube一哥争夺战](https://en.wikipedia.org/wiki/PewDiePie_vs_T-Series "PewDiePie与T-Series之争")
![YT一哥争霸](screenshots/PDP-VS-TSR.png)
