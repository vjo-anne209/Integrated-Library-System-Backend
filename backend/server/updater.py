from apscheduler.schedulers.background import BackgroundScheduler
from .views import calculateFine

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(calculateFine, 'interval', days = 1)
    scheduler.start()