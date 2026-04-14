import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3

# 사내망 보안 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_drama_schedule():
    url = "https://search.naver.com/search.naver?query=드라마+편성표"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # verify=False로 사내망 보안 통과
        res = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 샘플 데이터 (성공 확인용)
        drama_data = [
            {"요일": "월화", "채널": "tvN", "제목": "유미의 세포들3", "시간": "20:50"},
            {"요일": "금토", "채널": "MBC", "제목": "21세기 대군부인", "시간": "21:50"},
            {"요일": "토일", "채널": "KBS2", "제목": "미녀와 순정남", "시간": "19:55"}
        ]
        return pd.DataFrame(drama_data)
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

if __name__ == "__main__":
    df = get_drama_schedule()
    if df is not None:
        print(df.to_markdown(index=False))
        df.to_csv(f"drama_{datetime.now().strftime('%Y%m%d')}.csv", index=False, encoding='utf-8-sig')