from flask import Flask, request, jsonify, send_file
import os
import uuid
from ui_template import generate_comment_image
from PIL import Image
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    avatar = request.files['avatar']
    content = request.form['content']
    count = int(request.form.get('count', 1))
    product_title = request.form.get('product_title')
    product_price = request.form.get('product_price')
    random_mode = 'random_mode' in request.form

    # 创建输出目录
    os.makedirs('static/outputs', exist_ok=True)
    
    # 生成评论数据
    comments = []
    for _ in range(count):
        comment_data = {
            'avatar': f'static/temp_{avatar.filename}',
            'content': content,
            'nickname': '随机用户' if random_mode else '测试用户',
            'product': {
                'title': product_title or '测试商品',
                'price': product_price or '99.99'
            }
        }
        comments.append(comment_data)

    # 生成并保存图片
    output_buffer = io.BytesIO()
    generate_comment_image(output_buffer, comments)
    filename = f'static/outputs/{uuid.uuid4()}.png'
    with open(filename, 'wb') as f:
        f.write(output_buffer.getvalue())
    
    # 返回下载链接
    image_data = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
    return jsonify({'image': image_data, 'download_url': f'/download/{os.path.basename(filename)}'})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'static/outputs/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)