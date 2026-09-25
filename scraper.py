def format_m3u_entry(group_name, match_time, match_date, home_team, away_team, commentator, stream_type, logo_url, stream_url, referer_url):
    """
    Hàm tạo 1 block M3U chuẩn hiển thị đầy đủ giao diện như OTT Navigator / TiviMate
    """
    # 1. Tạo tên hiển thị chuẩn: 🟢 13:00 25/09 ⚽ China Women vs Vietnam Women (Gà Siêu Nhí) [hls]
    display_title = f"🟢 {match_time} {match_date} ⚽ {home_team} vs {away_team} ({commentator}) [{stream_type}]"
    
    # 2. Xử lý đường dẫn stream kèm Header Referer để không bị chặn
    full_stream_url = f"{stream_url}|Referer={referer_url}&User-Agent=Mozilla/5.0"
    
    # 3. Tạo dòng #EXTINF với group-title và tvg-logo
    extinf_line = f'#EXTINF:-1 group-title="{group_name}" tvg-logo="{logo_url}", {display_title}'
    
    return f"{extinf_line}\n{full_stream_url}\n"


# Ví dụ tạo danh sách dữ liệu mẫu
matches_data = [
    {
        "group": "Gà Vàng 33 TV",
        "time": "13:00",
        "date": "25/09",
        "home": "China Women",
        "away": "Vietnam Women",
        "commentator": "Gà Siêu Nhí",
        "type": "hls",
        "logo": "https://flagcdn.com/w320/cn.png",  # Link logo cờ Trung Quốc
        "stream_url": "https://example.com/live1.m3u8",
        "referer": "https://gavang33.me/"
    },
    {
        "group": "Gà Vàng 33 TV",
        "time": "12:00",
        "date": "25/09",
        "home": "Uzbekistan U23",
        "away": "Saudi Arabia U23",
        "commentator": "Gà Siêu Tổ",
        "type": "flv",
        "logo": "https://flagcdn.com/w320/uz.png",  # Link logo cờ Uzbekistan
        "stream_url": "https://example.com/live2.m3u8",
        "referer": "https://gavang33.me/"
    },
    {
        "group": "Gà Vàng 33 TV",
        "time": "16:00",
        "date": "25/09",
        "home": "Bangladesh",
        "away": "Malaysia",
        "commentator": "Gà Siêu Kiều",
        "type": "flv",
        "logo": "https://flagcdn.com/w320/bd.png",  # Link logo cờ Bangladesh
        "stream_url": "https://example.com/live3.m3u8",
        "referer": "https://gavang33.me/"
    }
]

# Tạo nội dung M3U hoàn chỉnh
m3u_output = '#EXTM3U tvg-shift="0"\n\n'
for item in matches_data:
    m3u_output += format_m3u_entry(
        group_name=item["group"],
        match_time=item["time"],
        match_date=item["date"],
        home_team=item["home"],
        away_team=item["away"],
        commentator=item["commentator"],
        stream_type=item["type"],
        logo_url=item["logo"],
        stream_url=item["stream_url"],
        referer_url=item["referer"]
    )

# Lưu ra file
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u_output)

print("Đã tạo file playlist.m3u chuẩn giao diện!")
