import  re
default_root = 'C:\\Users\\Dcison\\Desktop'
file_object = open(default_root+'\\mmmm.txt',encoding="utf-8") #以utf-8编码打开文件
try:
     all_the_text = file_object.read( )
     regex = "[a-zA-Z]+" #正则匹配单词
     result = re.findall(regex,all_the_text,re.I)
     result = list(set(result)) #把结果加入到result列表中
     result.sort() #列表排序
     print(result) 
     new_file = open(default_root+"\\dict1.txt","w",encoding="utf-8") #以utf-8编码写入文件
     for i in result:
        new_file.writelines(i+"#")
     new_file.close()
finally:
     file_object.close( )