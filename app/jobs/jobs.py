from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import scrape_news


scheduler = BackgroundScheduler()

scheduler.add_job(scrape_news, "cron", hour=19, minute=54)
# scheduler.add_job(scrape_news, "interval", hours=1)
