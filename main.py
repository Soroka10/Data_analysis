import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


file_path = "data.csv"
output_pdf = "EDA_Report.pdf"

try:
    df = pd.read_csv(
        file_path,
        delimiter=",",
        on_bad_lines="skip",
        quoting=3,
        encoding="utf-8",
        engine="python"
    )
    print("✅ Файл успішно прочитаний!")
except Exception as e:
    print("❌ Помилка:", e)
    exit()


df["created_time"] = pd.to_datetime(df["created_time"], errors="coerce")
df = df.dropna(subset=["created_time", "likes_count", "comments_count", "shares_count"])
df["likes_count"] = pd.to_numeric(df["likes_count"], errors="coerce")
df["comments_count"] = pd.to_numeric(df["comments_count"], errors="coerce")
df["shares_count"] = pd.to_numeric(df["shares_count"], errors="coerce")
df = df.dropna()


sns.set(style="whitegrid")


fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.histplot(df["likes_count"], bins=30, ax=axes[0], color="blue")
axes[0].set_title("Розподіл лайків")

sns.histplot(df["comments_count"], bins=30, ax=axes[1], color="green")
axes[1].set_title("Розподіл коментарів")

sns.histplot(df["shares_count"], bins=30, ax=axes[2], color="red")
axes[2].set_title("Розподіл репостів")

plt.tight_layout()
plt.savefig("histograms.png")
plt.close()


plt.figure(figsize=(12, 6))
df.set_index("created_time").resample("D")["likes_count"].sum().plot(marker="o", linestyle="-")
plt.title("Лайки за днями")
plt.xlabel("Дата")
plt.ylabel("Кількість лайків")
plt.grid()
plt.savefig("likes_trend.png")
plt.close()


c = canvas.Canvas(output_pdf, pagesize=letter)
width, height = letter


c.setFont("Helvetica-Bold", 16)
c.drawString(30, height - 50, "📊 Аналіз Instagram-постів")


c.setFont("Helvetica", 12)
stats_text = f"""
Дата аналізу: {pd.Timestamp.today().strftime('%Y-%m-%d')}
Кількість постів: {len(df)}
Середня кількість лайків: {df['likes_count'].mean():.2f}
Середня кількість коментарів: {df['comments_count'].mean():.2f}
Середня кількість репостів: {df['shares_count'].mean():.2f}
"""
c.drawString(30, height - 80, stats_text)


c.drawImage(ImageReader("histograms.png"), 30, height - 400, width=500, height=180)
c.drawString(30, height - 420, "Розподіл лайків, коментарів і репостів")

c.drawImage(ImageReader("likes_trend.png"), 30, height - 620, width=500, height=180)
c.drawString(30, height - 640, "Тренд лайків за днями")

c.save()
print(f"📄 PDF-звіт збережено у {output_pdf}")
