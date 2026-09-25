import json
import re
import requests

def create_m3u_playlist():
    # Khai báo Header giả lập trình duyệt để vượt rào cản anti-hotlink của server stream
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    referer = "https://gavang33.me/"

    m3u_content = '#EXTM3U tvg-shift="0"\n\n'

    # Danh sách mẫu cấu trúc chuẩn hỗ trợ phát m3u8 trực tiếp & hiển thị đẹp
    # Code sẽ tự động thêm User-Agent và Referer để ứng dụng (TiviMate, OTT Navigator, VLC...) phát mượt mà không bị đen màn hình
    matches = [
        {
            "title": "[20:00] Trực Tiếp Bóng Đá - Kênh 1",
            "group": "🔥 TRỰC TIẾP HÔM NAY",
            "logo": "https://flagcdn.com/w320/un.png",
            "url": "https://example.com/live/stream1/playlist.m3u8"
        },
        {
            "title": "[22:30] Trực Tiếp Bóng Đá - Kênh 2",
            "group": "🔥 TRỰC TIẾP HÔM NAY",
            "logo": "https://flagcdn.com/w320/un.png",
            "url": "https://example.com/live/stream2/playlist.m3u8"
        }
    ]

    count = 0
    for match in matches:
        title = match["title"]
        group = match["group"]
        logo = match["logo"]
        stream_url = match["url"]

        # Chuỗi bypass chặn phát trực tiếp
        full_url = f"{stream_url}|User-Agent={user_agent}&Referer={referer}"

        m3u_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}", {title}\n'
        m3u_content += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer={referer}\n'
        m3u_content += f'{full_url}\n\n'
        count += 1

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"Đã tạo thành công file playlist.m3u với {count} kênh.")

if __name__ == "__main__":
    create_m3u_playlist()
  
