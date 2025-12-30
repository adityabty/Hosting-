from database import get_or_create_user, update_credits
from config import CREDIT_COST_PER_HOUR
import time
import threading

def credit_worker():
    while True:
        time.sleep(3600)

        # later: fetch active bots + owners
        pass


threading.Thread(target=credit_worker, daemon=True).start()
