import json
import os
import time
import redis
import settings
from joblib import load
import numpy as np

# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
  host=settings.REDIS_IP,
  port=settings.REDIS_PORT,
  db=settings.REDIS_DB_ID)

# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = load('pipe.joblib')


def predict(pts):
    return  int(model.predict(np.array(pts).reshape(-1, 1)).round(0)[0])

def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        #   1. Take a new job from Redis
        _ , job_data = db.brpop(settings.REDIS_QUEUE)
        
        #   2. Run your ML model on the given data
        job_data = json.loads(job_data)
        model_prediction = predict(float(job_data["PTS"]))
        db.set(job_data["id"], model_prediction)

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()