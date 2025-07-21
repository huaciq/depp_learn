import albumentations as A
import cv2
import os
import numpy as np
import random
from tqdm import tqdm
import warnings

# 屏蔽警告（例如 ShiftScaleRotate 的警告）
warnings.filterwarnings("ignore", category=UserWarning)

# --- 配置参数 ---
IMAGE_DIR = r"E:\TWHD\mydata\images"
LABEL_DIR = r"E:\TWHD\mydata\labels"
OUTPUT_IMAGE_DIR = r"E:\TWHD\mydata\augmented_images"
OUTPUT_LABEL_DIR = r"E:\TWHD\mydata\augmented_labels"

TARGET_TOTAL_IMAGES = 10000
CLASSES = ['two_wheeler', 'helmet', 'without_helmet']

AUGMENT_COUNT_HIGH = (6, 10)
AUGMENT_COUNT_LOW = (1, 3)

BBOX_PARAMS = A.BboxParams(format='yolo', label_fields=['class_labels'])

# --- 数据增强 Pipeline ---
augmentations = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=10, p=0.5, border_mode=cv2.BORDER_CONSTANT),
    A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.3),
    A.HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.3),
    A.GaussNoise(p=0.1),
    A.Blur(blur_limit=3, p=0.1),
    A.CoarseDropout(max_holes=8, max_height=32, max_width=32, fill_value=0, p=0.2),
], bbox_params=BBOX_PARAMS)

# --- 辅助函数 ---
def read_yolo_annotations(label_path):
    bboxes, class_labels = [], []
    if not os.path.exists(label_path):
        return bboxes, class_labels
    with open(label_path, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split()
            if len(parts) == 5:
                class_id, x_center, y_center, width, height = map(float, parts)
                bboxes.append([x_center, y_center, width, height, class_id])
                class_labels.append(CLASSES[int(class_id)])
    return bboxes, class_labels

def write_yolo_annotations(label_path, bboxes):
    with open(label_path, 'w') as f:
        for bbox in bboxes:
            class_id = int(bbox[4])
            x_c, y_c, w, h = bbox[:4]
            f.write(f"{class_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}\n")

# --- 主增强流程 ---
os.makedirs(OUTPUT_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"找到 {len(image_files)} 张原始图片。")

augmented_count = 0
original_count = 0

# 复制原图和标注
print("正在复制原始图片和标注...")
for image_file in tqdm(image_files):
    name, ext = os.path.splitext(image_file)
    label_file = name + '.txt'

    original_image_path = os.path.join(IMAGE_DIR, image_file)
    original_label_path = os.path.join(LABEL_DIR, label_file)
    output_image_path = os.path.join(OUTPUT_IMAGE_DIR, image_file)
    output_label_path = os.path.join(OUTPUT_LABEL_DIR, label_file)

    img = cv2.imread(original_image_path)
    if img is not None:
        cv2.imwrite(output_image_path, img)
        original_count += 1
    else:
        print(f"警告: 无法读取图片 {original_image_path}")
        continue

    if os.path.exists(original_label_path):
        with open(original_label_path, 'r') as f_in, open(output_label_path, 'w') as f_out:
            f_out.writelines(f_in.readlines())
    else:
        open(output_label_path, 'w').close()

print(f"已复制 {original_count} 张原始图片及其标注。")
current_total_images = original_count

# --- 数据增强部分 ---
print(f"开始数据增强，目标总数: {TARGET_TOTAL_IMAGES}")
for image_file in tqdm(image_files, desc="Processing for augmentation"):
    if current_total_images >= TARGET_TOTAL_IMAGES:
        break

    name, ext = os.path.splitext(image_file)
    label_file = name + '.txt'
    original_image_path = os.path.join(IMAGE_DIR, image_file)
    original_label_path = os.path.join(LABEL_DIR, label_file)

    img = cv2.imread(original_image_path)
    if img is None:
        continue

    bboxes, class_labels = read_yolo_annotations(original_label_path)
    contains_target_classes = any(label in ['helmet', 'without_helmet'] for label in class_labels)
    num_augmentations = random.randint(*AUGMENT_COUNT_HIGH) if contains_target_classes else random.randint(*AUGMENT_COUNT_LOW)

    for i in range(num_augmentations):
        if current_total_images >= TARGET_TOTAL_IMAGES:
            break
        try:
            transformed = augmentations(image=img, bboxes=bboxes, class_labels=class_labels)
            augmented_img = transformed['image']
            augmented_bboxes = transformed['bboxes']

            augmented_name = f"{name}_aug_{augmented_count}_{i}{ext}"
            augmented_label_name = f"{name}_aug_{augmented_count}_{i}.txt"

            output_aug_img_path = os.path.join(OUTPUT_IMAGE_DIR, augmented_name)
            output_aug_lbl_path = os.path.join(OUTPUT_LABEL_DIR, augmented_label_name)

            cv2.imwrite(output_aug_img_path, augmented_img)
            write_yolo_annotations(output_aug_lbl_path, augmented_bboxes)

            augmented_count += 1
            current_total_images += 1

        except Exception as e:
            print(f"增强错误: {image_file} - {e}")
            continue

# --- 完成报告 ---
print("\n数据增强完成！")
print(f"原始图片数量: {original_count}")
print(f"增强图片数量: {augmented_count}")
print(f"总图片数量: {current_total_images}")

output_images = [f for f in os.listdir(OUTPUT_IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
output_labels = [f for f in os.listdir(OUTPUT_LABEL_DIR) if f.lower().endswith('.txt')]
print(f"输出目录实际图片数量: {len(output_images)}")
print(f"输出目录实际标注数量: {len(output_labels)}")
