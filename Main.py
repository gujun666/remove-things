import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
import os

def get_md5(file_path):
    """计算文件的MD5值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def remove_duplicate_images(directory):
    """移除重复的图片文件"""
    md5_dict = {}
    duplicates = 0
    deleted_files = []
    
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(directory, filename)
            # 计算文件的MD5值
            file_md5 = get_md5(file_path)
            
            # 检查MD5值是否已存在
            if file_md5 in md5_dict:
                # 如果存在，删除文件
                print(f"删除重复文件: {filename}")
                os.remove(file_path)
                duplicates += 1
                deleted_files.append(filename)
            else:
                # 如果不存在，将MD5值添加到字典中
                md5_dict[file_md5] = filename

    return duplicates, deleted_files

def browse_folder():
    """浏览文件夹并选择"""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder_selected)

def start_process():
    """开始删除重复图片的进程"""
    directory_path = entry_path.get()
    if not directory_path:
        messagebox.showwarning("警告", "请选择一个文件夹")
        return
    duplicates_removed, deleted_files = remove_duplicate_images(directory_path)
    if duplicates_removed > 0:
        deleted_files_message = "\n".join(deleted_files)
        messagebox.showinfo("完成", f"删除了 {duplicates_removed} 个重复文件:\n{deleted_files_message}")
    else:
        messagebox.showinfo("完成", "没有找到重复的文件")

# 创建主窗口
root = tk.Tk()
root.title("删除重复图片")

# 创建路径输入框
entry_path = tk.Entry(root, width=50)
entry_path.pack(pady=10)

# 创建浏览文件夹按钮
button_browse = tk.Button(root, text="选择文件夹", command=browse_folder)
button_browse.pack()

# 创建开始按钮
button_start = tk.Button(root, text="删除重复图片", command=start_process)
button_start.pack(pady=10)

# 启动GUI的事件循环
root.mainloop()
