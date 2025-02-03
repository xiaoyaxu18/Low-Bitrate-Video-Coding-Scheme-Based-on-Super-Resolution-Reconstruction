import os
import subprocess

def downsample_single_frame(input_folder, output_folder, ffmpeg_path):
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有YUV文件
    input_files = [f for f in os.listdir(input_folder) if f.endswith('.yuv')]

    for input_file in input_files:
        input_path = os.path.join(input_folder, input_file)
        output_path = os.path.join(output_folder, f'downsampled_{input_file}')
        name = os.path.splitext(input_file)[0]
        temp3 = name.split('_', 5)[3]
        weight = int(temp3.split('x')[0])
        height = int(temp3.split('x')[1])

        # 使用FFmpeg进行双线性插值2倍下采样，并确保宽和高是8的倍数
        # 解析文件名以获取宽、高和帧率
        temp_parts = name.split('_')
        width, height = map(int, temp_parts[3].split('x'))
        framerate = temp_parts[4]

        print(f'Original Size: {width}x{height}, Framerate: {framerate}')

        # 使用FFmpeg进行双线性插值2倍下采样，并确保宽和高是8的倍数
        cmd = [
            ffmpeg_path,
            '-s', f'{width}x{height}',  # 指定视频分辨率
            '-r', framerate,  # 指定帧率
            '-pix_fmt', 'yuv420p10le',
            '-i', input_path,  # 输入文件路径
            '-vf', 'scale=iw/2:ih/2',
            '-frames:v', '1',  # 只处理一帧
            '-sws_flags', 'bilinear',
            '-pix_fmt', 'yuv420p10le',
            '-c:v', 'rawvideo',
            '-y',  # 覆盖输出文件
            '-pix_fmt', 'yuv420p10le',  # 明确设置像素格式
            output_path  # 输出文件路径
        ]


        subprocess.run(cmd)

if __name__ == "__main__":
    input_folder = "C:\\Users\\p\\Desktop\\Cindy2\\"
    output_folder = "C:\\Users\\p\\Desktop\\Cindy1\\"
    ffmpeg_path = "G:\\软件\\ffmpeg-2023-02\\bin\\ffmpeg.exe"

    downsample_single_frame(input_folder, output_folder, ffmpeg_path)


