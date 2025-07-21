import os

# 设置路径
image_dir = r"E:\文件夹集合\毕设过程材料\Code_Data\TWHD\helmetdataset\JPEGImages"
label_dir = r"E:\文件夹集合\毕设过程材料\Code_Data\TWHD\helmetdataset\labels"

# 支持的图片扩展名
image_exts = ['.jpg', '.jpeg', '.png']

# 统计删除数量
deleted_labels = 0

# 获取所有现存图片的基础文件名（不含扩展名）
image_basenames = set()
for file in os.listdir(image_dir):
    name, ext = os.path.splitext(file)
    if ext.lower() in image_exts:
        image_basenames.add(name)

# 遍历所有标注文件
for label_file in os.listdir(label_dir):
    label_name, _ = os.path.splitext(label_file)
    if label_name not in image_basenames:
        label_path = os.path.join(label_dir, label_file)
        os.remove(label_path)
        deleted_labels += 1
        print(f"已删除无对应图片的标注文件: {label_path}")

print(f"\n共删除无效标注文件数: {deleted_labels}")
