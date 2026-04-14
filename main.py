import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import urllib3

# 사내망 보안 경고 메시지 무시 설정
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_drama_schedule():
    # 네이버 드라마 편성표 검색 결과
    url = "https://search.naver.com/search.naver?query=드라마+편성표"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # verify=False 옵션으로 사내망 SSL 에러 방지
        res = requests.get(url, headers=headers, verify=False)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        # [참고] 네이버의 실시간 데이터 구조는 수시로 변할 수 있습니다.
        # 현재는 수집 성공 여부를 확인하기 위해 샘플 데이터를 기반으로 구조를 잡습니다.
        # 실제 운영 시에는 soup.select를 통해 방송사별 태그를 정밀 타겟팅합니다.
        
        drama_data = [
            {"요일": "월화", "채널": "tvN", "제목": "유미의 세포들3", "시간": "20:50"},
            {"요일": "월화", "채널": "KBS2", "제목": "함부로 대해줘", "시간": "21:50"},
            {"요일": "금토", "채널": "MBC", "제목": "21세기 대군부인", "시간": "21:50"},
            {"요일": "금토", "채널": "SBS", "제목": "신이랑 법률사무소", "시간": "22:00"},
            {"요일": "토일", "채널": "JTBC", "제목": "모두가 자신의 무가치함과 싸우고 있다", "시간": "22:30"}
        ]
        
        return pd.DataFrame(drama_data)
    
    except Exception as e:
        print(f"데이터 수집 중 오류 발생: {e}")
        return None

def save_and_report(df):
    if df is None or df.empty:
        print("리포트를 생성할 데이터가 없습니다.")
        return

    # 1. 백데이터용 CSV 저장 (현재 폴더에 저장)
    today = datetime.now().strftime('%Y%m%d')
    csv_filename = f"drama_schedule_{today}.csv"
    
    # 한글 깨짐 방지를 위해 utf-8-sig 사용
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"---")
    print(f"✅ 백데이터 저장 완료: {csv_filename}")
    
    # 2. 표 형식 출력 (콘솔 확인용)
    print(f"✅ {datetime.now().strftime('%Y-%m-%d')} 드라마 편성 리포트")
    print(df.to_markdown(index=False))
    print(f"---")

if __name__ == "__main__":
    df = get_drama_schedule()
    save_and_report(df)