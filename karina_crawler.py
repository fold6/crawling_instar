import instaloader
from datetime import datetime, timedelta

L = instaloader.Instaloader()
L.load_session_from_file('내인스타아이디적기')  # ← 인스타 ID *로그인 세션을 저장(2단계인증계정추천)해놓은 프로세스가 있어야 불러올 수 있음

# 아래 단계가 로그인세션 저장을 위한 프로세스
# USERNAME = 'your_username'  # 너의 인스타 아이디
# PASSWORD = 'your_password'  # 너의 인스타 비번
# L.login(USERNAME, PASSWORD)


# 현재 시간 기준 11일 이내만
now = datetime.utcnow()
recent_cutoff = now - timedelta(days=11)

# 에스파 공식 계정에서 #카리나 포함 게시물만
aespa = instaloader.Profile.from_username(L.context, 'aespa_official')
for post in aespa.get_posts():
    if post.date_utc < recent_cutoff:
        break  # 오래된 게시물이므로 중단
    if '#카리나' in (post.caption or ''):
        L.download_post(post, target='aespa_karina')

# 카리나 개인 계정에서 11일 이내 게시물만
karina = instaloader.Profile.from_username(L.context, 'katarinabluu')
for post in karina.get_posts():
    if post.date_utc < recent_cutoff:
        break
    L.download_post(post, target='karina_personal')

#=================================================#
#[업데이트시 - 1단계(크롤링용.py)]
# python karina_crawler.py 터미널 명령어 입력을 통해 다시한번 크롤링을 함 (2단계인증 아이디필요)
# 🔴오래된 게시물은 크롤링하지 않아도 되므로, days=?으로 제한함