# -*- coding:utf-8 -*-
from tkinter import *
from base64 import *
import base64
import tkinter.messagebox,tkinter.filedialog
import os
import random
import huffman
import re
import datetime
default_root = "C:\\Users\\Dcison\\Desktop"
Max = 100
class MainWindow:
    def baseEncode(self,str):
        #base混合加密
        str = str.encode()
        result = {
            '16': lambda x: b16encode(x),
            '32': lambda x: b32encode(x),
            '64': lambda x: b64encode(x),
        }
        for i in range(5):
            a = random.choice(['16', '32', '64'])
            str = result[a](str)
        self.decode['text'] = "位置有限，只显示部分内容\n"+str.decode()
        with open(default_root+'\\code.txt', "wb") as f:
            f.write(str)
        f.close()

    def baseDecode(self,tar):
        print (tar)
        p = tar #将目标赋值给p
        n = ""
        Times = 5
        while Times>0:
            # Base16
            Times -= 1 #次数减一
            try: #尝试base16解码
                n = base64.b16decode(p)
                p = n
                continue
            except:
                pass
            # Base32
            try: #尝试base32解码
                n = base64.b32decode(p)
                p = n
                continue
            except:
                pass
            # Base64
            try: #尝试base64解码
                n = base64.b64decode(p)
                p = n
                continue
            except:
                pass
            break
        try:
            self.tarDict = n.decode().split()
        except:
            tkinter.messagebox.showwarning(title="解密失败", message="请确保所用加密方式正确")

    def buttonListener1(self, event):
        root = tkinter.filedialog.askopenfilename(title="选择字典",initialdir=(os.path.expanduser(default_root)),filetypes=[("Text file", "*.txt*")])
        #将字典存储
        if len(root):
            new_file = open(root, "r")
            self.dict = new_file.read().split("#")
            #生成随机权重
            if len(self.dict)>1:
                print("打开字典" + root + "成功")
                print(self.dict)
                self.hasDict = True
                self.label = Label(self.frame, text=root,bg="#fafaff",fg="#9966CC")
                self.label.grid(row=0, column=1, padx=5, pady=5, sticky=(W, E))
                _dict = []
                for i in range(0,len(self.dict)-1):
                    _dict.append((self.dict[i],random.randint(0,Max)))
                #画哈夫曼树
                tree = huffman.codebook(_dict)
                if (len(self.keyDict)):
                    self.keyDict.clear()
                for i in tree:
                    t = tree.get(i)
                    self.keyDict.append((i, t))
                print(self.keyDict)
                new_file.close()
            else:
                tkinter.messagebox.showwarning(title="打开字典失败", message="字典内容不正确，请确保字典内容格式正确且数目大于一个单词")

    def buttonListener2(self, event):
        root = tkinter.filedialog.askopenfilename(title="选择文件",initialdir=(os.path.expanduser(default_root)),filetypes=([("Text file", "*.txt*")]))
        if len(root):
            print("打开"+root+"成功")
            self.hasTxt = True
            self.label = Label(self.frame, text=root,bg="#fafaff",fg="#9966CC")
            self.label.grid(row=1, column=1, padx=5, pady=5,sticky=(W,E))
            #分词
            file_object = open(root,"r",encoding="utf-8")
            all_the_text = file_object.read()
            self.code['text'] = "位置有限，只显示部分内容\n" + all_the_text
            string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+","#", all_the_text)#将标点符号替换为空格
            result = string.split('#')
            arr = [elem for elem in result if elem != '']
            self.tarDict = arr
            file_object.close()

    def buttonListener3(self, event):
        type = self.choose
        if self.hasDict and self.hasTxt:
            if len(self.keyDict) is 0 or len(self.tarDict) is 0:
                tkinter.messagebox.showwarning(title="失败", message="加密字典或者目标文件内容为空或字典格式不正确")
            else:
                time1 = datetime.datetime.now()
                print("加密字典", self.keyDict)
                print("目标", self.tarDict)
                arr = []
                flag = False
                if type == 1:   #加密
                    for i in self.tarDict:
                        flag = False
                        for j in self.keyDict:
                            if i == j[0]:
                                flag = True
                                arr.append(j[1])
                                break
                        if not flag:
                            arr.append('ERR')
                    flag = False
                    for i in arr:
                        if i == 'ERR':
                            flag = True
                            break
                    str = ""
                    for i in arr:
                        str += i + " "
                    self.baseEncode(str)
                    time2 = datetime.datetime.now()
                    print(time2-time1)
                    if flag:
                        tkinter.messagebox.showwarning(title="加密完成", message="文件存储在桌面,但是加密内容不全成功")
                    else:
                        tkinter.messagebox.showinfo(title="加密成功", message="文件存储在桌面")
                elif type == 2: #解密
                    time1 = datetime.datetime.now()
                    print(self.tarDict)
                    self.baseDecode(self.tarDict[0])
                    for i in self.tarDict:
                        flag = False
                        for j in self.keyDict:
                            if i == j[1]:
                                flag = True
                                arr.append(j[0])
                                break
                        if not flag:
                            arr.append('ERR')
                    new_file = open(default_root+"\\decode.txt", "w", encoding="utf-8")
                    text = ""
                    for i in arr:
                        new_file.writelines(i + " ")
                        text+= i+" "
                    self.decode['text'] = "位置有限，只显示部分内容\n" + text
                    new_file.close()
                    time2 = datetime.datetime.now()
                    print(time2 - time1)
                    flag = False
                    for i in arr:
                        if i == 'ERR':
                            flag = True
                            break
                    if flag:
                        tkinter.messagebox.showwarning(title="解密完成", message="文件存储在桌面,但是解密内容不全成功")
                    else:
                        tkinter.messagebox.showinfo(title="解密成功", message="文件存储在桌面")
                elif type != 1 and type !=2:
                    tkinter.messagebox.showwarning(title="提醒", message="请先选择操作")
        else:
            tkinter.messagebox.showwarning(title="发生错误", message="请先导入字典与选定要加密的文件")

    def centerWindow(self, width, height):
        screenwidth = self.frame.winfo_screenwidth()
        screenheight = self.frame.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.frame.geometry(size)

    def radio(self): #单选框变量赋值
        self.choose = self.var.get()

    def __init__(self):
        self.hasDict = False
        self.hasTxt = False
        self.choose = 0
        self.keyDict = [] #密码字典
        self.tarDict = [] #加密/解密目标
        self.dict = list()   #打开的字典文件
        self.codeContent='加/解密目标'
        self.decodeContent="加/解密结果"
        self.frame = Tk()
        self.frame.title("Huffman Encode/Decode")
        self.frame['bg'] = '#f8f8ff' #设置背景颜色
        self.centerWindow(600,450) # 居中显示
        self.var = tkinter.IntVar()
        #初始化控件
        self.button1 = Button(self.frame, text="导入字典", width=10,bg="#00aeee",fg="white",bd=0,relief="solid")
        self.button2 = Button(self.frame, text="导入文件", width=10,bg="#00aeee",fg="white",bd=0,relief="solid")
        self.button3 = Button(self.frame,text="Go→",width=10,bg="#00aeee",fg="white",bd=0,relief="solid")
        self.author = Label(self.frame,text="Author@Dcison",bg="#f8f8ff",fg="#00BFFF")
        self.code = Label(self.frame,text=self.codeContent,bg="white",fg="black",width=34,height=15,justify="left",anchor='nw',wraplength=230)
        self.decode = Label(self.frame, text=self.decodeContent, bg="white", fg="black", width=34,height=15,justify="left", anchor='nw', wraplength=230)
        self.radio1 = Radiobutton(self.frame,text="加密文件",variable=self.var,value=1,command=self.radio,bg='#f8f8ff')
        self.radio2 = Radiobutton(self.frame,text="解密文件",variable=self.var,value=2,command=self.radio,bg='#f8f8ff')
        #设置控件布局
        self.button1.grid(row=0, column=0, padx=5, pady=5)
        self.button2.grid(row=1, column=0, padx=5, pady=5)
        self.code.place(anchor='n',x=135,y=100)
        self.decode.place(anchor='n', x=465, y=100)
        self.author.place(anchor='n',x=300,y=430)
        self.radio1.place(anchor="n",x=65,y=75)
        self.radio2.place(anchor="n", x=150, y=75)
        self.button3.place(anchor="n", x=300, y=220)
        #控件绑定方法
        self.button1.bind("<ButtonRelease-1>", self.buttonListener1)
        self.button2.bind("<ButtonRelease-1>", self.buttonListener2)
        self.button3.bind("<ButtonRelease-1>", self.buttonListener3)


        self.frame.mainloop() #循环渲染


window = MainWindow()