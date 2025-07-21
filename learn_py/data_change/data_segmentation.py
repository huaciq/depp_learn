import os
import shutil
import random
from tqdm import tqdm

# --- 配置参数 ---
IMAGE_DIR = r'E:\TWHD\mydata\images'  # 你的图片文件路径
LABEL_DIR = r'E:\TWHD\mydata\labels'  # 你的标注文件路径 (txt格式, YOLO)
OUTPUT_BASE_DIR = r'E:\TWHD\split_data' # 输出数据集的根目录，会在这个目录下创建 images 和 labels 子目录

TRAIN_RATIO = 0.8 # 训练集比例 (80%)
VAL_RATIO = 1 - TRAIN_RATIO # 验证集比例 (20%)

# 确保随机性，可以设置一个固定的随机种子以便重现划分结果
# 如果每次都想要不同的划分结果，可以注释掉下一行
random.seed(42)

# --- 创建输出目录结构 (根据你的要求修改) ---
# 原始: OUTPUT_TRAIN_IMG_DIR = os.path.join(OUTPUT_BASE_DIR, 'train', 'images')
# 修改后:
OUTPUT_TRAIN_IMG_DIR = os.path.join(OUTPUT_BASE_DIR, 'images', 'train')
OUTPUT_VAL_IMG_DIR = os.path.join(OUTPUT_BASE_DIR, 'images', 'val')
OUTPUT_TRAIN_LABEL_DIR = os.path.join(OUTPUT_BASE_DIR, 'labels', 'train')
OUTPUT_VAL_LABEL_DIR = os.path.join(OUTPUT_BASE_DIR, 'labels', 'val')


# 创建目录 (如果不存在)
# os.makedirs 配合 exist_ok=True 可以创建多级目录
os.makedirs(OUTPUT_TRAIN_IMG_DIR, exist_ok=True)
os.makedirs(OUTPUT_TRAIN_LABEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_VAL_IMG_DIR, exist_ok=True)
os.makedirs(OUTPUT_VAL_LABEL_DIR, exist_ok=True)


print(f"输入图片目录: {IMAGE_DIR}")
print(f"输入标注目录: {LABEL_DIR}")
print(f"输出数据集根目录: {OUTPUT_BASE_DIR}")
print(f"训练集比例: {TRAIN_RATIO:.0%}")
print(f"验证集比例: {VAL_RATIO:.0%}")
print(f"输出图片训练集目录: {OUTPUT_TRAIN_IMG_DIR}")
print(f"输出图片验证集目录: {OUTPUT_VAL_IMG_DIR}")
print(f"输出标注训练集目录: {OUTPUT_TRAIN_LABEL_DIR}")
print(f"输出标注验证集目录: {OUTPUT_VAL_LABEL_DIR}")


# --- 获取图片文件列表并校验对应的标注文件 ---
print("正在扫描图片目录并校验标注文件...")
image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]

# 过滤出有对应标注文件的图片
valid_files = []
missing_labels_count = 0
for img_file in tqdm(image_files, desc="校验标注文件"):
    name, ext = os.path.splitext(img_file)
    label_file = name + '.txt'
    label_path = os.path.join(LABEL_DIR, label_file)
    if os.path.exists(label_path):
        valid_files.append(img_file)
    else:
        missing_labels_count += 1

print(f"找到 {len(image_files)} 张图片文件。")
print(f"其中 {len(valid_files)} 张图片有对应的标注文件，将用于划分。")
if missing_labels_count > 0:
     print(f"{missing_labels_count} 张图片没有找到对应的标注文件，已忽略。")

if not valid_files:
    print("没有找到有效的图片-标注对，脚本结束。")
    exit()

# --- 随机打乱文件列表 ---
print("正在随机打乱文件列表...")
random.shuffle(valid_files)

# --- 计算划分数量并进行划分 ---
total_files = len(valid_files)
train_count = int(total_files * TRAIN_RATIO)
val_count = total_files - train_count # 确保总数正确

train_files = valid_files[:train_count]
val_files = valid_files[train_count:]

print(f"计划划分: 训练集 {len(train_files)} 个文件，验证集 {len(val_files)} 个文件。")

# --- 复制文件到目标目录 ---

# 复制训练集文件
print("正在复制训练集文件...")
for img_file in tqdm(train_files, desc="复制训练集"):
    name, ext = os.path.splitext(img_file)
    label_file = name + '.txt'

    src_img_path = os.path.join(IMAGE_DIR, img_file)
    src_label_path = os.path.join(LABEL_DIR, label_file)

    dst_img_path = os.path.join(OUTPUT_TRAIN_IMG_DIR, img_file)
    dst_label_path = os.path.join(OUTPUT_TRAIN_LABEL_DIR, label_file)

    try:
        shutil.copy(src_img_path, dst_img_path)
        shutil.copy(src_label_path, dst_label_path)
    except Exception as e:
        print(f"错误: 复制文件 {img_file} 及其标注到训练集时发生错误: {e}")


# 复制验证集文件
print("正在复制验证集文件...")
for img_file in tqdm(val_files, desc="复制验证集"):
    name, ext = os.path.splitext(img_file)
    label_file = name + '.txt'

    src_img_path = os.path.join(IMAGE_DIR, img_file)
    src_label_path = os.path.join(LABEL_DIR, label_file)

    dst_img_path = os.path.join(OUTPUT_VAL_IMG_DIR, img_file)
    dst_label_path = os.path.join(OUTPUT_VAL_LABEL_DIR, label_file)

    try:
        shutil.copy(src_img_path, dst_img_path)
        shutil.copy(src_label_path, dst_label_path)
    except Exception as e:
        print(f"错误: 复制文件 {img_file} 及其标注到验证集时发生错误: {e}")

print("\n数据集划分及复制完成！")
print(f"训练集图片数量: {len(os.listdir(OUTPUT_TRAIN_IMG_DIR))}")
print(f"训练集标注数量: {len(os.listdir(OUTPUT_TRAIN_LABEL_DIR))}")
print(f"验证集图片数量: {len(os.listdir(OUTPUT_VAL_IMG_DIR))}")
print(f"验证集标注数量: {len(os.listdir(OUTPUT_VAL_LABEL_DIR))}")