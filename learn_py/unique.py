import os
from PIL import Image
import imagehash

# 路径配置（你可以直接运行这段代码）
image_dir = r"E:\文件夹集合\毕设过程材料\Code_Data\KY002：电动车佩戴头盔检测数据集（TWHD）\helmetdataset\JPEGImages"
label_dir = r"E:\文件夹集合\毕设过程材料\Code_Data\KY002：电动车佩戴头盔检测数据集（TWHD）\helmetdataset\labels"

# 支持的图片格式
image_extensions = ['.jpg', '.jpeg', '.png']

# 记录删除统计
deleted_empty_labels = 0
deleted_duplicates = 0

print(">>> 第一步：删除空标注及其对应图片...")
for label_file in os.listdir(label_dir):
    label_path = os.path.join(label_dir, label_file)

    # 如果标注为空（文件大小为 0 或只包含空白符）
    if os.path.getsize(label_path) == 0 or open(label_path).read().strip() == "":
        base_name = os.path.splitext(label_file)[0]

        # 删除对应的图片
        for ext in image_extensions:
            image_path = os.path.join(image_dir, base_name + ext)
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"已删除空标注图片: {image_path}")

        os.remove(label_path)
        deleted_empty_labels += 1

print(f"已删除空标注及其图片共计：{deleted_empty_labels} 对。")

print("\n>>> 第二步：删除重复率过高的图片（感知哈希）...")
hash_dict = {}
similarity_threshold = 10  # 汉明距离阈值（0-5之间越小越严格）

for filename in os.listdir(image_dir):
    filepath = os.path.join(image_dir, filename)
    try:
        with Image.open(filepath) as img:
            img_hash = imagehash.phash(img)
    except Exception as e:
        print(f"跳过无法处理的图片：{filename}，原因：{e}")
        continue

    is_duplicate = False
    for existing_hash in hash_dict:
        if abs(img_hash - existing_hash) <= similarity_threshold:
            is_duplicate = True
            break

    if is_duplicate:
        os.remove(filepath)
        print(f"已删除重复图片: {filepath}")
        deleted_duplicates += 1
    else:
        hash_dict[img_hash] = filename

print(f"已删除重复图片共计：{deleted_duplicates} 张。")
