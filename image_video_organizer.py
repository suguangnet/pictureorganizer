import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from pathlib import Path
import threading

class ImageVideoOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("图片和视频收纳器")
        self.root.geometry("600x520")
        self.root.resizable(True, True)
        
        # 窗体居中
        self.center_window()
        
        # 支持的文件格式
        self.image_extensions = {'.psb', '.psd', '.tif', '.jpg', '.jpeg', '.heic', '.png', '.bmp', '.webp', '.gif'}
        self.video_extensions = {'.mp4', '.mov', '.wmv', '.3gp', '.avi', '.flv'}
        
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="准备就绪")
        
        self.create_widgets()
        
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 输入目录选择
        ttk.Label(main_frame, text="输入目录:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(main_frame, text="浏览", command=self.select_input_directory).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录选择
        ttk.Label(main_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(main_frame, text="浏览", command=self.select_output_directory).grid(row=1, column=2, padx=5, pady=5)
        
        # 选项框架
        options_frame = ttk.LabelFrame(main_frame, text="选项", padding="5")
        options_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        
        self.include_subdirs = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="包含子目录", variable=self.include_subdirs).grid(row=0, column=0, sticky=tk.W)
        
        self.copy_mode = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="复制文件（取消则为移动文件）", variable=self.copy_mode).grid(row=1, column=0, sticky=tk.W)
        
        # 支持格式显示
        formats_frame = ttk.LabelFrame(main_frame, text="支持的文件格式", padding="5")
        formats_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        
        # 显示支持的格式（按指定顺序）
        image_formats = ".psb .psd .tif .jpg .jpeg .heic .png .bmp .webp .gif"
        video_formats = ".mp4 .mov .wmv .3gp .avi .flv"
        
        ttk.Label(formats_frame, text=f"图片格式: {image_formats}").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(formats_frame, text=f"视频格式: {video_formats}").grid(row=1, column=0, sticky=tk.W)
        
        # 开始按钮
        self.start_button = ttk.Button(main_frame, text="开始整理", command=self.start_organizing)
        self.start_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # 进度条
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=5)
        
        # 状态标签
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=6, column=0, columnspan=3, pady=5)
        
        # 日志文本框
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=10)
        main_frame.rowconfigure(7, weight=1)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 版权信息
        copyright_label = ttk.Label(main_frame, text="© 2025 速光网络软件开发  抖音号关注：dubaishun12", 
                                   font=('Arial', 8), foreground='gray')
        copyright_label.grid(row=8, column=0, columnspan=3, pady=(5, 0))
        
    def center_window(self):
        """窗体居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def select_input_directory(self):
        directory = filedialog.askdirectory(title="选择输入目录")
        if directory:
            self.input_path.set(directory)
            
    def select_output_directory(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_path.set(directory)
            
    def log_message(self, message):
        """在日志区域添加消息"""
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def is_media_file(self, filepath):
        """检查文件是否为图片或视频文件"""
        ext = Path(filepath).suffix.lower()
        return ext in self.image_extensions or ext in self.video_extensions
        
    def get_file_date_folder(self, filepath):
        """根据文件修改时间获取年月文件夹名称"""
        try:
            # 获取文件修改时间
            mtime = os.path.getmtime(filepath)
            date_obj = datetime.fromtimestamp(mtime)
            return f"{date_obj.year}-{date_obj.month:02d}"
        except Exception as e:
            self.log_message(f"无法获取文件 {filepath} 的修改时间: {str(e)}")
            return "未知日期"
            
    def scan_files(self, input_dir):
        """扫描目录中的媒体文件"""
        media_files = []
        
        if self.include_subdirs.get():
            # 递归搜索所有子目录
            for root, dirs, files in os.walk(input_dir):
                for file in files:
                    filepath = os.path.join(root, file)
                    if self.is_media_file(filepath):
                        media_files.append(filepath)
        else:
            # 只搜索当前目录
            try:
                for file in os.listdir(input_dir):
                    filepath = os.path.join(input_dir, file)
                    if os.path.isfile(filepath) and self.is_media_file(filepath):
                        media_files.append(filepath)
            except PermissionError:
                self.log_message(f"无法访问目录: {input_dir}")
                
        return media_files
        
    def organize_file(self, source_path, output_dir):
        """整理单个文件"""
        try:
            # 获取目标文件夹名称
            date_folder = self.get_file_date_folder(source_path)
            
            # 创建目标目录
            target_dir = os.path.join(output_dir, date_folder)
            os.makedirs(target_dir, exist_ok=True)
            
            # 获取文件名
            filename = os.path.basename(source_path)
            target_path = os.path.join(target_dir, filename)
            
            # 处理文件名冲突
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(target_path):
                new_filename = f"{base_name}_{counter}{ext}"
                target_path = os.path.join(target_dir, new_filename)
                counter += 1
            
            # 复制或移动文件
            if self.copy_mode.get():
                shutil.copy2(source_path, target_path)
                operation = "复制"
            else:
                shutil.move(source_path, target_path)
                operation = "移动"
                
            self.log_message(f"{operation}: {filename} -> {date_folder}/")
            return True
            
        except Exception as e:
            self.log_message(f"处理文件 {source_path} 时出错: {str(e)}")
            return False
            
    def organize_files_thread(self):
        """在后台线程中组织文件"""
        try:
            input_dir = self.input_path.get()
            output_dir = self.output_path.get()
            
            if not input_dir or not output_dir:
                messagebox.showerror("错误", "请选择输入和输出目录")
                return
                
            if not os.path.exists(input_dir):
                messagebox.showerror("错误", "输入目录不存在")
                return
                
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            self.log_message("开始扫描文件...")
            self.status_var.set("正在扫描文件...")
            
            # 扫描文件
            media_files = self.scan_files(input_dir)
            
            if not media_files:
                self.log_message("未找到任何图片或视频文件")
                self.status_var.set("未找到文件")
                return
                
            self.log_message(f"找到 {len(media_files)} 个媒体文件")
            self.status_var.set(f"正在处理 {len(media_files)} 个文件...")
            
            # 处理文件
            success_count = 0
            total_files = len(media_files)
            
            for i, filepath in enumerate(media_files):
                if self.organize_file(filepath, output_dir):
                    success_count += 1
                    
                # 更新进度
                progress = (i + 1) / total_files * 100
                self.progress_var.set(progress)
                self.root.update_idletasks()
                
            self.log_message(f"整理完成！成功处理 {success_count}/{total_files} 个文件")
            self.status_var.set(f"完成：{success_count}/{total_files} 个文件")
            messagebox.showinfo("完成", f"文件整理完成！\n成功处理 {success_count}/{total_files} 个文件")
            
        except Exception as e:
            error_msg = f"整理过程中出现错误: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("错误", error_msg)
        finally:
            self.start_button.config(state='normal')
            self.progress_var.set(0)
            
    def start_organizing(self):
        """开始整理文件"""
        # 清空日志
        self.log_text.delete(1.0, tk.END)
        
        # 禁用开始按钮
        self.start_button.config(state='disabled')
        
        # 在后台线程中运行整理过程
        thread = threading.Thread(target=self.organize_files_thread)
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = ImageVideoOrganizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()