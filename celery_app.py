"""
Celery App Configuration for Pharmyrus
"""

import os
import logging

from celery import Celery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Redis URL from Railway environment variable
redis_url = os.getenv('REDIS_URL')

# Debug logging
if redis_url:
    logger.info(f"✅ REDIS_URL found: {redis_url[:50]}...")
else:
    logger.error("❌ REDIS_URL not found! Using localhost fallback")
    redis_url = 'redis://localhost:6379/0'

# Create Celery app
app = Celery(
    'pharmyrus',
    broker=redis_url,
    backend=redis_url
)

# Configure
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_send_sent_event=True,
    task_time_limit=3600,  # 60 min
    task_soft_time_limit=3300,  # 55 min
    result_expires=86400,  # 24h
    broker_connection_retry_on_startup=True,
    worker_prefetch_multiplier=1,
)

logger.info(f"🚀 Celery configured with broker: {redis_url[:50]}...")

# CRITICAL: Import tasks module to register them with Celery
# This MUST happen after app is configured
try:
    import tasks
    logger.info("✅ Tasks module imported successfully")
except ImportError as e:
    logger.error(f"❌ Failed to import tasks: {e}")
