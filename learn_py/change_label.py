import os

# 替换为你新采集的数据标注文件夹路径（163份）
label_dir = r"E:\TWHD\dataset\labels"

# 类别映射字典（原类别 -> 新类别）
class_mapping = {
    0: 1,  # helmet -> helmetr
    1: 0,  # motor -> two_wheeler
    2: 2   # head -> without_helmet
}

changed_count = 0
for label_file in os.listdir(label_dir):
    label_path = os.path.join(label_dir, label_file)
    if not label_file.endswith(".txt"):
        continue

    with open(label_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 5:
            continue  # 忽略格式错误的行
        old_class = int(parts[0])
        if old_class in class_mapping:
            parts[0] = str(class_mapping[old_class])
        new_lines.append(" ".join(parts))

    # 覆盖写入新标签
    with open(label_path, 'w') as f:
        f.write("\n".join(new_lines) + "\n")
        changed_count += 1

print(f"已处理并转换类别的标注文件数量：{changed_count}")
