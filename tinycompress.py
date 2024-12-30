import os
import re
import hashlib
import tinify

# 设置 Tinify API Keys
tinify_keys = [
    "tinify_keys1",
    "tinify_keys2",
    "tinify_keys3"
]
current_key_index = 0

# 初始化 Tinify API Key
tinify.key = tinify_keys[current_key_index]

# 提供需要压缩的文件夹路径
folder_to_compress = r"D:\project\x20pro_02_hood\oven"

# 设置最小图片大小（字节），小于此大小的图片将不压缩
min_image_size = 20 * 1024  # 20 KB

# 是否替换原图片
replace_original = True

# 白名单文件和文件夹，支持正则匹配
whitelist = [
    r".*example1\.png$",  # 匹配文件名为 example1.png
    r".*example2\.jpg$",  # 匹配文件名为 example2.jpg
    r"^icon_pot_anim_.*$",  # 匹配文件名以 icon_pot_anim_ 开头的文件
    r"^icon_roast_anim_.*$",  # 匹配文件名以 icon_roast_anim_ 开头的文件
    r"^icon_steam_anim_.*$",  # 匹配文件名以 icon_steam_anim_ 开头的文件
    r"^icon_super_charge_.*$",  # 匹配文件名以 icon_super_charge_ 开头的文件
    r".*folder_name.*"     # 匹配包含 folder_name 的文件夹
]

# 已压缩文件的 MD5 记录文件
md5_record_file = os.path.join(folder_to_compress, "compressed_files_md5.txt")
md5_tmp_file = os.path.join(folder_to_compress, "compressed_files_md5.txt.tmp")

def switch_tinify_key():
    """
    切换到下一个 Tinify API Key。
    """
    global current_key_index
    current_key_index += 1
    if current_key_index < len(tinify_keys):
        tinify.key = tinify_keys[current_key_index]
        print(f"已切换到新的 Tinify API Key: {tinify.key}")
    else:
        raise RuntimeError("所有 Tinify API Keys 已达到使用限制。")

def load_compressed_md5():
    """
    加载已压缩文件的 MD5 列表。

    返回：
        set: 已压缩文件的 MD5 集合。
    """
    if not os.path.exists(md5_record_file):
        return set()
    with open(md5_record_file, "r") as file:
        return set(line.strip() for line in file)

def calculate_md5(file_path):
    """
    计算文件的 MD5 哈希值。

    参数：
        file_path (str): 文件路径。

    返回：
        str: 文件的 MD5 哈希值。
    """
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compress_images_in_folder(folder_path):
    """
    递归遍历文件夹，对所有 PNG 和 JPG 图片进行压缩。

    参数：
        folder_path (str): 文件夹路径。
    """
    # 创建 compress 文件夹（如果不替换原图片）
    if not replace_original:
        compress_folder = os.path.join(folder_path, "compress")
        os.makedirs(compress_folder, exist_ok=True)

    # 加载已压缩文件的 MD5 列表
    compressed_md5 = load_compressed_md5()

    try:
        # 打开临时文件用于记录新压缩的 MD5
        with open(md5_tmp_file, "w") as tmp_file:
            # 遍历文件夹
            for root, dirs, files in os.walk(folder_path):
                # 检查文件夹是否匹配白名单
                if any(re.match(pattern, root) for pattern in whitelist):
                    print(f"跳过文件夹: {root}")
                    continue

                for file in files:
                    # 检查文件名是否匹配白名单
                    if any(re.match(pattern, file) for pattern in whitelist):
                        print(f"跳过白名单文件: {file}")
                        continue

                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file_path = os.path.join(root, file)
                        file_md5 = calculate_md5(file_path)

                        # 如果文件已经被压缩过，跳过
                        if file_md5 in compressed_md5:
                            print(f"文件已压缩过，跳过: {file_path}")
                            tmp_file.write(file_md5 + "\n")
                            continue

                        try:
                            # 压缩文件
                            compress_image(file_path, compress_folder if not replace_original else None)
                            # 保存已压缩的文件 MD5
                            tmp_file.write(file_md5 + "\n")
                        except tinify.AccountError:
                            print(f"API 使用限制已达到，切换到下一个 API Key。")
                            switch_tinify_key()
                            compress_image(file_path, compress_folder if not replace_original else None)
                            tmp_file.write(file_md5 + "\n")
                        except Exception as e:
                            print(f"跳过图片: {file_path}, 错误: {e}")

        # 任务完成后覆盖 MD5 记录文件
        os.replace(md5_tmp_file, md5_record_file)
        print("MD5 记录文件更新完成。")

    finally:
        # 清理临时文件
        if os.path.exists(md5_tmp_file):
            os.remove(md5_tmp_file)
            print(f"已删除临时文件: {md5_tmp_file}")

def compress_image(file_path, compress_folder):
    """
    使用 Tinify API 压缩单个图片，并打印压缩百分比。

    参数：
        file_path (str): 图片文件路径。
        compress_folder (str): 压缩后图片存放的文件夹路径（如果不替换原图片）。
    """
    # 获取原始文件大小
    original_size = os.path.getsize(file_path)

    # 跳过小于最小大小的图片
    if original_size < min_image_size:
        print(f"跳过压缩（文件太小）: {file_path}，大小: {original_size / 1024:.2f} kB")
        return

    print(f"正在压缩图片: {file_path}")
    source = tinify.from_file(file_path)

    if compress_folder:
        # 保存到 compress 文件夹
        new_file_path = os.path.join(compress_folder, os.path.basename(file_path))
        source.to_file(new_file_path)
    else:
        # 覆盖原文件
        source.to_file(file_path)

    # 获取压缩后的文件大小
    compressed_size = os.path.getsize(new_file_path if compress_folder else file_path)

    # 计算压缩百分比
    reduction = ((original_size - compressed_size) / original_size) * 100

    print(f"压缩完成: {file_path}，原始大小: {original_size / 1024:.2f} kB，压缩后大小: {compressed_size / 1024:.2f} kB，压缩百分比: {reduction:.2f}%")

if __name__ == "__main__":
    if os.path.isdir(folder_to_compress):
        compress_images_in_folder(folder_to_compress)
    else:
        print("提供的路径不是有效的文件夹。")
