from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import scrape_news


scheduler = BackgroundScheduler()

scheduler.add_job(scrape_news, "cron", hour=21, minute=30)
# scheduler.add_job(scrape_news, "interval", hours=1)
