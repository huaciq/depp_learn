import os
import cv2
import xml.etree.ElementTree as ET

# 图片和标注路径
image_dir = r"E:\TWHD\helmetdataset\JPEGImages"
label_dir = r"E:\TWHD\helmetdataset\Annotations"
output_dir = r"E:\TWHD\helmetdataset\vis_labels"

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 获取所有xml标注文件
xml_files = [f for f in os.listdir(label_dir) if f.endswith(".xml")]

# 遍历所有xml标注文件
for xml_file in xml_files:
    image_name = os.path.splitext(xml_file)[0] + ".jpg"
    image_path = os.path.join(image_dir, image_name)
    xml_path = os.path.join(label_dir, xml_file)

    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ 无法读取图片: {image_path}")
        continue

    # 解析xml文件
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 获取标注框
    for obj in root.findall("object"):
        # 获取类别
        cls_name = obj.find("name").text
        # 获取标注框信息
        bndbox = obj.find("bndbox")
        x_min = int(bndbox.find("xmin").text)
        y_min = int(bndbox.find("ymin").text)
        x_max = int(bndbox.find("xmax").text)
        y_max = int(bndbox.find("ymax").text)

        # 画标注框
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv2.putText(image, cls_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 0), 2, lineType=cv2.LINE_AA)

    # 保存可视化图像
    output_path = os.path.join(output_dir, image_name)
    cv2.imwrite(output_path, image)
    print(f"✅ 保存可视化图像: {output_path}")

print("🎉 所有图片可视化完成！")
