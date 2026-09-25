import json
import re
import cloudscraper
from bs4 import BeautifulSoup

BASE_URL = "https://gavang33.me"

def get_gavang_next_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': f'{BASE_URL}/',
        'Origin': BASE_URL
    }

    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )

    m3u_content = '#EXTM3U tvg-shift="0"\n\n'
    total_channels = 0

    try:
        print(f"Đang kết nối tới {BASE_URL}...")
        response = scraper.get(BASE_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tìm thẻ script chứa toàn bộ dữ liệu Next.js của trang
            next_data_script = soup.find('script', id='__NEXT_DATA__')
            
            if next_data_script:
                print("-> Đã tìm thấy cấu trúc dữ liệu JSON gốc!")
                data = json.loads(next_data_script.string)
                
                # Truy xuất vào danh sách các trận đấu
                page_props = data.get('props', {}).get('pageProps', {})
                matches = page_props.get('matches', []) or page_props.get('dehydratedState', {}).get('queries', [])
                
                # Nếu cấu trúc lưu dưới dạng dehydratedState (React Query)
                if not matches and 'dehydratedState' in page_props:
                    for query in page_props['dehydratedState'].get('queries', []):
                        if 'data' in query and isinstance(query['data'], list):
                            matches = query['data']
                            break

                print(f"-> Phát hiện {len(matches)} trận đấu trong hệ thống.")

                for match in matches:
                    if not isinstance(match, dict):
                        continue
                        
                    # Trích xuất thông tin trận đấu
                    home_team = match.get('home_name') or match.get('homeTeam', {}).get('name', 'Đội nhà')
                    away_team = match.get('away_name') or match.get('awayTeam', {}).get('name', 'Đội khách')
                    match_time = match.get('match_time') or match.get('time', '')
                    
                    # Cờ/Logo đội bóng
                    logo = match.get('home_icon') or match.get('homeTeam', {}).get('icon', '')
                    if not logo:
                        logo = "https://flagcdn.com/w320/un.png"

                    # Danh sách các link phát (Servers)
                    links = match.get('links', []) or match.get('servers', [])
                    
                    for idx, link_info in enumerate(links):
                        if not isinstance(link_info, dict):
                            continue
                            
                        stream_url = link_info.get('url') or link_info.get('m3u8') or link_info.get('stream_url')
                        blv_name = link_info.get('blv_name') or link_info.get('name') or f"Server {idx+1}"
                        stream_type = "hls" if "m3u8" in str(stream_url) else "flv"

                        if stream_url:
                            display_title = f"🟢 {match_time} ⚽ {home_team} vs {away_team} ({blv_name}) [{stream_type}]"
                            
                            # Chèn Header Referer để tránh bị chặn khi xem trên OTT Navigator / TiviMate
                            full_stream_url = f"{stream_url}|Referer={BASE_URL}/&User-Agent=Mozilla/5.0"
                            
                            m3u_content += f'#EXTINF:-1 group-title="Gà Vàng 33 TV" tvg-logo="{logo}", {display_title}\n'
                            m3u_content += f'{full_stream_url}\n\n'
                            total_channels += 1

            # Phương pháp dự phòng (Quét Regex nếu trang đổi cấu trúc JSON)
            if total_channels == 0:
                print("-> Chuyển sang phương pháp quét luồng phụ...")
                m3u8_links = list(set(re.findall(r'https?://[^\s"\']+\.m3u8[^\s"\']*', response.text)))
                for idx, url in enumerate(m3u8_links, start=1):
                    if "ad" in url.lower() or "segment" in url.lower():
                        continue
                    full_stream_url = f"{url}|Referer={BASE_URL}/&User-Agent=Mozilla/5.0"
                    m3u_content += f'#EXTINF:-1 group-title="Gà Vàng 33 TV", Trực Tiếp Gà Vàng - Luồng {idx}\n'
                    m3u_content += f'{full_stream_url}\n\n'
                    total_channels += 1

            print(f"==> TỔNG CỘNG ĐÃ TẠO: {total_channels} kênh trận đấu.")
        else:
            print(f"Lỗi truy cập {BASE_URL}: Status {response.status_code}")

    except Exception as e:
        print(f"Lỗi trong quá trình xử lý: {e}")

    return m3u_content

if __name__ == "__main__":
    m3u_result = get_gavang_next_data()
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_result)
    print("Đã cập nhật file playlist.m3u thành công!")
    
