import xml.etree.ElementTree as ET
import os
from PIL import Image # 需要安装 Pillow: pip install Pillow
import tqdm # 用于显示进度条: pip install tqdm


# Xml转YOLO格式脚本
# --- 必须配置：定义你的类别和对应的索引 ---
# 例如: 如果你的 XML 里有 "helmet" 和 "person" 两种类别
# CLASS_MAP = {
#     "helmet": 0,
#     "person": 1,
# }
# 请根据你的 XML 文件中的实际 <name> 标签内容来修改这个字典！
CLASS_MAP = {
    "two_wheeler": 0,
    "helmet": 1,  # 如果还有其他类别，像这样添加
    "without_helmet": 2, # 索引必须从 0 开始，连续增加
    # 添加你数据集中所有的类别名称...
}
# ------------------------------------------

def convert_xml_to_yolo(xml_dir, image_dir, output_dir, class_map):
    """
    将 PASCAL VOC XML 标注转换为 YOLO TXT 格式。

    Args:
        xml_dir (str): 包含 XML 标注文件的目录路径。
        image_dir (str): 包含对应图像文件的目录路径。
        output_dir (str): 保存 YOLO 格式标注文件的输出目录路径。
        class_map (dict): 类别名称到整数索引的映射字典。
    """

    print("--- 开始转换 XML 到 YOLO ---")
    print(f"XML 目录: {xml_dir}")
    print(f"图像目录: {image_dir}")
    print(f"输出目录: {output_dir}")
    print(f"类别映射: {class_map}")

    # --- 检查输入目录 ---
    if not os.path.isdir(xml_dir):
        print(f"错误: XML 目录 '{xml_dir}' 不存在。")
        return
    if not os.path.isdir(image_dir):
        print(f"错误: 图像目录 '{image_dir}' 不存在。")
        return

    # --- 创建输出目录 ---
    os.makedirs(output_dir, exist_ok=True)
    print(f"输出目录 '{output_dir}' 已创建或已存在。")

    xml_files = [f for f in os.listdir(xml_dir) if f.lower().endswith('.xml')]
    print(f"找到 {len(xml_files)} 个 XML 文件，准备处理...")

    conversion_errors = 0
    skipped_files = 0
    processed_files = 0

    # --- 遍历 XML 文件 ---
    # with tqdm.tqdm(total=len(xml_files), desc="转换进度") as pbar:
    for xml_filename in tqdm.tqdm(xml_files, desc="转换进度"):
        xml_basename = os.path.splitext(xml_filename)[0]
        xml_filepath = os.path.join(xml_dir, xml_filename)
        output_txt_filepath = os.path.join(output_dir, xml_basename + ".txt")

        # --- 查找对应的图像文件 ---
        image_path = None
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        for ext in possible_extensions:
            potential_image_path = os.path.join(image_dir, xml_basename + ext)
            if os.path.exists(potential_image_path):
                image_path = potential_image_path
                break

        if image_path is None:
            print(f"\n警告：找不到 XML 文件 '{xml_filename}' 对应的图像。跳过此文件。")
            skipped_files += 1
            # pbar.update(1)
            continue

        # --- 获取实际图像尺寸 ---
        try:
            with Image.open(image_path) as img:
                img_width, img_height = img.size
            if img_width <= 0 or img_height <= 0:
                print(f"\n警告：图像 '{image_path}' 的尺寸无效 ({img_width}x{img_height})。跳过 XML 文件 '{xml_filename}'。")
                skipped_files += 1
                # pbar.update(1)
                continue
        except Exception as e:
            print(f"\n错误：无法打开或读取图像 '{image_path}': {e}。跳过 XML 文件 '{xml_filename}'。")
            skipped_files += 1
            # pbar.update(1)
            continue

        # --- 解析 XML 文件 ---
        yolo_annotations = []
        try:
            tree = ET.parse(xml_filepath)
            root = tree.getroot()

            # 有些 XML 可能没有 <size> 标签，但我们已经从图像文件获取了实际尺寸
            # xml_size = root.find('size')
            # if xml_size:
            #     xml_width = int(xml_size.find('width').text)
            #     xml_height = int(xml_size.find('height').text)
            #     # 可选：检查XML尺寸与实际图像尺寸是否一致
            #     if xml_width != img_width or xml_height != img_height:
            #         print(f"\n警告: XML '{xml_filename}' 中的尺寸 ({xml_width}x{xml_height}) 与实际图像尺寸 ({img_width}x{img_height}) 不符。将使用实际图像尺寸进行归一化。")
            # else:
                 # 如果 XML 中没有尺寸信息，依赖从图像读取的尺寸
                # print(f"\n信息: XML '{xml_filename}' 中未找到 <size> 标签，使用图像文件尺寸 {img_width}x{img_height}。")
                # pass # 已经从 Image.open 获取了 img_width, img_height

            # --- 提取每个对象的信息 ---
            object_found = False
            for obj in root.findall('object'):
                object_found = True
                class_name = obj.find('name').text
                if class_name not in class_map:
                    print(f"\n警告：在 XML 文件 '{xml_filename}' 中发现未知类别 '{class_name}' (未在 CLASS_MAP 中定义)。跳过此对象。")
                    continue # 跳过这个对象

                class_id = class_map[class_name]

                bndbox = obj.find('bndbox')
                if bndbox is None:
                     print(f"\n警告：XML 文件 '{xml_filename}' 中的对象 '{class_name}' 缺少 <bndbox> 标签。跳过此对象。")
                     continue

                # 获取边界框坐标并转换为浮点数
                try:
                    xmin = float(bndbox.find('xmin').text)
                    ymin = float(bndbox.find('ymin').text)
                    xmax = float(bndbox.find('xmax').text)
                    ymax = float(bndbox.find('ymax').text)
                except (ValueError, AttributeError) as e:
                     print(f"\n警告：无法解析 XML 文件 '{xml_filename}' 对象 '{class_name}' 的边界框坐标: {e}。跳过此对象。")
                     continue


                # --- 坐标验证 ---
                # 1. 检查基本逻辑
                if xmin >= xmax or ymin >= ymax:
                    print(f"\n警告: XML '{xml_filename}' 对象 '{class_name}' 坐标无效 (min >= max): xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}。跳过此对象。")
                    continue
                # 2. 检查是否超出图像边界 (允许稍微超出一点点，或者严格限制在内部)
                #    将坐标限制在图像范围内
                xmin = max(0.0, xmin)
                ymin = max(0.0, ymin)
                xmax = min(img_width, xmax)
                ymax = min(img_height, ymax)
                #    再次检查修正后是否还有效 (例如，如果xmax原本小于0，修正后xmin和xmax可能都为0)
                if xmin >= xmax or ymin >= ymax:
                    print(f"\n警告: XML '{xml_filename}' 对象 '{class_name}' 坐标修正后无效或完全在图像外。跳过此对象。")
                    continue


                # --- 计算 YOLO 格式 ---
                dw = 1.0 / img_width
                dh = 1.0 / img_height
                x_center = (xmin + xmax) / 2.0
                y_center = (ymin + ymax) / 2.0
                width = xmax - xmin
                height = ymax - ymin

                x_center_norm = x_center * dw
                y_center_norm = y_center * dh
                width_norm = width * dw
                height_norm = height * dh

                # 确保值在 [0.0, 1.0] 范围内 (防止浮点数精度问题)
                x_center_norm = max(0.0, min(1.0, x_center_norm))
                y_center_norm = max(0.0, min(1.0, y_center_norm))
                width_norm = max(0.0, min(1.0, width_norm))
                height_norm = max(0.0, min(1.0, height_norm))

                yolo_annotations.append(f"{class_id} {x_center_norm:.6f} {y_center_norm:.6f} {width_norm:.6f} {height_norm:.6f}")

            # 如果 XML 文件中没有找到任何 <object> 标签
            # if not object_found:
            #    print(f"\n信息: XML 文件 '{xml_filename}' 不包含任何 <object> 标签。将创建一个空的 TXT 文件。")
            #    pass # 会创建一个空的txt文件，这通常是期望的行为

        except ET.ParseError as e:
            print(f"\n错误：解析 XML 文件 '{xml_filepath}' 时出错: {e}。跳过此文件。")
            conversion_errors += 1
            # pbar.update(1)
            continue
        except Exception as e:
            print(f"\n处理 XML 文件 '{xml_filepath}' 时发生意外错误: {e}。跳过此文件。")
            conversion_errors += 1
            # pbar.update(1)
            continue

        # --- 写入 YOLO TXT 文件 ---
        try:
            # 即使没有对象，也创建一个空的 txt 文件，这对于某些训练框架是必要的
            with open(output_txt_filepath, 'w') as f_out:
                 for line in yolo_annotations:
                     f_out.write(line + '\n')
            processed_files += 1
        except Exception as e:
            print(f"\n错误：写入 YOLO 标注文件 '{output_txt_filepath}' 时出错: {e}。")
            conversion_errors += 1

        # pbar.update(1) # 更新进度条

    print("\n--------------------")
    print("转换完成!")
    print(f"成功处理并写入 TXT 文件数: {processed_files}")
    print(f"因图像缺失或无效而跳过的 XML 文件数: {skipped_files}")
    print(f"因解析或写入错误而失败的文件数: {conversion_errors}")
    print(f"归一化后的标注文件保存在: '{output_dir}'")
    if any("未知类别" in msg for msg in tqdm.tqdm.write.messages): # 检查是否有未知类别警告
         print("\n警告：转换过程中发现未知类别，请检查上面的输出并更新 CLASS_MAP。")
    print("--------------------")


# --- 配置您的路径 ---
XML_DIR = r"E:\TWHD\helmetdataset\Annotations"
IMAGE_DIR = r"E:\TWHD\helmetdataset\JPEGImages"
OUTPUT_DIR = r"E:\TWHD\helmetdataset\labels_yolo" # YOLO txt 文件输出目录

# --- 运行转换 ---
if __name__ == "__main__":
    # 在运行前再次确认 CLASS_MAP 是否已正确定义！
    if not CLASS_MAP:
        print("错误：请在脚本顶部定义 CLASS_MAP 字典！")
    else:
        convert_xml_to_yolo(XML_DIR, IMAGE_DIR, OUTPUT_DIR, CLASS_MAP)