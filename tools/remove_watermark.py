# import cv2
# import numpy as np

# # 全局变量
# coords = []
# img = None
# img_copy = None

# def draw_all_boxes():
#     """在图像上绘制所有已选的矩形框"""
#     global img_copy
#     img_copy = img.copy()
#     for i in range(0, len(coords), 2):
#         x1, y1 = coords[i]
#         x2, y2 = coords[i + 1]
#         cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     cv2.imshow("Image", img_copy)

# def click_event(event, x, y, flags, param):
#     global coords, img_copy

#     if event == cv2.EVENT_LBUTTONDOWN:
#         if len(coords) % 2 == 0:
#             coords.append((x, y))
#             print(f"Clicked at: x={x}, y={y} (Start)")
#         else:
#             coords.append((x, y))
#             print(f"Clicked at: x={x}, y={y} (End)")
#             draw_all_boxes()

#     elif event == cv2.EVENT_MOUSEMOVE and len(coords) % 2 == 1:
#         x1, y1 = coords[-1]
#         temp_img = img_copy.copy()
#         cv2.rectangle(temp_img, (x1, y1), (x, y), (255, 0, 0), 1)
#         cv2.imshow("Image", temp_img)

#     elif event == cv2.EVENT_RBUTTONDOWN:
#         if len(coords) >= 2:
#             coords.pop()
#             coords.pop()
#             print("Removed last selected area.")
#             draw_all_boxes()

# def remove_watermarks(input_file, output_file):
#     """去除所有选定区域的水印"""
#     cap = cv2.VideoCapture(input_file)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_file, fourcc, cap.get(cv2.CAP_PROP_FPS),
#                           (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     print(f"👉 开始处理视频，总帧数: {frame_count}")

#     frame_idx = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         for i in range(0, len(coords), 2):
#             x1, y1 = coords[i]
#             x2, y2 = coords[i + 1]
#             w, h = x2 - x1, y2 - y1

#             # ✅ 确保坐标在图像内
#             x1, y1 = max(x1, 0), max(y1, 0)
#             x2, y2 = min(x2, frame.shape[1]), min(y2, frame.shape[0])
#             w, h = x2 - x1, y2 - y1

#             if w > 0 and h > 0:
#                 # ✅ 生成掩码
#                 mask = np.zeros(frame.shape[:2], np.uint8)
#                 mask[y1:y2, x1:x2] = 255

#                 # ✅ 显示掩码（用于调试）
#                 debug_mask = cv2.bitwise_and(frame, frame, mask=mask)
#                 cv2.imshow("Mask Preview", debug_mask)
#                 cv2.waitKey(1)

#                 # ✅ 使用 seamlessClone 替代 inpaint
#                 center = (x1 + w // 2, y1 + h // 2)
#                 replacement = cv2.GaussianBlur(frame[y1:y2, x1:x2], (11, 11), 0)
#                 frame[y1:y2, x1:x2] = replacement

#             else:
#                 print(f"⚠️ 跳过无效区域: x={x1}, y={y1}, w={w}, h={h}")

#         out.write(frame)
#         frame_idx += 1

#         if frame_idx % 100 == 0:
#             print(f"已处理帧数: {frame_idx}/{frame_count}")

#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
#     print("✅ 水印处理完成！")

# def main():
#     global img, img_copy

#     input_file = 'test.mp4'
#     output_file = 'output_no_watermark.mp4'

#     cap = cv2.VideoCapture(input_file)
#     if not cap.isOpened():
#         print("Error: Could not open video file.")
#         return
    
#     ret, img = cap.read()
#     cap.release()

#     if not ret:
#         print("Error: Could not read video frame.")
#         return

#     img_copy = img.copy()

#     cv2.imshow('Image', img_copy)
#     cv2.setMouseCallback('Image', click_event)

#     print("👉 左键点击选择水印区域，右键撤销最后一个框，按 'q' 退出并处理水印")

#     while True:
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cv2.destroyAllWindows()

#     if len(coords) >= 2:
#         print("\n✅ 选择的水印区域：")
#         for i in range(0, len(coords), 2):
#             x1, y1 = coords[i]
#             x2, y2 = coords[i + 1]
#             w, h = x2 - x1, y2 - y1
#             print(f"👉 区域 {i//2 + 1}: x={x1}, y={y1}, w={w}, h={h}")

#         # 🚀 调用水印修复函数
#         remove_watermarks(input_file, output_file)
#     else:
#         print("\n❌ 未完整选择水印区域")

# if __name__ == "__main__":
#     main()

#############################################
import cv2
import numpy as np

# 存储水印位置
coords = []
ready = False

def click_event(event, x, y, flags, param):
    global coords, ready
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        print(f"Clicked at: x={x}, y={y}")

        if len(coords) == 2:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            w, h = x2 - x1, y2 - y1
            print(f"Watermark position -> x={x1}, y={y1}, w={w}, h={h}")
            ready = True

def select_watermark_position(video_path):
    global coords, ready
    
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Error: Cannot read video frame.")
        return None

    cv2.imshow("Select Watermark", frame)
    cv2.setMouseCallback("Select Watermark", click_event)

    # 等待选择完成
    while not ready:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    if len(coords) == 2:
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        return (x1, y1, x2 - x1, y2 - y1)  # 返回 (x, y, w, h)
    else:
        return None

def remove_watermark(input_file, output_file):
    # 定位水印
    position = select_watermark_position(input_file)
    if not position:
        print("Watermark position not selected.")
        return
    
    x, y, w, h = position

    cap = cv2.VideoCapture(input_file)
    
    # 获取视频参数
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 生成掩码
        mask = np.zeros(frame.shape[:2], np.uint8)
        mask[y:y+h, x:x+w] = 255
        
        # 使用 inpaint 方法修复
        frame = cv2.inpaint(frame, mask, 3, cv2.INPAINT_NS)  # 使用 Navier-Stokes 方法修复
        
        # 平滑修复区域和边缘
        frame[y:y+h, x:x+w] = cv2.GaussianBlur(frame[y:y+h, x:x+w], (5, 5), 0)
        
        out.write(frame)

        frame_count += 1
        print(f"Processing frame {frame_count}/{total_frames}", end="\r")

    cap.release()
    out.release()
    print("\nWatermark removal completed.")

# 示例用法
remove_watermark('test.mp4', 'output_no_watermark.mp4')