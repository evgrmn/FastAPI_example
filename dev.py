import os

os.system("celery -A endpoints._celery.celery_app worker --loglevel=INFO -Q test-queue --detach")
os.system("uvicorn main:app --reload")