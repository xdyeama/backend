from apscheduler.schedulers.background import BackgroundScheduler
from tasks import scrape_news


scheduler = BackgroundScheduler()

scheduler.add_job(scrape_news, trigger="cron", hour=14, minute=30)


