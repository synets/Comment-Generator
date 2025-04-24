import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def draw_multiline_text(draw, pos, text, font, fill, max_width, line_spacing=4):
    lines = textwrap.wrap(text, width=int(max_width / (font.size * 0.6))) # Approximate width calculation
    x, y = pos
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_spacing
    return y # Return the y position after the last line

import random

def generate_comment_image(output_path, comments, width=1440, height=2560): # 调整为更高分辨率
    # 创建白色背景
    img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # --- 字体设置 (尝试更精确的字体大小) ---
    try:
        # 尝试使用苹方-简 常规体 和 中黑体 (更符合 iOS 风格)
        font_path_regular = "/System/Library/Fonts/PingFang.ttc"
        font_path_medium = "/System/Library/Fonts/PingFang.ttc" # Pillow might pick Medium weight
        font_status = ImageFont.truetype(font_path_regular, 24) # 状态栏字体
        font_title = ImageFont.truetype(font_path_medium, 30) # 页面标题字体
        font_nickname = ImageFont.truetype(font_path_medium, 24) # 昵称字体
        font_content = ImageFont.truetype(font_path_regular, 24) # 评论内容字体
        font_product_title = ImageFont.truetype(font_path_regular, 22) # 商品标题字体
        font_product_price = ImageFont.truetype(font_path_regular, 22) # 商品价格字体
        font_button = ImageFont.truetype(font_path_regular, 20) # 按钮字体
        font_pdd = ImageFont.truetype(font_path_medium, 16) # 拼多多 Logo 字体
        font_icon = ImageFont.truetype(font_path_regular, 24) # 图标字体 (用于 Unicode 符号)
    except IOError:
        print("警告：苹方字体未找到，将使用默认字体。样式可能不准确。")
        # Fallback to default font if PingFang is not available
        font_status = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_nickname = ImageFont.load_default()
        font_content = ImageFont.load_default()
        font_product_title = ImageFont.load_default()
        font_product_price = ImageFont.load_default()
        font_button = ImageFont.load_default()
        font_pdd = ImageFont.load_default()
        font_icon = ImageFont.load_default()

    # --- 顶部状态栏 (更接近 iOS 风格) ---
    status_bar_height = 44 # iOS 状态栏大致高度
    header_height = 44    # 导航栏高度
    top_offset = status_bar_height + header_height

    draw.rectangle([0, 0, width, status_bar_height], fill=(255, 255, 255)) # 白色背景
    # 时间
    time_text = "23:45"
    time_bbox = draw.textbbox((0, 0), time_text, font=font_status)
    time_width = time_bbox[2] - time_bbox[0]
    draw.text((20, (status_bar_height - (time_bbox[3] - time_bbox[1])) // 2), time_text, fill=(0, 0, 0), font=font_status)

    # 右侧图标 (使用 Unicode 占位符)
    signal_icon = "📶"
    wifi_icon = ""
    battery_icon = "🔋"
    icons_text = f"{signal_icon}  {wifi_icon}  {battery_icon} 90%"
    icons_bbox = draw.textbbox((0, 0), icons_text, font=font_status)
    icons_width = icons_bbox[2] - icons_bbox[0]
    draw.text((width - icons_width - 15, (status_bar_height - (icons_bbox[3] - icons_bbox[1])) // 2), icons_text, fill=(0, 0, 0), font=font_status)

    # --- 标题栏 --- (添加返回和分享图标)
    draw.rectangle([0, status_bar_height, width, top_offset], fill=(255, 255, 255)) # 白色背景
    # 返回按钮 (Unicode 占位符)
    back_icon = "<"
    back_bbox = draw.textbbox((0, 0), back_icon, font=font_icon)
    draw.text((15, status_bar_height + (header_height - (back_bbox[3] - back_bbox[1])) // 2), back_icon, fill=(0, 0, 0), font=font_icon)

    # 标题文字
    title_text = "店铺评价"
    title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width) // 2, status_bar_height + (header_height - (title_bbox[3] - title_bbox[1])) // 2), title_text, fill=(0, 0, 0), font=font_title)

    # 分享按钮 (Unicode 占位符)
    share_icon = "🔗"
    share_bbox = draw.textbbox((0, 0), share_icon, font=font_icon)
    draw.text((width - (share_bbox[2] - share_bbox[0]) - 15, status_bar_height + (header_height - (share_bbox[3] - share_bbox[1])) // 2), share_icon, fill=(0, 0, 0), font=font_icon)

    # --- 评论区 --- #
    y = top_offset + 15 # 评论区起始 Y 坐标，增加一些边距
    left_margin = 15
    content_left_margin = left_margin + 48 + 10 # 头像宽度 + 间距
    content_width = width - content_left_margin - left_margin # 内容区域宽度

    for c_idx, c in enumerate(comments):
        start_y = y
        # 头像
        avatar_size = 60 # 增大头像尺寸以提高清晰度
        if os.path.exists(c['avatar']):
            try:
                avatar = Image.open(c['avatar']).convert("RGBA").resize((avatar_size, avatar_size))
                # 创建圆形遮罩
                mask = Image.new('L', (avatar_size, avatar_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
                img.paste(avatar, (left_margin, y), mask)
            except Exception as e:
                print(f"加载头像失败: {c['avatar']}, 错误: {e}")
                # 画一个灰色圆形占位符
                draw.ellipse([left_margin, y, left_margin + avatar_size, y + avatar_size], fill=(200, 200, 200))
                # 添加错误提示文本
                error_font = ImageFont.load_default()
                draw.text((left_margin, y + avatar_size + 5), "头像加载失败", fill=(255, 0, 0), font=error_font)
        else:
             # 画一个灰色圆形占位符
             draw.ellipse([left_margin, y, left_margin + avatar_size, y + avatar_size], fill=(200, 200, 200))
             # 添加缺失提示文本
             error_font = ImageFont.load_default()
             draw.text((left_margin, y + avatar_size + 5), "头像文件缺失", fill=(255, 0, 0), font=error_font)

        # 昵称
        avatar_y = y # Store avatar y for alignment
        nickname_y = avatar_y + 2 # 垂直居中对齐头像
        draw.text((content_left_margin, nickname_y), c['nickname'], fill=(80, 80, 80), font=font_nickname) # 调整颜色
        nickname_bbox = draw.textbbox((0,0), c['nickname'], font=font_nickname)
        current_y = nickname_y + (nickname_bbox[3] - nickname_bbox[1]) + 10 # 昵称下方 Y 坐标 + 间距

        # 评论内容 (使用换行函数)
        content_y = current_y
        last_line_y = draw_multiline_text(draw, (content_left_margin, content_y), c['content'], font_content, fill=(30, 30, 30), max_width=content_width, line_spacing=6) # 增加行间距
        current_y = last_line_y + 12 # 内容下方 Y 坐标 + 间距

        # 评论图片 (多图横排，简单实现)
        image_y = current_y
        image_padding = 5
        images_in_row = 3
        max_img_size = (content_width - (images_in_row - 1) * image_padding) // images_in_row
        img_size = min(max_img_size, 150) # 增大图片尺寸以提高清晰度

        comment_images = c.get('images', []) # 支持多图，假设传入的是 'images' 列表
        if isinstance(c.get('image'), str) and os.path.exists(c['image']): # 兼容旧的单图 'image'
            if c['image'] not in comment_images: # Avoid duplicates if 'image' is also in 'images'
                 comment_images.insert(0, c['image'])

        if comment_images:
            img_x = content_left_margin
            img_row_y = image_y
            for i, img_path in enumerate(comment_images):
                if i > 0 and i % images_in_row == 0:
                    img_row_y += img_size + image_padding
                    img_x = content_left_margin

                if os.path.exists(img_path):
                    try:
                        comment_img_orig = Image.open(img_path).convert("RGBA")
                        # 等比缩放，使其短边等于 img_size
                        w, h = comment_img_orig.size
                        if w < h:
                            new_w = img_size
                            new_h = int(h * (img_size / w))
                        else:
                            new_h = img_size
                            new_w = int(w * (img_size / h))
                        comment_img_resized = comment_img_orig.resize((new_w, new_h))
                        # 居中裁剪到正方形
                        left = (new_w - img_size) / 2
                        top = (new_h - img_size) / 2
                        right = (new_w + img_size) / 2
                        bottom = (new_h + img_size) / 2
                        comment_img = comment_img_resized.crop((left, top, right, bottom))

                        # 添加圆角
                        radius = 6
                        mask = Image.new('L', (img_size, img_size), 0)
                        mask_draw = ImageDraw.Draw(mask)
                        mask_draw.rounded_rectangle((0, 0, img_size, img_size), radius, fill=255)
                        img.paste(comment_img, (int(img_x), int(img_row_y)), mask)
                    except Exception as e:
                        print(f"加载评论图片失败: {img_path}, 错误: {e}")
                        # 画灰色方块占位
                        draw.rectangle([int(img_x), int(img_row_y), int(img_x + img_size), int(img_row_y + img_size)], fill=(220, 220, 220))
                        # 添加错误提示文本
                        error_font = ImageFont.load_default()
                        draw.text((int(img_x), int(img_row_y) + img_size + 5), "图片加载失败", fill=(255, 0, 0), font=error_font)
                else:
                    # 画灰色方块占位
                    draw.rectangle([int(img_x), int(img_row_y), int(img_x + img_size), int(img_row_y + img_size)], fill=(220, 220, 220))
                    # 添加缺失提示文本
                    error_font = ImageFont.load_default()
                    draw.text((int(img_x), int(img_row_y) + img_size + 5), "图片文件缺失", fill=(255, 0, 0), font=error_font)

                img_x += img_size + image_padding

            # 更新 current_y 到最后一排图片下方
            num_rows = (len(comment_images) + images_in_row - 1) // images_in_row
            current_y = img_row_y + img_size + 15 # 图片下方 Y 坐标 + 间距
        else:
             current_y = image_y # 没有图片则 Y 坐标不变

        # 商品卡片 (添加图片, '已抢', '去拼单'按钮)
        product_y = current_y
        if c.get('product') and isinstance(c['product'].get('image'), str) and os.path.exists(c['product']['image']):
            card_padding = 10
            card_bg_color = (248, 248, 248)
            product_img_size = 60 # 商品图片尺寸
            card_height = product_img_size + card_padding * 2 # 卡片高度由图片和边距决定
            button_width = 70
            button_height = 25
            button_radius = 12
            button_color = (255, 80, 0)
            button_text_color = (255, 255, 255)

            # Use rounded_rectangle for the card background
            draw.rounded_rectangle([content_left_margin, product_y, width - left_margin, product_y + card_height], radius=5, fill=card_bg_color)

            # 商品图片
            product_img_x = content_left_margin + card_padding
            product_img_y = product_y + card_padding
            product_image_path = c['product'].get('image') # 获取商品图片路径
            if product_image_path and isinstance(product_image_path, str) and os.path.exists(product_image_path): # 严格验证路径类型和存在性
                 try:
                    prod_img_orig = Image.open(product_image_path).convert("RGBA")
                    prod_img_orig.thumbnail((product_img_size, product_img_size))
                    # Resize and crop to square
                    w, h = prod_img_orig.size
                    if w != h:
                        crop_size = min(w, h)
                        left = (w - crop_size) / 2
                        top = (h - crop_size) / 2
                        right = (w + crop_size) / 2
                        bottom = (h + crop_size) / 2
                        prod_img_orig = prod_img_orig.crop((left, top, right, bottom))
                    prod_img = prod_img_orig.resize((product_img_size, product_img_size))

                    # 圆角
                    prod_mask = Image.new('L', (product_img_size, product_img_size), 0)
                    prod_mask_draw = ImageDraw.Draw(prod_mask)
                    prod_mask_draw.rounded_rectangle((0, 0, product_img_size, product_img_size), 5, fill=255)
                    img.paste(prod_img, (product_img_x, product_img_y), prod_mask)
                 except Exception as e:
                    print(f"加载商品图片失败: {product_image_path}, 错误: {e}")
                    draw.rectangle([product_img_x, product_img_y, product_img_x + product_img_size, product_img_y + product_img_size], fill=(220, 220, 220))
            else:
                draw.rectangle([product_img_x, product_img_y, product_img_x + product_img_size, product_img_y + product_img_size], fill=(220, 220, 220))

            # 商品文本区域起始 X
            product_text_x = product_img_x + product_img_size + 10
            product_text_max_width = width - left_margin - product_text_x - button_width - card_padding * 2 # 减去按钮宽度和边距

            # 商品标题 (限制一行，加省略号)
            title_text_y = product_img_y + 2
            product_title = c['product']['title']
            title_bbox = draw.textbbox((0,0), product_title, font=font_product_title)
            if title_bbox[2] > product_text_max_width:
                # 估算能放多少字
                approx_char_width = font_product_title.size * 0.6 # Estimate character width
                max_chars = int(product_text_max_width / approx_char_width)
                if max_chars > 2: # Ensure space for ellipsis
                     product_title = product_title[:max_chars-1] + '…'
                else:
                     product_title = product_title[:1] + '…' # Handle very narrow space
            draw.text((product_text_x, title_text_y), product_title, fill=(80, 80, 80), font=font_product_title)

            # 已抢信息
            sold_text_y = title_text_y + font_product_title.size + 8
            sold_count = random.randint(1000, 9999) # 假设有 sold_count 字段
            sold_text = f"已抢{sold_count}件"
            draw.text((product_text_x, sold_text_y), sold_text, fill=(150, 150, 150), font=font_product_title) # 灰色小字

            # 价格
            price_text_y = product_img_y + card_height - card_padding - font_product_price.size - 2 # 底部对齐
            price_text = f"￥{c['product']['price']}"
            draw.text((product_text_x, price_text_y), price_text, fill=(255, 80, 0), font=font_product_price)

            # 去拼单按钮
            button_x = width - left_margin - button_width - card_padding
            button_y = product_y + (card_height - button_height) // 2
            draw.rounded_rectangle([button_x, button_y, button_x + button_width, button_y + button_height], radius=button_radius, fill=button_color)
            button_text = "去拼单"
            button_text_bbox = draw.textbbox((0,0), button_text, font=font_button)
            button_text_width = button_text_bbox[2] - button_text_bbox[0]
            button_text_height = button_text_bbox[3] - button_text_bbox[1]
            # Adjust text position slightly for better vertical centering
            draw.text((button_x + (button_width - button_text_width) // 2, button_y + (button_height - button_text_height) // 2 - 1), button_text, fill=button_text_color, font=font_button)

            current_y = product_y + card_height + 15 # 卡片下方 Y 坐标 + 间距
        else:
            current_y = product_y # 没有商品卡片则 Y 坐标不变

        # 点赞和评论图标 (使用 Unicode 占位符)
        actions_y = current_y
        like_icon = "👍"
        comment_icon = "💬"
        like_count = c.get('likes', 0) # 假设有点赞数字段
        comments_count_val = c.get('comments_count', 0) # 假设有评论数字段

        icon_font_size = 14
        try:
            font_actions = ImageFont.truetype(font_path_regular, icon_font_size)
        except:
            font_actions = ImageFont.load_default()

        # 评论图标和数量 (Handle '评论' text case)
        if isinstance(comments_count_val, str):
            comment_text = f"{comment_icon} {comments_count_val}"
        else:
            comment_text = f"{comment_icon} {comments_count_val if comments_count_val > 0 else '评论'}"

        comment_bbox = draw.textbbox((0,0), comment_text, font=font_actions)
        comment_width = comment_bbox[2] - comment_bbox[0]
        comment_x = width - left_margin - comment_width
        draw.text((comment_x, actions_y), comment_text, fill=(150, 150, 150), font=font_actions)

        # 点赞图标和数量 (Only show count if > 0)
        like_text = f"{like_icon}{' ' + str(like_count) if like_count > 0 else ''}"
        like_bbox = draw.textbbox((0,0), like_text, font=font_actions)
        like_width = like_bbox[2] - like_bbox[0]
        like_x = comment_x - like_width - 15 # 图标间距
        draw.text((like_x, actions_y), like_text, fill=(150, 150, 150), font=font_actions)

        current_y = actions_y + (like_bbox[3] - like_bbox[1]) + 20 # 图标下方 Y 坐标 + 间距

        # 计算评论块的总高度并更新下一个评论的起始 Y
        # comment_height = current_y - start_y # This calculation is complex now
        y = current_y # Directly use current_y for the next block's start

        # 绘制分隔线 (可选，且在最后一条评论后不画)
        # Need c_idx, so enumerate the comments loop
        # Add 'c_idx' to the loop: for c_idx, c in enumerate(comments):
        if 'c_idx' in locals() and c_idx < len(comments) - 1:
             draw.line([(left_margin, y - 10), (width - left_margin, y - 10)], fill=(230, 230, 230), width=1)
        else:
             y -= 10 # 移除最后分隔线的空间

    # --- 调整最终图像高度 --- #
    # 如果内容超出预设高度，则裁剪或创建更高图片 (这里选择裁剪)
    final_height = min(y + 20, height) # 加一点底部边距
    img = img.crop((0, 0, width, final_height))

    img.save(output_path)

def demo():
    comments = [
        {
            'avatar': 'avatar1.png',
            'nickname': '东春',
            'content': '收到外壳老化生认可以。',
            'image': 'product1.png',
            'product': {'title': '库存电子选台调频收音机低价处理', 'price': '10.5'}
        },
        {
            'avatar': 'avatar2.png',
            'nickname': '三信电子 SansonEL...',
            'content': '商品完全符合描述，小二服务热情耐心，使用体验超棒，外观设计新颖独特，品质量过硬，物流服务迅速，性价比极高，非常满意！',
            'image': 'product2.png',
            'product': {'title': '库存全新汽车应急启动电源低价处理', 'price': '64'}
        },
        {
            'avatar': 'avatar3.png',
            'nickname': '滨州🚀💎liuyanling...',
            'content': '货物已收到了！挺好的，声音也不错，插上耳机就可以听了😊😊',
            'image': 'product3.png',
            'product': None
        }
    ]
    generate_comment_image('demo_output.png', comments)

if __name__ == "__main__":
    # 更新 demo 数据以包含新字段，更接近截图
    comments_demo = [
        {
            'avatar': 'avatar1.png', # Replace with actual path or ensure exists
            'nickname': '东春',
            'content': '收到外壳老化生认可以。',
            'images': [], # No image in first comment of example
            'product': {
                'title': '库存电子选台调频收音机低价处理',
                'price': '10.5',
                'image': 'product1.png', # Replace/ensure exists
                'sold_count': 11
            },
            'likes': 0,
            'comments_count': 0
        },
        {
            'avatar': 'avatar2.png', # Replace/ensure exists
            'nickname': '三信电子 SansonEL...',
            'content': '商品完全符合描述，小二服务热情耐心，使用体验超棒，外观设计新颖独特，品质量过硬，物流服务迅速，性价比极高，非常满意！',
            # Use actual image paths from example if available
            'images': ['product2_1.png', 'product2_2.png', 'product2_3.png'],
            'product': {
                'title': '库存全新汽车应急启动电源低价处理',
                'price': '64',
                'image': 'product2_thumb.png', # Replace/ensure exists
                'sold_count': 223
            },
            'likes': 15,
            'comments_count': '评论' # Match example text
        },
        {
            'avatar': 'avatar3.png', # Replace/ensure exists
            'nickname': '滨州🚀💎liuyanling...',
            'content': '货物已收到了！挺好的，声音也不错，插上耳机就可以听了😊😊',
            'images': ['product3.png'], # Replace/ensure exists
            'product': None,
            'likes': 0,
            'comments_count': 0
        }
    ]
    # Optional: Add placeholder logic if needed
    # import shutil
    # placeholder_avatar = 'placeholder_avatar.png'
    # placeholder_product = 'placeholder_product.png'
    # if not os.path.exists(placeholder_avatar): Image.new('RGB', (40, 40), (200, 200, 200)).save(placeholder_avatar)
    # if not os.path.exists(placeholder_product): Image.new('RGB', (60, 60), (220, 220, 220)).save(placeholder_product)
    #
    # for c in comments_demo:
    #     if not os.path.exists(c['avatar']): c['avatar'] = placeholder_avatar
    #     valid_images = []
    #     for img_path in c.get('images', []):
    #         if os.path.exists(img_path):
    #             valid_images.append(img_path)
    #         # else: you might want to add a placeholder image path here too
    #     c['images'] = valid_images
    #     if c.get('product') and not os.path.exists(c['product'].get('image','')):
    #         c['product']['image'] = placeholder_product

    output_file = 'demo_output_final.png'
    generate_comment_image(output_file, comments_demo)
    print(f"生成 {output_file}")