import os
import cv2
import numpy as np

# --- 配置区域 ---
# 定义图片和标注文件夹路径
image_folder = r"E:\TWHD\N_mydata\images\val"
label_folder = r"E:\TWHD\N_mydata\labels\val"

# 定义保存结果的输出文件夹路径
output_folder = r"E:\TWHD\mydata\annotated_images" # 新的输出文件夹路径

# 定义可选的类别文件路径 (如果你的标注文件包含类别ID，且你想显示类别名称)
# 例如：classes.txt 文件每行一个类别名称，顺序与标注文件中的 class_id 对应 (从0开始)
classes_file = r"E:\TWHD\mydata\classes.txt" # 替换为你的类别文件路径，如果没有可以设为 None

# 定义 bounding box 的颜色和线条粗细
bbox_color = (0, 255, 0)  # 绿色 (BGR格式)
bbox_thickness = 2

# 定义文本颜色和字体
text_color = (0, 0, 0) # 黑色
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 0.5
text_thickness = 1
text_background_color = bbox_color # 与框同色作为背景

# --- 代码开始 ---

# 可选：加载类别名称
class_names = []
if classes_file and os.path.exists(classes_file):
    try:
        with open(classes_file, 'r', encoding='utf-8') as f:
            class_names = [line.strip() for line in f.readlines()]
        print(f"成功加载 {len(class_names)} 个类别名称。")
    except Exception as e:
        print(f"加载类别文件失败: {e}")
        class_names = []
else:
    print("未找到类别文件或路径错误，将只显示类别ID。")


def save_annotated_images(image_dir, label_dir, output_dir, class_names=None):
    """
    读取图片和标注，绘制标注框，并将结果保存到新的文件夹。

    Args:
        image_dir (str): 图片文件夹路径。
        label_dir (str): 标注文件夹路径。
        output_dir (str): 保存带标注图片的新文件夹路径。
        class_names (list, optional): 类别名称列表。默认为 None。
    """
    if not os.path.isdir(image_dir):
        print(f"错误：图片文件夹 '{image_dir}' 不存在。")
        return

    if not os.path.isdir(label_dir):
        print(f"错误：标注文件夹 '{label_dir}' 不存在。")
        return

    # 创建输出文件夹如果不存在
    os.makedirs(output_dir, exist_ok=True)
    print(f"确保输出文件夹存在: {output_dir}")

    print(f"正在扫描图片文件夹: {image_dir}")

    # 获取图片文件夹中的所有文件
    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    image_files.sort() # 按字母顺序排序处理

    if not image_files:
        print("图片文件夹中没有找到任何文件。")
        return

    print(f"找到 {len(image_files)} 个图片文件。")
    print("开始处理图片和标注，并保存结果...")

    processed_count = 0
    saved_count = 0

    for image_filename in image_files:
        image_path = os.path.join(image_dir, image_filename)
        name, image_ext = os.path.splitext(image_filename)

        # 构建对应的标注文件路径 (假设标注文件和图片同名，扩展名不同)
        # 常见的标注扩展名是 .txt，你可以根据实际情况修改
        label_filename = name + ".txt"
        label_path = os.path.join(label_dir, label_filename)

        # 构建输出文件路径
        output_path = os.path.join(output_dir, image_filename)

        print(f"正在处理: {image_filename}")

        # 读取图片
        img = cv2.imread(image_path)

        if img is None:
            print(f"  警告：无法读取图片文件 '{image_filename}'，跳过。")
            continue

        # 获取图片尺寸
        img_height, img_width, _ = img.shape
        display_img = img.copy() # 复制图片用于绘制

        # 检查对应的标注文件是否存在
        if os.path.exists(label_path):
            print(f"  找到标注文件: {label_filename}")
            try:
                with open(label_path, 'r') as f:
                    annotations = f.readlines()

                if not annotations:
                    print(f"  标注文件 '{label_filename}' 为空。")

                for line in annotations:
                    line = line.strip()
                    if not line: # 跳过空行
                        continue

                    try:
                        # 解析 YOLO 格式标注: class_id center_x center_y width height
                        parts = line.split()
                        if len(parts) != 5:
                            print(f"  警告：标注文件 '{label_filename}' 中的行格式错误: '{line}'，跳过该行。")
                            continue

                        class_id = int(parts[0])
                        center_x = float(parts[1])
                        center_y = float(parts[2])
                        width = float(parts[3])
                        height = float(parts[4])

                        # 将归一化坐标转换为像素坐标
                        # 计算 bounding box 左上角和右下角坐标
                        x_center = center_x * img_width
                        y_center = center_y * img_height
                        box_width = width * img_width
                        box_height = height * img_height

                        x1 = int(x_center - box_width / 2)
                        y1 = int(y_center - box_height / 2)
                        x2 = int(x_center + box_width / 2)
                        y2 = int(y_center + box_height / 2)

                         # 确保坐标在图片范围内
                        x1 = max(0, x1)
                        y1 = max(0, y1)
                        x2 = min(img_width - 1, x2)
                        y2 = min(img_height - 1, y2)


                        # 绘制 bounding box
                        cv2.rectangle(display_img, (x1, y1), (x2, y2), bbox_color, bbox_thickness)

                        # 添加类别名称或ID文本
                        display_text = str(class_id)
                        if class_names and class_id < len(class_names):
                            display_text = class_names[class_id]
                        elif class_names and class_id >= len(class_names):
                            print(f"  警告：类别ID {class_id} 超出类别名称列表范围 ({len(class_names)})，显示原始ID。")


                        # 计算文本位置 (通常在 bounding box 左上角附近)
                        text_x = x1
                        text_y = y1 - 5 # 稍微向上偏移一点
                        if text_y < 0: # 如果太靠上，画在框内下方
                            text_y = y1 + 15 + int(cv2.getTextSize("Test", text_font, text_scale, text_thickness)[0][1])


                        # 添加文本背景
                        (text_width, text_height), baseline = cv2.getTextSize(display_text, text_font, text_scale, text_thickness)
                        cv2.rectangle(display_img, (text_x, text_y - text_height - baseline), (text_x + text_width, text_y), text_background_color, -1) # -1 填充矩形

                        # 添加文本
                        cv2.putText(display_img, display_text, (text_x, text_y), text_font, text_scale, text_color, text_thickness)


                    except ValueError as ve:
                        print(f"  警告：解析标注行时发生值错误 '{line}': {ve}，跳过该行。")
                    except IndexError as ie:
                         print(f"  警告：解析标注行时发生索引错误 '{line}': {ie}，请检查格式是否正确，跳过该行。")
                    except Exception as ex:
                        print(f"  警告：处理标注行时发生未知错误 '{line}': {ex}，跳过该行。")

            except Exception as e:
                print(f"  警告：读取或处理标注文件 '{label_filename}' 失败: {e}，该图片将不包含标注。")
        else:
             print(f"  未找到对应的标注文件: {label_filename}，图片将不包含标注。")
             # 如果没有标注文件，可以在图片上显示一条信息 (可选)
             # cv2.putText(display_img, "No annotations found", (10, 30), text_font, text_scale, (0, 0, 255), text_thickness) # 红色文字

        # 保存带有标注的图片
        try:
            cv2.imwrite(output_path, display_img)
            print(f"  已保存带标注图片到: {output_path}")
            saved_count += 1
        except Exception as e:
            print(f"  错误：保存图片 '{output_path}' 失败: {e}")

        processed_count += 1

    print(f"\n处理完成。共处理 {processed_count} 张图片。成功保存 {saved_count} 张带标注图片到 '{output_dir}'。")


# 运行保存标注图片函数
save_annotated_images(image_folder, label_folder, output_folder, class_names)