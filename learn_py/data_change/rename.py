import os

# 定义图片和标注文件夹路径
image_folder = r"E:\TWHD\mydata\images"
label_folder = r"E:\TWHD\mydata\labels"

def rename_files_with_prefix(image_dir, label_dir, prefix="a"):
    """
    重命名图片和标注文件，使其名称从 prefix+1 开始递增并保持一致。

    Args:
        image_dir (str): 图片文件夹路径。
        label_dir (str): 标注文件夹路径。
        prefix (str): 新文件名前缀，默认为 'a'。
    """
    if not os.path.isdir(image_dir):
        print(f"错误：图片文件夹 '{image_dir}' 不存在。")
        return

    if not os.path.isdir(label_dir):
        print(f"错误：标注文件夹 '{label_dir}' 不存在。")
        return

    print(f"正在扫描图片文件夹: {image_dir}")
    print(f"正在扫描标注文件夹: {label_dir}")

    # 获取图片文件夹中的所有文件（忽略子文件夹）
    image_files = {}
    for filename in os.listdir(image_dir):
        file_path = os.path.join(image_dir, filename)
        if os.path.isfile(file_path):
            # 获取文件名（不含扩展名）和扩展名
            name, ext = os.path.splitext(filename)
            image_files[name] = (filename, ext) # 存储原始文件名和扩展名

    # 获取标注文件夹中的所有文件（忽略子文件夹）
    label_files = {}
    for filename in os.listdir(label_dir):
        file_path = os.path.join(label_dir, filename)
        if os.path.isfile(file_path):
            # 获取文件名（不含扩展名）和扩展名
            name, ext = os.path.splitext(filename)
            label_files[name] = (filename, ext) # 存储原始文件名和扩展名

    print(f"找到图片文件数量: {len(image_files)}")
    print(f"找到标注文件数量: {len(label_files)}")

    # 找到图片和标注文件都存在的主文件名（keys）
    common_names = sorted(list(set(image_files.keys()) & set(label_files.keys())))

    if not common_names:
        print("没有找到匹配的图片和标注文件对，无需重命名。")
        return

    print(f"找到 {len(common_names)} 对匹配的图片和标注文件。")
    print(f"开始以 '{prefix}1', '{prefix}2', ... 的规则重命名...")

    # 开始按顺序重命名
    counter = 1
    renamed_count = 0
    for name in common_names:
        original_image_filename, image_ext = image_files[name]
        original_label_filename, label_ext = label_files[name]

        # 构建原始文件完整路径
        original_image_path = os.path.join(image_dir, original_image_filename)
        original_label_path = os.path.join(label_dir, original_label_filename)

        # 构建新的文件名和完整路径
        # 核心修改：这里生成新的文件名，加上前缀 'a'
        new_name = f"{prefix}{counter}" # 或者使用 prefix + str(counter)
        new_image_filename = new_name + image_ext
        new_label_filename = new_name + label_ext
        new_image_path = os.path.join(image_dir, new_image_filename)
        new_label_path = os.path.join(label_dir, new_label_filename)

        # 检查新的文件名是否会覆盖现有文件 (可选，但推荐)
        # if os.path.exists(new_image_path) or os.path.exists(new_label_path):
        #     print(f"警告：新的文件名 '{new_name}' 已存在，跳过重命名 pair: {name}")
        #     counter += 1
        #     continue # 如果担心覆盖，可以取消注释这几行

        try:
            # 重命名图片文件
            os.rename(original_image_path, new_image_path)
            # 重命名标注文件
            os.rename(original_label_path, new_label_path)

            print(f"重命名 '{original_image_filename}' -> '{new_image_filename}'")
            print(f"重命名 '{original_label_filename}' -> '{new_label_filename}'")
            renamed_count += 1
            counter += 1

        except OSError as e:
            print(f"重命名文件 '{name}' 时发生错误: {e}")
            # 发生错误时，可以决定是否继续或停止
            # pass # 继续处理下一个文件
            # break # 停止所有操作

    print(f"\n重命名完成。成功重命名了 {renamed_count} 对文件。")
    if len(common_names) != renamed_count:
        print(f"注意：有 {len(common_names) - renamed_count} 对文件未能成功重命名。")

# 运行重命名函数，指定前缀为 'a'
rename_files_with_prefix(image_folder, label_folder, prefix="")