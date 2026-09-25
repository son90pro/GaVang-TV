import re
import os
import cloudscraper
from bs4 import BeautifulSoup

BASE_URL = "https://gavang33.me"

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

def extract_m3u_gavang():
    m3u_content = '#EXTM3U tvg-shift="0"\n'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': f'{BASE_URL}/',
        'Origin': BASE_URL
    }

    try:
        print(f"Đang kết nối tới {BASE_URL}...")
        response = scraper.get(BASE_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            match_cards = soup.select('a[href*="/truc-tiep/"], div.match-item, .item-match')
            
            count = 0
            for card in match_cards:
                title_elem = card.select_one('.match-detail, .teams-name, .title, .name')
                title = title_elem.text.strip() if title_elem else card.get('title', 'Trận đấu Gà Vàng TV')
                
                time_elem = card.select_one('.time, .match-time')
                match_time = time_elem.text.strip() if time_elem else ""
                
                href = card.get('href') or card.get('data-href')
                if not href:
                    continue
                    
                match_url = href if href.startswith('http') else f"{BASE_URL}{href}"
                
                try:
                    detail_res = scraper.get(match_url, headers=headers, timeout=10)
                    if detail_res.status_code == 200:
                        m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', detail_res.text)
                        
                        if m3u8_links:
                            stream_link = m3u8_links[0]
                            display_title = f"[{match_time}] {title}" if match_time else title
                            full_stream_url = f"{stream_link}|Referer={BASE_URL}/&User-Agent=Mozilla/5.0"
                            
                            m3u_content += f'#EXTINF:-1 group-title="Gà Vàng TV", {display_title}\n'
                            m3u_content += f'{full_stream_url}\n'
                            count += 1
                            print(f"Đã cập nhật: {display_title}")
                except Exception:
                    continue

            print(f"-> Tổng số trận đấu trích xuất thành công: {count}")
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")

    return m3u_content

if __name__ == "__main__":
    playlist_data = extract_m3u_gavang()
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist_data)
    print("-> Đã lưu dữ liệu vào file playlist.m3u")
  
