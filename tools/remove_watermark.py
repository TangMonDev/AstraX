import cv2
import numpy as np

# 全局变量
coords = []  # 存储用户选择的水印区域坐标
img = None  # 存储视频的第一帧图像
drawing = False  # 标记是否正在绘制矩形
current_pos = (-1, -1)  # 当前鼠标位置

def draw_rectangle(event, x, y, flags, param):
    """
    鼠标回调函数，用于处理鼠标事件（点击和移动）
    """
    global coords, img, drawing, current_pos
    
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        if not drawing:  # 如果未开始绘制
            coords.append((x, y))  # 记录起始点
            drawing = True  # 标记为正在绘制
            print(f"Start point: x={x}, y={y}")
        else:  # 如果已经开始绘制
            coords.append((x, y))  # 记录结束点
            drawing = False  # 标记为绘制完成
            print(f"End point: x={x}, y={y}")
            redraw()  # 重绘图像

    elif event == cv2.EVENT_MOUSEMOVE:  # 鼠标移动
        current_pos = (x, y)  # 更新当前鼠标位置
        if drawing:  # 如果正在绘制
            redraw(temp_rect=(coords[-1], current_pos))  # 重绘图像并显示临时矩形
        else:
            redraw()  # 仅重绘图像

def redraw(temp_rect=None):
    """
    重绘图像，显示已选定的矩形和当前鼠标位置
    """
    img_copy = img.copy()  # 复制原始图像

    # 画出所有已完成的矩形（确保坐标数量为偶数）
    if len(coords) % 2 == 0:
        for i in range(0, len(coords), 2):
            cv2.rectangle(img_copy, coords[i], coords[i + 1], (0, 255, 0), 2)  # 绿色框

    # 绘制动态矩形（正在绘制中）
    if temp_rect:
        cv2.rectangle(img_copy, temp_rect[0], temp_rect[1], (255, 0, 0), 1)  # 蓝色框

    # 显示当前鼠标位置
    x, y = current_pos
    cv2.putText(img_copy, f"({x}, {y})", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, (255, 255, 255), 1)  # 白色文字

    cv2.imshow("Select Watermark", img_copy)  # 显示更新后的图像

def select_watermark_position(video_path):
    """
    选择水印区域的主函数
    """
    global coords, img, drawing
    
    # 读取视频第一帧
    cap = cv2.VideoCapture(video_path)
    ret, img = cap.read()
    cap.release()

    if not ret:  # 如果读取失败
        print("❌ Error: Cannot read video frame.")
        return []

    cv2.imshow("Select Watermark", img)  # 显示第一帧图像
    cv2.setMouseCallback("Select Watermark", draw_rectangle)  # 设置鼠标回调函数

    print("👉 左键点击选择水印区域，按 'q' 结束选择，'z' 撤销")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # 按 'q' 完成选择
            break
        elif key == ord('z'):  # 按 'z' 撤销上一步
            if len(coords) >= 2:
                coords = coords[:-2]  # 删除最后两个坐标
                print("↩️  Undo last selection.")
                redraw()  # 重绘图像

    cv2.destroyAllWindows()  # 关闭所有窗口

    # 整理结果，将坐标转换为 (x, y, w, h) 格式
    positions = []
    if len(coords) % 2 == 0:
        for i in range(0, len(coords), 2):
            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            x1, x2 = sorted([x1, x2])  # 确保 x1 < x2
            y1, y2 = sorted([y1, y2])  # 确保 y1 < y2
            w, h = x2 - x1, y2 - y1  # 计算宽度和高度
            positions.append((x1, y1, w, h))  # 添加到结果列表

    return positions  # 返回水印区域的位置信息

def remove_watermarks(input_file, output_file):
    """
    去除水印的主函数
    """
    from tqdm import tqdm  # 导入进度条库
    
    positions = select_watermark_position(input_file)  # 选择水印区域
    if not positions:  # 如果未选择任何区域
        print("❌ Watermark position not selected.")
        return
    
    cap = cv2.VideoCapture(input_file)  # 打开输入视频
    
    # 获取视频参数
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))  # 视频编码格式
    fps = cap.get(cv2.CAP_PROP_FPS)  # 帧率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 视频宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 视频高度
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 总帧数
    
    # 定义输出视频
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    print(f"🎯 Starting watermark removal for {total_frames} frames...")

    with tqdm(total=total_frames, desc="Processing", unit="frame") as pbar:  # 创建进度条
        while True:
            ret, frame = cap.read()  # 读取一帧
            if not ret:  # 如果读取失败
                break

            # 修复所有选择的水印区域
            for (x, y, w, h) in positions:
                # 生成掩码
                mask = np.zeros(frame.shape[:2], dtype=np.uint8)  # 创建全黑掩码
                mask[y:y+h, x:x+w] = 255  # 将水印区域设为白色

                # 使用 inpaint 方法修复
                frame = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)

                # 使用更平滑的模糊效果
                frame[y:y+h, x:x+w] = cv2.bilateralFilter(frame[y:y+h, x:x+w], 9, 75, 75)

            # 写入输出视频
            out.write(frame)
            pbar.update(1)  # 更新进度条

    cap.release()  # 释放视频捕获对象
    out.release()  # 释放视频写入对象

    print("\n✅ Watermark removal completed!")  # 完成提示

if __name__ == "__main__":
    input_file = 'test.mp4'  # 输入视频文件路径
    output_file = 'output_no_watermark.mp4'  # 输出视频文件路径
    
    remove_watermarks(input_file, output_file)  # 调用主函数