import os
import sys

def clean_orphan_annotations(image_dir, annotation_dir):
    """
    删除在图像目录中没有对应图像文件的XML标注文件。

    Args:
        image_dir (str): 包含图像文件的目录路径 (例如 JPEGImages)。
        annotation_dir (str): 包含XML标注文件的目录路径 (例如 Annotations)。
    """

    print(f"图像目录: {image_dir}")
    print(f"标注目录: {annotation_dir}")

    # --- 检查目录是否存在 ---
    if not os.path.isdir(image_dir):
        print(f"错误：图像目录 '{image_dir}' 不存在或不是一个目录。")
        return
    if not os.path.isdir(annotation_dir):
        print(f"错误：标注目录 '{annotation_dir}' 不存在或不是一个目录。")
        return

    # --- 1. 获取所有图像文件的基本名称 (不含扩展名) ---
    image_basenames = set()
    print("\n正在扫描图像文件...")
    try:
        image_files = os.listdir(image_dir)
        for img_file in image_files:
            # 确保处理的是文件而不是子目录 (虽然通常JPEGImages里只有文件)
            if os.path.isfile(os.path.join(image_dir, img_file)):
                 basename = os.path.splitext(img_file)[0]
                 image_basenames.add(basename)
        print(f"找到 {len(image_basenames)} 个图像文件基本名称。")
        if not image_basenames:
             print("警告：在图像目录中没有找到任何文件。将不会删除任何标注文件。")
             return

    except Exception as e:
        print(f"错误：扫描图像目录时出错: {e}")
        return

    # --- 2. 遍历标注文件并决定是否删除 ---
    print("\n正在检查标注文件...")
    xml_files_to_delete = []
    xml_files_found = 0
    xml_files_kept = 0

    try:
        annotation_files = os.listdir(annotation_dir)
        for anno_file in annotation_files:
            # 只处理 .xml 文件
            if anno_file.lower().endswith('.xml'):
                xml_files_found += 1
                basename = os.path.splitext(anno_file)[0]
                full_anno_path = os.path.join(annotation_dir, anno_file)

                # 检查对应的图像基本名称是否存在
                if basename not in image_basenames:
                    xml_files_to_delete.append(full_anno_path)
                else:
                    xml_files_kept += 1

        print(f"找到 {xml_files_found} 个 XML 标注文件。")
        print(f"将保留 {xml_files_kept} 个文件 (有对应的图像)。")
        print(f"将删除 {len(xml_files_to_delete)} 个孤立文件 (无对应的图像)。")

    except Exception as e:
        print(f"错误：扫描标注目录时出错: {e}")
        return

    # --- 3. 执行删除 ---
    if not xml_files_to_delete:
        print("\n没有需要删除的孤立标注文件。")
        return

    # --- 安全确认 ---
    # 在实际删除前，可以取消下面这行注释来列出将要删除的文件
    # print("\n将要删除以下文件:")
    # for file_path in xml_files_to_delete:
    #     print(f" - {file_path}")

    confirm = input(f"\n确认要删除 {len(xml_files_to_delete)} 个XML文件吗？ (输入 'yes' 确认): ").strip().lower()

    if confirm == 'yes':
        print("\n正在删除文件...")
        deleted_count = 0
        error_count = 0
        for file_path in xml_files_to_delete:
            try:
                os.remove(file_path)
                print(f"已删除: {os.path.basename(file_path)}")
                deleted_count += 1
            except OSError as e:
                print(f"错误：无法删除文件 '{file_path}': {e}")
                error_count += 1
        print("\n--------------------")
        print("删除操作完成!")
        print(f"成功删除文件数: {deleted_count}")
        print(f"删除失败文件数: {error_count}")
        print("--------------------")
    else:
        print("\n操作已取消，没有文件被删除。")

# --- 配置您的路径 ---
# 使用原始字符串 (r"...") 或双反斜杠 (\\) 来处理 Windows 路径
IMAGE_DIR = r"E:\文件夹集合\毕设过程材料\Code_Data\TWHD\helmetdataset\JPEGImages"
ANNOTATION_DIR = r"E:\文件夹集合\毕设过程材料\Code_Data\TWHD\helmetdataset\Annotations"

# --- 运行清理脚本 ---
if __name__ == "__main__":
    clean_orphan_annotations(IMAGE_DIR, ANNOTATION_DIR)