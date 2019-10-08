import os
import shutil
rootdir_xiao = 'E:\\python_\\accu\\dan'                           #输入文件夹名改这里，文件夹里放一个人标的所有文件
rootdir_xie = 'E:\\python_\\accu\\xie'                            #输入文件夹名改这里，文件夹里放另一个人的文件，文件名得跟上面的一样
list = os.listdir(rootdir_xiao) #列出文件夹下所有的目录与文件
outputdir = 'E:\\python_\\accu\\accu_rate_xie_dan'                #输出文件夹名改这里
shutil.rmtree(outputdir) # 能删除该文件夹和文件夹下所有文件
os.mkdir(outputdir) #重建文件夹，这个+上一个目的是清空文件夹
print(list,len(list))
accu_rate = []
for j in range(len(list)):
    diff_count = 0
    different = []
    file_xiao = rootdir_xiao + '\\' + list[j]
    with open(file_xiao,'r', encoding="utf-8") as xiao:
        xiaolines = xiao.readlines()
    file_xie = rootdir_xie + '\\' + list[j]
    with open(file_xie, 'r', encoding="utf-8") as xie:
        xielines = xie.readlines()
    print(len(xiaolines), len(xielines))
    for i in range(min(len(xiaolines), len(xielines))):
        if(xiaolines[i] != xielines[i]):
            diff_count += 1
            different += str(i+1) + '\n' + '丹 ' + xiaolines[i]  + '谢 ' + xielines[i] + '\n'         #这里的名字顺序得跟文件夹名那里一样
    accu_rate.append(100-diff_count)
    output_file = outputdir + '\\' + list[j]
    with open(output_file, 'w', encoding="utf-8") as output:
        output.write(str(accu_rate[j]) + '%' +'\n')
        output.writelines(different)
        accurate = sum(accu_rate)/len(list)
file_accuracy = outputdir+'\\accuracy.txt'
with open(file_accuracy, 'w', encoding="utf-8") as output:
    output.write(str(accurate) + '%' + '\n' + str(list))