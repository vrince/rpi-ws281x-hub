#!/bin/bash
sudo celery -A playground worker --concurrency=1  --loglevel=info