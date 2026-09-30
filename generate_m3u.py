import time
import requests

def generate_m3u():
    # Tạo timestamp theo chuẩn miligiây của API
    timestamp = int(time.time() * 1000)
    api_url = f"https://gavangtv-api.adviceme.io/api/v1/matches?webType=gavang&t={timestamp}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Referer": "https://gavang33.live",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()
        res_data = response.json()
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}")
        return

    if not res_data.get("success") or "data" not in res_data:
        print("API không trả về dữ liệu hợp lệ!")
        return

    matches = res_data["data"]
    m3u_lines = ["#EXTM3U x-tvg-url=\"\"\n"]
    
    for match_slug, match in matches.items():
        # Lấy thời gian, tên đội bóng và logo đội nhà
        time_str = match.get("matchNormalizedDate", "")
        home_team = match.get("homeTeam", {}).get("name", "")
        away_team = match.get("awayTeam", {}).get("name", "")
        logo = match.get("homeTeam", {}).get("logo") or match.get("homeTeam", {}).get("countryLogo") or ""
        
        anchors = match.get("anchorAppointmentVoList", [])
        
        # Trường hợp trận đấu có Bình luận viên (BLV)
        if anchors:
            for anchor in anchors:
                blv_name = anchor.get("nickName", "BLV")
                stream_urls = anchor.get("streamUrls", [])
                
                for stream_url in stream_urls:
                    # Xác định định dạng hls hoặc flv
                    ext = "hls" if ".m3u8" in stream_url else ("flv" if ".flv" in stream_url else "stream")
                    
                    # Cấu trúc tiêu đề đúng mẫu: 16:00 30/09 ⚽ Timor Leste vs Cambodia (Gà Siêu Kiêu) [flv]
                    title = f"{time_str} ⚽ {home_team} vs {away_team} ({blv_name}) [{ext}]"
                    
                    # Gắn User-Agent & Referer vào cuối URL để TiviMate/IPTV phát được không bị chặn Referer
                    play_url = f"{stream_url}|Referer=https://gavang33.live&User-Agent=Mozilla/5.0"
                    
                    m3u_lines.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="Gà Vàng 33 TV",{title}\n')
                    m3u_lines.append(f'#EXTVLCOPT:http-referrer=https://gavang33.live\n')
                    m3u_lines.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n')
                    m3u_lines.append(f'{play_url}\n\n')
        else:
            # Trường hợp chưa/không có BLV, sử dụng link mặc định nếu có
            default_link = match.get("defaultLink")
            if default_link:
                ext = "hls" if ".m3u8" in default_link else "stream"
                title = f"{time_str} ⚽ {home_team} vs {away_team} (Mặc định) [{ext}]"
                play_url = f"{default_link}|Referer=https://gavang33.live&User-Agent=Mozilla/5.0"
                
                m3u_lines.append(f'#EXTINF:-1 tvg-logo="{logo}" group-title="Gà Vàng 33 TV",{title}\n')
                m3u_lines.append(f'#EXTVLCOPT:http-referrer=https://gavang33.live\n')
                m3u_lines.append(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n')
                m3u_lines.append(f'{play_url}\n\n')

    # Xuất ra file gavang33.m3u
    with open("gavang33.m3u", "w", encoding="utf-8") as f:
        f.writelines(m3u_lines)

    print("Đã tạo thành công file gavang33.m3u!")

if __name__ == "__main__":
    generate_m3u()
  
