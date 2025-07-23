
import datetime
import requests
from bs4 import BeautifulSoup
import time

# ✅ الصورة الافتراضية
DEFAULT_IMAGE = "https://raw.githubusercontent.com/Osamah077/rss-jobs-sa/refs/heads/main/%D9%84%D9%88%D8%AC%D9%88%20%D8%AF%D8%A7%D8%B1%20%D8%AB%D9%82%D8%A7%D9%81%D8%A9%20%D8%A7%D8%B5%D9%81%D8%B1%20%D9%88%20%D8%A7%D8%A8%D9%8A%D8%B6%20%D8%AA%D8%B9%D9%84%D9%8A%D9%85%20(3).png"

# ✅ وظيفة إعادة المحاولة عند فشل الاتصال
def fetch_with_retry(url, retries=3, delay=5):
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"⚠️ محاولة {i+1} فشلت: {e} .. إعادة المحاولة بعد {delay} ثانية")
            time.sleep(delay)
    raise Exception("❌ فشلت جميع المحاولات")

# ✅ جلب وظائف البلوقر
BLOGGER_RSS = "https://jobsksa2026.blogspot.com/feeds/posts/default?alt=rss"
resp = fetch_with_retry(BLOGGER_RSS)
soup = BeautifulSoup(resp.content, "xml")

blogger_jobs = []
for item in soup.find_all("item"):
    title = item.title.text.strip()
    link = item.link.text.strip()
    pub_date = item.pubDate.text.strip()
    description = item.description.text.strip()

    # محاولة استخراج الصورة من الوصف
    soup_desc = BeautifulSoup(description, "html.parser")
    img_tag = soup_desc.find("img")
    image_url = img_tag["src"] if img_tag else DEFAULT_IMAGE

    blogger_jobs.append({
        "title": title,
        "url": link,
        "description": description,
        "pub_date": pub_date,
        "image_url": image_url
    })

# ✅ وظائف السكريبت الأصلية (تعديل حسب ما تبرمج أنت)
original_jobs = [
    {
        "title": "وظيفة سكريبت تجريبية",
        "url": "https://jobsksa2026.blogspot.com/2025/07/example.html",
        "description": "هذه وظيفة مضافة من السكريبت فقط",
        "pub_date": datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"),
        "image_url": DEFAULT_IMAGE
    }
]

# ✅ دمج كل الوظائف
all_jobs = blogger_jobs + original_jobs

# ✅ توليد عناصر RSS
rss_items = []
for job in all_jobs:
    image_final = job["image_url"] if job["image_url"] else DEFAULT_IMAGE
    rss_items.append(f"""
    <item>
        <title>{job['title']}</title>
        <link>{job['url']}</link>
        <description><![CDATA[{job['description']}]]></description>
        <pubDate>{job['pub_date']}</pubDate>
        <media:content url="{image_final}" medium="image" />
    </item>
    """)

# ✅ إنشاء ملف RSS النهائي
rss_feed = f"""
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
    <title>وظائف السعودية المدمجة</title>
    <link>https://jobsksa2026.blogspot.com/</link>
    <description>آخر الوظائف من البلوقر والسكريبت</description>
    {''.join(rss_items)}
</channel>
</rss>
"""

with open("index.xml", "w", encoding="utf-8") as f:
    f.write(rss_feed)

print("✅ تم تحديث RSS بنجاح")
