import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import random # 新增 random 模块
from ui_template import generate_comment_image

# --- 随机数据 --- (新增)
RANDOM_NICKNAMES = [
    "快乐小星", "购物达人", "生活家", "匿名用户", "阳光彩虹", "月下独酌", "追风少年",
    "学霸小张", "课程导师", "知识捕手", "终身学习者", "教育先锋", "智慧家长", "职场进修生",
    "慕课达人", "云课堂VIP", "笔记专家", "思维导图王", "错题终结者", "考研战士", "考证达人",
    "专升本学员", "公考先锋", "留学预备役", "编程新秀", "外语达人", "数学天才", "物理狂人",
    "化学实验员", "历史通", "地理探索者", "生物观察员", "政治评论员", "艺术特长生", "体育健将",
    "音乐爱好者", "美术创意家", "哲学思考者", "经济学人", "法学先锋", "医学预科生", "工程学徒",
    "AI探索者", "大数据分析", "网络安全员", "软件工程师", "网页设计师", "APP开发者", "游戏制作人",
    "无人机飞手", "机器人专家"
]

RANDOM_COMMENTS = [
    "课程内容非常实用，讲解清晰易懂！",
    "老师授课方式很好，知识点覆盖全面。",
    "资料整理得很系统，学习效率大大提高。",
    "课后习题设计合理，帮助巩固知识点。",
    "视频画质清晰，声音也很清楚。",
    "强烈推荐！这套课程资料真的很有价值！",
    "课程结构设计合理，循序渐进容易理解。",
    "配套资料很齐全，学习起来很方便。",
    "案例分析很到位，理论联系实际。",
    "课程更新及时，紧跟行业最新发展趋势。",
    "学习后收获很大，物超所值！",
    "客服回复及时，问题解决很快。",
    "课程难度适中，适合不同基础的学习者。",
    "PPT制作精美，重点突出。",
    "课程时长安排合理，学习节奏很好。"
]
AVATAR_DIR = "avatars" # 假设头像存放在 avatars 目录下 (新增)
DEFAULT_AVATAR = 'default_avatar.png'

# 确保头像目录存在 (新增)
if not os.path.exists(AVATAR_DIR):
    os.makedirs(AVATAR_DIR)
    print(f"创建头像目录: {AVATAR_DIR}, 请放入头像图片。")

# 获取可用头像列表 (新增)
available_avatars = []
if os.path.isdir(AVATAR_DIR):
    try:
        available_avatars = [os.path.join(AVATAR_DIR, f) for f in os.listdir(AVATAR_DIR) if os.path.isfile(os.path.join(AVATAR_DIR, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    except Exception as e:
        print(f"读取头像目录 {AVATAR_DIR} 出错: {e}")

if not available_avatars:
    print(f"警告：头像目录 {AVATAR_DIR} 中没有找到图片文件，将使用默认头像 {DEFAULT_AVATAR}。")


def select_files(entry_widget):
    """打开文件选择对话框并更新输入框，支持多选"""
    file_paths = filedialog.askopenfilenames(
        title="选择图片文件",
        filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"), ("所有文件", "*.*")]
    )
    if file_paths:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ";".join(file_paths))

def generate():
    """根据输入生成评论图片"""
    # 获取评论数量
    try:
        count = int(comment_count_entry.get())
        if count <= 0:
            messagebox.showerror("错误", "评论数量必须大于0")
            return
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")
        return
        
    # 生成指定数量的评论
    comments = []
    for _ in range(count):
        nickname = random.choice(RANDOM_NICKNAMES)
        content = random.choice(RANDOM_COMMENTS)
        avatar_path = random.choice(available_avatars) if available_avatars else DEFAULT_AVATAR
        
        # 获取用户输入的商品信息和评论图片
        image_path = image_entry.get()
        product_title = product_title_entry.get()
        product_price = product_price_entry.get()
    
        # 构建商品信息对象
        product_data = None
        if product_title and product_price and product_image_entry.get():
            product_data = {'title': product_title, 'price': product_price, 'image': product_image_entry.get()}
        elif product_title or product_price:
            messagebox.showwarning("警告", "商品标题和价格必须同时填写才能显示商品卡片。")
    
        # 构建完整评论数据结构
        comment_data = {
            'avatar': avatar_path,
            'nickname': nickname,
            'content': content,
            'images': image_path.split(';') if image_path else [],
            'product': product_data
        }
        comments.append(comment_data)

    # --- 保留用户输入的商品信息和评论图片 ---
    image_path = image_entry.get() # 评论图片路径保持用户输入
    product_title = product_title_entry.get()
    product_price = product_price_entry.get()

    # --- 不再需要检查昵称和内容是否为空 ---
    # if not nickname or not content:
    #     messagebox.showerror("错误", "昵称和评论内容不能为空！")
    #     return

    # --- 头像路径检查已在随机选择部分处理 ---
    # if avatar_path and not os.path.exists(avatar_path):
    #     messagebox.showerror("错误", f"头像文件不存在: {avatar_path}")
    #     return

    if image_path:
        image_paths = image_path.split(';')
        for img_path in image_paths:
            if not os.path.exists(img_path):
                messagebox.showerror("错误", f"评论图片文件不存在: {img_path}")
                return

    # 构建评论数据结构
    comment_data = {
        'avatar': avatar_path, # 使用随机或默认头像
        'nickname': nickname, # 使用随机昵称
        'content': content,   # 使用随机评论
        'images': image_path.split(';') if image_path else [],
        'product': None
    }

    if product_title and product_price and product_image_entry.get():
        comment_data['product'] = {'title': product_title, 'price': product_price}
    elif product_title or product_price: # 如果只填了商品信息的一部分
        messagebox.showwarning("警告", "商品标题和价格必须同时填写才能显示商品卡片。")

    # 将当前评论添加到comments列表
    comments.append(comment_data)

    output_filename = "gui_output.png"
    try:
        generate_comment_image(output_filename, comments) # 传入所有评论
        messagebox.showinfo("成功", f"已生成{count}条评论图片：{output_filename}")
    except Exception as e:
        messagebox.showerror("生成失败", f"生成图片时发生错误: {e}")

# --- GUI 设置 --- (修改：禁用或移除部分控件)
def select_file(entry_widget):
    """打开文件选择对话框并更新指定的输入框"""
    filepath = filedialog.askopenfilename(
        title="选择图片文件",
        filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"), ("所有文件", "*.*")]
    )
    if filepath:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filepath)

def select_product_image(): # 新增商品图片选择函数
    select_file(product_image_entry)

root = tk.Tk()
root.title("评论生成器")
root.geometry("500x450") # 调整窗口大小

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# --- 禁用或移除昵称、评论内容、头像输入 ---
# # 昵称
# nickname_label = ttk.Label(main_frame, text="昵称:")
# nickname_label.grid(row=0, column=0, sticky=tk.W, pady=5)
# nickname_entry = ttk.Entry(main_frame, width=40)
# nickname_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
# nickname_entry.config(state='disabled') # 或者直接注释掉上面四行

# # 评论内容
# content_label = ttk.Label(main_frame, text="评论内容:")
# content_label.grid(row=1, column=0, sticky=(tk.W, tk.N), pady=5)
# content_entry = tk.Text(main_frame, width=40, height=5) # 使用 Text 组件允许多行输入
# content_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
# content_entry.config(state='disabled') # 或者直接注释掉上面四行

# # 头像路径
# avatar_label = ttk.Label(main_frame, text="头像路径:")
# avatar_label.grid(row=2, column=0, sticky=tk.W, pady=5)
# avatar_entry = ttk.Entry(main_frame, width=30)
# avatar_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
# avatar_button = ttk.Button(main_frame, text="选择文件", command=lambda: select_file(avatar_entry))
# avatar_button.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
# avatar_entry.config(state='disabled') # 或者直接注释掉上面五行
# avatar_button.config(state='disabled')

# --- 保留评论图片、商品标题、商品价格输入 ---
current_row = 0 # 用于追踪网格行号

# 评论图片路径
image_label = ttk.Label(main_frame, text="评论图片路径 (可选):")
image_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
image_entry = ttk.Entry(main_frame, width=30)
image_entry.grid(row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
image_button = ttk.Button(main_frame, text="选择文件(可多选)", command=lambda: select_files(image_entry))
image_button.grid(row=current_row, column=2, sticky=tk.W, padx=5, pady=5)
current_row += 1

# 商品标题
product_title_label = ttk.Label(main_frame, text="商品标题 (可选):")
product_title_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
product_title_entry = ttk.Entry(main_frame, width=40)
product_title_entry.grid(row=current_row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
current_row += 1

# 商品价格
product_price_label = ttk.Label(main_frame, text="商品价格 (可选):")
product_price_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
product_price_entry = ttk.Entry(main_frame, width=40)
product_price_entry.grid(row=current_row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
current_row += 1

# 评论数量输入
comment_count_label = ttk.Label(main_frame, text="评论数量:")
comment_count_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
comment_count_entry = ttk.Entry(main_frame, width=40)
comment_count_entry.insert(0, "1") # 默认值
comment_count_entry.grid(row=current_row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
current_row += 1

# --- 新增：商品图片输入 --- #
product_image_label = ttk.Label(main_frame, text="商品图片路径:")
product_image_label.grid(row=current_row, column=0, sticky=tk.W, pady=5)
product_image_entry = ttk.Entry(main_frame, width=30)
product_image_entry.grid(row=current_row, column=1, sticky=(tk.W, tk.E), pady=5)
product_image_button = ttk.Button(main_frame, text="选择图片", command=lambda: select_file(product_image_entry))
product_image_button.grid(row=current_row, column=2, sticky=tk.W, padx=5, pady=5)
current_row += 1

# 生成按钮
generate_button = ttk.Button(main_frame, text="生成评论图片", command=generate)
generate_button.grid(row=current_row, column=0, columnspan=3, pady=20)

# 配置列的伸缩
main_frame.columnconfigure(1, weight=1)

# 运行主循环
root.mainloop()