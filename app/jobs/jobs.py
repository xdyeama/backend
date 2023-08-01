from apscheduler.schedulers.background import BackgroundScheduler
from tasks import scrape_news


scheduler = BackgroundScheduler()

scheduler.add_job(scrape_news, trigger="cron", hour=15, minute=5)


