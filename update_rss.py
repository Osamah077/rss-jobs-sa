import feedparser
from datetime import datetime

# روابط RSS الخاصة بتنبيهات Google Alerts
rss_links = [
    "https://www.google.com/alerts/feeds/02094315391893505011/9151460460105884746",
    "https://www.google.com/alerts/feeds/02094315391893505011/6805183905483548191",
    "https://www.google.com/alerts/feeds/02094315391893505011/6805183905483548114",
    "https://www.google.com/alerts/feeds/02094315391893505011/16102999831032449615",
    "https://www.google.com.sa/alerts/feeds/02094315391893505011/6240063675421501745",
    "https://www.google.com.sa/alerts/feeds/02094315391893505011/868323184601300714",
    "https://www.google.com.sa/alerts/feeds/02094315391893505011/868323184601299385",
    "https://www.google.com.sa/alerts/feeds/02094315391893505011/9680062043210233641",
    "https://www.google.com.sa/alerts/feeds/02094315391893505011/868323184601298883"
]

all_items = []

# قراءة كل الروابط
for url in rss_links:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        all_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")),
            "description": entry.get("summary", "وظيفة جديدة - اضغط الرابط للتفاصيل")
        })

# ترتيب الأحدث أولاً
all_items = sorted(all_items, key=lambda x: x["published"], reverse=True)

# إنشاء محتوى RSS جديد
rss_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
rss_content += '<rss version="2.0">\n<channel>\n'
rss_content += '<title>وظائف السعودية الموحدة</title>\n'
rss_content += '<link>https://osamah077.github.io/rss-jobs-sa/</link>\n'
rss_content += '<description>تحديث تلقائي كل ساعة</description>\n'

for item in all_items[:30]:  # فقط آخر 30 وظيفة
    rss_content += f"<item>\n"
    rss_content += f"<title>{item['title']}</title>\n"
    rss_content += f"<link>{item['link']}</link>\n"
    rss_content += f"<description>{item['description']}</description>\n"
    rss_content += f"<pubDate>{item['published']}</pubDate>\n"
    rss_content += "</item>\n"

rss_content += "</channel>\n</rss>"

# حفظه في index.xml
with open("index.xml", "w", encoding="utf-8") as f:
    f.write(rss_content)

print("✅ تم تحديث ملف index.xml بنجاح")
