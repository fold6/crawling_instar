import os
import re
import json
from datetime import datetime

# 처리할 폴더들과 라벨
folders = [
    ("aespa_karina", "📸 에스파 공식계정"),
    ("karina_personal", "🌟 카리나 개인계정")
]

date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

# 이미지 메타데이터 수집 (os.scandir 사용으로 최적화)
def collect_images(folders):
    images = []
    for folder, label in folders:
        try:
            for entry in os.scandir(folder):
                if not entry.is_file() or not entry.name.lower().endswith('.jpg'):
                    continue
                m = date_pattern.search(entry.name)
                if not m:
                    continue
                date_str = "-".join(m.groups())
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue
                images.append({
                    "src": f"{folder}/{entry.name}",
                    "date": date_str,
                    "date_obj": date_obj,
                    "source": label,
                    "hover": f"{label} | {date_str}"
                })
        except FileNotFoundError:
            continue
    # datetime 객체로 안전하게 정렬
    images.sort(key=lambda x: x['date_obj'], reverse=True)
    return images

# HTML 생성 (datetime 필드 제거 후 JSON 직렬화)
def generate_html(images, initial_count=20, batch_size=20):
    serializable = [
        {k: v for k, v in img.items() if k != 'date_obj'}
        for img in images
    ]
    data_json = json.dumps(serializable, ensure_ascii=False)
    with open("karina_gallery.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang=\"ko\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Karina INSTAR PIC</title>
  <style>
    body {{ font-family: sans-serif; padding: 20px; background: #f0f0f0; margin:0; }}
    .gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; }}
    .item img {{ width: 100%; border-radius: 12px; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.3s; }}
    .item img:hover {{ transform: scale(1.05); }}
    .caption {{ text-align: center; margin-top: 6px; font-size: 0.9rem; color: #555; }}
    .lightbox {{ display: none; position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); justify-content:center; align-items:center; z-index:999; }}
    .lightbox img {{ max-width: 90%; max-height:80%; border-radius:10px; }}
    #loader {{ display:none; text-align:center; padding:20px 0; }}
    #loader .spinner {{ border:6px solid #f3f3f3; border-top:6px solid #555; border-radius:50%; width:50px; height:50px; animation:spin 1s linear infinite; margin:auto; }}
    @keyframes spin {{ to {{ transform:rotate(360deg); }} }}
  </style>
</head>
<body>
  <h2 style=\"text-align:center;\">Karina INSTAR PIC<p style=\"font-size:12px; font-weight:200;\">only show you hashtag posts with Karina (from.official, personal)</p></h2>
  <div id=\"gallery\" class=\"gallery\"></div>
  <div id=\"loader\"><div class=\"spinner\"></div></div>
  <div id=\"lightbox\" class=\"lightbox\" onclick=\"hideLightbox()\"><img id=\"lightbox-img\" src=\"\"></div>
  <script>
    const images = {data_json};
    let currentIndex = 0;
    const initialCount = {initial_count}, batchSize = {batch_size};
    const gallery = document.getElementById('gallery'), loader = document.getElementById('loader');

    function showLightbox(src) {{
      document.getElementById('lightbox').style.display = 'flex';
      document.getElementById('lightbox-img').src = src;
    }}
    function hideLightbox() {{ document.getElementById('lightbox').style.display = 'none'; }}

    function loadBatch(count) {{
      for (let i = 0; i < count && currentIndex < images.length; i++, currentIndex++) {{
        const d = images[currentIndex];
        const item = document.createElement('div'); item.className = 'item';
        const img = document.createElement('img');
        img.src = d.src; img.alt = d.hover; img.title = d.hover; img.loading = 'lazy';
        img.onclick = () => showLightbox(d.src);
        const cap = document.createElement('div'); cap.className = 'caption'; cap.innerHTML = `${{d.source}}<br>${{d.date}}`;
        item.append(img, cap);
        gallery.appendChild(item);
      }}
    }}

    function loadInitial() {{ loader.style.display = 'block'; setTimeout(() => {{ loadBatch(initialCount); loader.style.display = 'none'; }}, 200); }}
    function loadNext() {{ if (currentIndex < images.length) {{ loader.style.display = 'block'; setTimeout(() => {{ loadBatch(batchSize); loader.style.display = 'none'; }}, 200); }} }}

    // 초기 로딩 및 스크롤 이벤트 등록
    loadInitial();
    window.addEventListener('scroll', () => {{
      if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 150) loadNext();
    }});
  </script>
</body>
</html>"""
)

if __name__ == '__main__':
    imgs = collect_images(folders)
    generate_html(imgs)
    print("✅ karina_gallery.html 생성 완료 (초기 로드 + 무한 스크롤 + 스피너)")

#=================================================#
#[업데이트시 - 2단계 (html생성용.py)]
# python generate_gallery.py 터미널 명령어 입력을 통해 
# karina_gallery.html 파일이 새로 덮어쓰기되며
# aespa_karina 폴더 안의 모든 .jpg 이미지를 갤러리로 자동 연결 
