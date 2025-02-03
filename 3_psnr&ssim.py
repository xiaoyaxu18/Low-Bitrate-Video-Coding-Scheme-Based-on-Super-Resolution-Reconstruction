import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

def yuv420p10le_to_rgb(yuv_data, width, height):
    # YUV420P10LE 数据包含 Y、U、V 三个分量，每个分量都是 16 位
    y_size = width * height
    uv_size = y_size // 4

    # 分离 Y、U、V 分量
    y_channel = yuv_data[:y_size]
    u_channel = yuv_data[y_size:y_size + uv_size]
    v_channel = yuv_data[y_size + uv_size:]

    # 调整形状
    y_channel = np.reshape(y_channel, (height, width))
    u_channel = np.reshape(u_channel, (height // 2, width // 2))
    v_channel = np.reshape(v_channel, (height // 2, width // 2))

    # 放大 U、V 通道，使其与 Y 通道具有相同的形状
    u_channel = cv2.resize(u_channel, (width, height), interpolation=cv2.INTER_LINEAR)
    v_channel = cv2.resize(v_channel, (width, height), interpolation=cv2.INTER_LINEAR)

    # 将 YUV 转换为 RGB
    yuv_img = np.stack((y_channel, u_channel, v_channel), axis=-1)
    rgb_img = cv2.cvtColor(yuv_img.astype(np.uint16), cv2.COLOR_YUV2RGB)


    return rgb_img


def calculate_psnr_ssim(folder1, folder2):
    # 获取两个文件夹中的所有 YUV 文件
    files1 = sorted([f for f in os.listdir(folder1) if f.endswith('.yuv')])
    files2 = sorted([f for f in os.listdir(folder2) if f.endswith('.yuv')])

    psnr_values = []
    ssim_values = []

    for file1, file2 in zip(files1, files2):
        name = os.path.splitext(file1)[0]
        temp3 = name.split('_', 5)[3]
        width = int(temp3.split('x')[0])
        height = int(temp3.split('x')[1])
        #print(width)
        #print(height)
        # 读取 YUV 数据
        yuv_data1 = np.fromfile(os.path.join(folder1, file1), dtype=np.uint16)
        yuv_data2 = np.fromfile(os.path.join(folder2, file2), dtype=np.uint16)

        # 将 YUV 转换为 RGB
        rgb_img1 = yuv420p10le_to_rgb(yuv_data1, width, height)
        rgb_img2 = yuv420p10le_to_rgb(yuv_data2, width, height)

        # 计算 PSNR
        psnr_value = psnr(rgb_img1, rgb_img2)
        psnr_values.append(psnr_value)

        # 计算 SSIM
        ssim_value, _ = ssim(rgb_img1, rgb_img2, full=True, multichannel=True)
        ssim_values.append(ssim_value)

    return psnr_values, ssim_values

if __name__ == "__main__":
    folder1 = "C:\\Users\\p\\Desktop\\Code\\Cindy2_高分辨率视频\\"
    folder2 = "C:\\Users\\p\\Desktop\\Code\\Cindy2_高分辨率视频\\"


    psnr_value, ssim_value = calculate_psnr_ssim(folder1, folder2)

    for psnr_val in psnr_value:
        print(f"PSNR: {psnr_val:.2f}")
    for ssim_val in ssim_value:
        print(f"SSIM: {ssim_val:.2f}")