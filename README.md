# Image Compression Script README

## Overview
This script uses the Tinify API to compress images in a folder. It recursively traverses the folder and compresses all PNG, JPG, and JPEG files efficiently. Key features include:

1. Support for multiple Tinify API Keys with automatic switching when the free limit is reached.
2. Skipping already compressed files (tracked via MD5 hash).
3. Whitelist functionality to exclude specified files from compression.
4. Minimum file size threshold to avoid compressing very small files.
5. Option to replace original images or save compressed versions in a separate folder.

## Requirements
- Python 3.x
- `tinify` library

## Install Dependencies
```bash
pip install tinify
```

## Usage

1. Configure the following variables in the script:

   ```python
   # Set Tinify API Keys
   tinify_keys = [
       "YOUR_API_KEY_1",
       "YOUR_API_KEY_2"
   ]

   # Specify the folder containing images to compress
   folder_to_compress = "C:\\Users\\YourUsername\\Pictures"

   # Set minimum image size (in bytes); images smaller than this will not be compressed
   min_image_size = 10240  # 10 KB

   # Replace original images or save compressed images in a separate folder
   replace_original = False

   # Specify files to exclude from compression
   whitelist = ["example1.png", "example2.jpg"]
   ```

2. Run the script:

   ```bash
   python compress_images.py
   ```

3. Compressed images:
   - If `replace_original = False`, compressed images will be saved in the `compress` folder.
   - If `replace_original = True`, original images will be replaced by the compressed versions.

## Features

### API Key Switching
The script supports multiple Tinify API Keys. When the current key reaches its limit (500 compressions per month for free accounts), it automatically switches to the next key. If all keys are exhausted, the script will terminate with an error message.

### Skipping Already Compressed Files
The script creates a `compressed_files_md5.txt` file in the target folder to record the MD5 hashes of all compressed files. Files with matching MD5 hashes will be skipped.

### Whitelist
Files specified in the `whitelist` list will be excluded from compression.

### Minimum File Size Threshold
Images smaller than `min_image_size` (default: 10 KB) will not be compressed.

### Compression Details
The script outputs the original and compressed file sizes, as well as the compression percentage.

## Notes
1. Ensure all Tinify API Keys are valid.
2. For multiple API Keys, list them in the `tinify_keys` array in priority order.
3. Backup important files before setting `replace_original = True`.

## Sample Output
```plaintext
Compressing image: C:\\Users\\YourUsername\\Pictures\\example.png
Compression completed: C:\\Users\\YourUsername\\Pictures\\example.png, Original size: 204800 bytes, Compressed size: 102400 bytes, Compression rate: 50.00%
API limit reached, switching to the next API Key.
File already compressed, skipping: C:\\Users\\YourUsername\\Pictures\\compressed_image.jpg
```

## FAQ

### 1. How do I know if an API Key is exhausted?
When the current key reaches its limit, the script automatically switches to the next key and outputs:

```plaintext
API limit reached, switching to the next API Key.
```

### 2. Why are some images not compressed?
- The image size may be smaller than `min_image_size`.
- The image may be in the whitelist.
- The image may have already been compressed (MD5 recorded in `compressed_files_md5.txt`).

### 3. Why did the script stop?
If all Tinify API Keys are exhausted, the script will throw an error and stop:

```plaintext
RuntimeError: All Tinify API Keys have reached their usage limits.
```

## Contributing
Feel free to submit issues or pull requests for improvements!

## License
This script is open-sourced under the MIT License.

---

# 图片压缩脚本 README

## 概述
该脚本使用 Tinify API 对文件夹中的图片进行压缩，可递归遍历文件夹，对所有 PNG、JPG、JPEG 格式的图片进行高效压缩，并支持以下功能：

1. 支持多个 Tinify API Key，超过免费版限制后自动切换。
2. 支持跳过已压缩的文件（通过 MD5 记录）。
3. 支持白名单功能，白名单中的文件不会被压缩。
4. 支持最小文件大小限制，小于指定大小的图片不会被压缩。
5. 可选择是否替换原图片。

## 环境依赖
- Python 3.x
- `tinify` 库

## 安装依赖
```bash
pip install tinify
```

## 使用方法

1. 修改脚本中的配置项：

   ```python
   # 设置 Tinify API Keys
   tinify_keys = [
       "YOUR_API_KEY_1",
       "YOUR_API_KEY_2"
   ]

   # 提供需要压缩的文件夹路径
   folder_to_compress = "C:\\Users\\YourUsername\\Pictures"

   # 设置最小图片大小（字节），小于此大小的图片将不压缩
   min_image_size = 10240  # 10 KB

   # 是否替换原图片
   replace_original = False

   # 白名单文件
   whitelist = ["example1.png", "example2.jpg"]
   ```

2. 运行脚本：

   ```bash
   python compress_images.py
   ```

3. 压缩后的图片：
   - 如果 `replace_original = False`，压缩后的图片将存储在 `compress` 文件夹中。
   - 如果 `replace_original = True`，原图片将被替换为压缩后的图片。

## 功能说明

### API Key 自动切换
脚本支持多个 Tinify API Key。当当前 Key 达到使用限制（免费版 500 次压缩/月）时，会自动切换到下一个 Key。如果所有 Key 都达到限制，脚本将终止运行并提示错误。

### 已压缩文件跳过
脚本会在目标文件夹下生成一个 `compressed_files_md5.txt` 文件，记录所有已压缩文件的 MD5 值。在压缩前会校验文件的 MD5，如果文件已被压缩，则跳过。

### 白名单功能
通过 `whitelist` 列表可配置文件名，白名单中的文件将不会被压缩。

### 最小文件大小限制
小于 `min_image_size`（默认 10 KB）的文件将不会被压缩。

### 压缩效果
脚本会输出压缩前后的文件大小以及压缩百分比。

## 注意事项
1. 确保 Tinify API Key 正确有效。
2. 如果使用多个 API Key，请按优先级顺序填写到 `tinify_keys` 列表。
3. 请备份重要文件，尤其是在设置 `replace_original = True` 时。

## 示例输出
```plaintext
正在压缩图片: C:\\Users\\YourUsername\\Pictures\\example.png
压缩完成: C:\\Users\\YourUsername\\Pictures\\example.png，原始大小: 204800 字节，压缩后大小: 102400 字节，压缩百分比: 50.00%
API 使用限制已达到，切换到下一个 API Key。
文件已压缩过，跳过: C:\\Users\\YourUsername\\Pictures\\compressed_image.jpg
```

## 常见问题

### 1. 如何知道 API Key 是否已用尽？
当当前 Key 的使用次数达到上限时，脚本会自动切换到下一个 Key，并输出以下提示：

```plaintext
API 使用限制已达到，切换到下一个 API Key。
```

### 2. 为什么有些图片没有被压缩？
- 图片文件可能小于 `min_image_size`。
- 图片文件可能在白名单中。
- 图片文件可能已经被压缩过（MD5 记录在 `compressed_files_md5.txt` 中）。

### 3. 为什么脚本中止？
当所有 Tinify API Key 都用尽时，脚本会抛出错误并中止运行。

```plaintext
RuntimeError: 所有 Tinify API Keys 已达到使用限制。
```

## 贡献
如果有任何改进建议或发现问题，欢迎提交 Issue 或 Pull Request！

## 授权
本脚本基于 MIT License 开源。

