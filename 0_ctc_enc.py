import os
import sys

if __name__=="__main__":
    folder_name = "E:\\GitCode\\Code\\Cindy1_LR"  # 获取文件夹的名字，即路径
    file_names = os.listdir(folder_name)  # 获取文件夹内所有文件的名字
    qps = [22, 27, 32, 37, 42]
    for file_name in file_names:
        if file_name.endswith('.yuv'):
            name = os.path.splitext(file_name)[0]
            # print(name)
            temp0 = name.split('_', 6)[1]
            temp1 = name.split('_', 6)[2]
            temp2 = name.split('_', 6)[3]
            temp3 = name.split('_', 6)[4]
            weight = int(temp3.split('x')[0])
            height = int(temp3.split('x')[1])
            temp4 = name.split('_', 6)[5]
            temp5 = name.split('_', )[6]
            a=temp5[0:3]
            print(a)
            for i in qps:
                print(F'进行QP为{i}的编码')
                command = (
                           F'E:\\GitCode\\VVCSoftware_VTM\\bin\\vs16\\msvc-19.29\\x86_64\\release\\EncoderApp.exe -c '
                           F'E:\\GitCode\\VVCSoftware_VTM\\cfg\\encoder_intra_vtm.cfg -c '
                           F'E:\\GitCode\\VVCSoftware_VTM\\sequence.cfg -i E:\\GitCode\\Code\\Cindy1_LR\\%s -q {i} -f 1 -wdt %d -hgt %d -fr %d --Level=%.1f --PrintMSSSIM=1 -o '
                           F'E:\\GitCode\\VVCSoftware_VTM\\1_yuv\\{temp0}_{temp1}_{temp2}_{temp3}_{i}_{temp4}_{temp5}.yuv -b '
                           F'E:\\GitCode\\VVCSoftware_VTM\\2_bin\\{temp0}_{temp1}_{temp2}_{temp3}_{i}_{temp4}_{temp5}.bin> '
                           F'E:\\GitCode\\VVCSoftware_VTM\\3_txt\\{temp0}_{temp1}_{temp2}_{temp3}_{i}_{temp4}_{temp5}.txt'%(file_name, weight, height, int(temp4), float(a)))
                p=os.system(command) #最后调用os.system()函数
                if p == 0:
                    pass
                else:
                    print ("Process error")
                    sys.exit()
            #print("当前视频：%s编码完成！"%theVideoPath)
            print(F'本视频{file_name}已完成编码！')
    print('所有视频均已编码！')
os.system('pause')
