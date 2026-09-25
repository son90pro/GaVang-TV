import requests
import json

def generate_m3u():
    m3u_content = '#EXTM3U tvg-shift="0"\n\n'
    
    # Header giả lập trình duyệt để tránh bị chặn phát stream
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    referer = "https://gavangtv.com/" # Thay bằng domain nguồn phát tương ứng

    # Ví dụ danh sách trận đấu thu thập được từ API/Web
    matches = [
        {
            "title": "[20:00] Manchester United vs Liverpool",
            "group": "🔥 NGON - TRỰC TIẾP HÔM NAY",
            "logo": "https://i.imgur.com/mu-logo.png",
            "url": "https://example.com/live/stream1.m3u8"
        },
        {
            "title": "[22:30] Chelsea vs Tottenham",
            "group": "🔥 NGON - TRỰC TIẾP HÔM NAY",
            "logo": "https://i.imgur.com/chelsea-logo.png",
            "url": "https://example.com/live/stream2.m3u8"
        }
    ]

    for item in matches:
        # Thêm header vào sau URL để các app IPTV (TiviMate, OTT Navigator) vượt rào cản referrer/user-agent
        stream_link = f"{item['url']}|User-Agent={user_agent}&Referer={referer}"
        
        m3u_content += f'#EXTINF:-1 tvg-logo="{item["logo"]}" group-title="{item["group"]}", {item["title"]}\n'
        m3u_content += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer={referer}\n'
        m3u_content += f'{stream_link}\n\n'

    # Ghi nội dung vào file playlist.m3u
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    generate_m3u()
    
