# Video Watermark Removal Tool

这是一个基于 OpenCV 的视频水印去除工具。用户可以通过选择视频中的水印区域，程序会自动修复并去除水印，生成一个没有水印的视频文件。

## 功能特性
- **交互式水印选择**：用户可以通过鼠标在视频的第一帧中选择水印区域。
- **图像修复技术**：使用 OpenCV 的 Inpainting 技术修复水印区域。
- **图像平滑处理**：通过双边滤波改善修复区域的视觉效果。
- **逐帧处理**：支持对视频的每一帧进行水印去除。
- **撤销功能**：用户可以在选择水印区域时撤销上一步操作。

## 技术原理
1. **水印区域选择**：
   - 用户在视频的第一帧中通过鼠标选择水印所在的矩形区域。
   - 选择的区域坐标被记录下来，用于后续帧的处理。

2. **图像修复（Inpainting）**：
   - 使用 OpenCV 的 `cv2.inpaint` 函数对水印区域进行修复。
   - 修复算法基于快速行进方法（Fast Marching Method），适合修复小区域。

3. **图像平滑（Smoothing）**：
   - 使用双边滤波（Bilateral Filter）对修复区域进行平滑处理，保留边缘信息。

4. **逐帧处理**：
   - 视频被逐帧读取，每一帧都经过掩码生成、修复和平滑处理。
   - 处理后的帧被写入输出视频文件。

## 使用方法

### 安装依赖
确保已安装以下 Python 库：
```bash
pip install opencv-python numpy tqdm
运行程序

将需要处理的视频文件放置在项目目录下，例如 test.mp4。
修改 main 函数中的输入和输出文件路径（可选）：
python
复制
if __name__ == "__main__":
    input_file = 'test.mp4'  # 输入视频文件路径
    output_file = 'output_no_watermark.mp4'  # 输出视频文件路径
    remove_watermarks(input_file, output_file)
运行脚本：
bash
复制
python remove_watermark.py
操作说明

程序会显示视频的第一帧，用户需要通过鼠标左键点击选择水印区域。
点击一次选择矩形的一个角，再次点击选择对角的另一个角。
按 z 撤销上一步选择。
按 q 完成选择并开始处理。
程序会逐帧处理视频，去除水印并生成输出视频。
示例

输入

输入视频：test.mp4（包含水印的视频文件）。
输出

输出视频：output_no_watermark.mp4（去除水印后的视频文件）。
注意事项

性能问题：
Inpainting 和双边滤波计算量较大，处理高分辨率视频时可能较慢。
建议在处理前对视频进行分辨率调整或裁剪。
水印复杂度：
对于大面积或复杂的水印，修复效果可能不够理想。
可以考虑使用更高级的图像处理技术或深度学习模型。
动态水印：
如果水印在视频中移动或变化，该方法可能无法处理。
需要扩展功能以支持动态水印检测和跟踪。
依赖项

Python 3.x
OpenCV (opencv-python)
NumPy (numpy)
tqdm (tqdm)
许可证

本项目基于 MIT 许可证开源。详情请参阅 LICENSE 文件。

项目结构

复制
video-watermark-removal/
├── remove_watermark.py  # 主程序脚本
├── test.mp4             # 示例输入视频
├── output_no_watermark.mp4  # 示例输出视频
├── README.md            # 项目说明文件
└── requirements.txt     # 依赖项列表（可选）
贡献与反馈

欢迎提交 Issue 或 Pull Request 来改进本项目！如果有任何问题或建议，请通过 GitHub Issues 反馈。