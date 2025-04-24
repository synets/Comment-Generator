document.getElementById('commentForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData();
  formData.append('avatar', document.getElementById('avatar').files[0]);
  formData.append('content', document.getElementById('content').value);
  formData.append('count', document.getElementById('count').value);
  formData.append('product_title', document.getElementById('productTitle').value);
  formData.append('product_price', document.getElementById('productPrice').value);
  formData.append('random_mode', document.getElementById('randomMode').checked ? 'on' : '');

  try {
    const response = await fetch('/generate', {
      method: 'POST',
      body: formData
    });
    
    if (response.ok) {
      const result = await response.json();
      document.getElementById('downloadLink').href = result.download_url;
      document.getElementById('downloadLink').style.display = 'block';
      document.getElementById('result').innerHTML = `<h3>生成完成，共生成${result.count}条评论</h3>`;
    } else {
      alert('生成失败：' + await response.text());
    }
  } catch (error) {
    alert('请求错误：' + error.message);
  }
});