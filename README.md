# 图片压缩工具使用说明

## 简介
本工具通过调用 **Tinify API** 实现 PNG、JPG、JPEG 格式图片的高效压缩，支持跳过特定文件及文件夹，自动管理已压缩文件记录，避免重复压缩。同时支持大批量压缩操作，具有高效的任务管理机制。

---

## 功能特点
1. **支持白名单规则**  
   - 可使用正则表达式跳过特定文件或文件夹。
2. **智能 MD5 管理**  
   - 通过 MD5 检测文件是否已压缩，避免重复压缩。
   - 每次任务运行后，自动更新 MD5 记录文件。
3. **自动切换 API Key**  
   - 支持多组 Tinify API Key，自动切换以避免达到使用限制。
4. **灵活配置**  
   - 可设置最小压缩文件大小、是否替换原图片、输出路径等。

---

## 使用方法

1. **配置 Tinify API Key**  
   在代码顶部 `tinify_keys` 列表中添加您的 API Key。

   ```python
   tinify_keys = [
       "your_api_key_1",
       "your_api_key_2",
       "your_api_key_3"
   ]
   ```

2. **配置文件路径**  
   设置需要压缩的文件夹路径：  
   ```python
   folder_to_compress = r"D:\your\folder\path"
   ```

3. **配置白名单**  
   白名单支持正则表达式，用于过滤特定文件或文件夹：  
   ```python
   whitelist = [
       r".*example1\.png$",       # 匹配文件名为 example1.png 的文件
       r"^icon_pot_anim_.*$",     # 匹配文件名以 icon_pot_anim_ 开头的文件
       r".*folder_name.*"         # 匹配包含 folder_name 的文件夹
   ]
   ```

4. **运行脚本**  
   确保 Python 环境中已安装 `tinify` 库，然后运行脚本：  
   ```bash
   python script_name.py
   ```

---

## 注意事项
1. **API Key 配额**  
   每个 API Key 每月最多支持压缩 500 张图片，建议准备多个 Key 以应对大批量任务。
   
2. **文件大小限制**  
   默认跳过小于 20 KB 的文件，可通过 `min_image_size` 参数调整。  
   ```python
   min_image_size = 20 * 1024  # 单位：字节
   ```

3. **MD5 记录文件**  
   - MD5 文件默认保存为 `compressed_files_md5.txt`。
   - 每次任务执行后自动更新，清理未匹配文件的 MD5 记录。

4. **覆盖原文件**  
   若设置 `replace_original = False`，压缩后的文件将保存在 `compress` 文件夹中。

---

## 依赖安装
确保已安装必要依赖：  
```bash
pip install tinify
```

---

## 文件结构示例
```
D:\your\folder\path
│
├── example1.png           # 白名单文件，不压缩
├── compressed_files_md5.txt  # 自动生成的 MD5 记录文件
├── image1.jpg             # 被压缩的文件
├── compress/              # 压缩后的图片文件夹（若不替换原图）
└── subfolder/
    └── icon_pot_anim_test.png  # 白名单规则匹配文件，不压缩
```

---

## 联系方式
如有问题，请联系开发者或提交问题反馈。