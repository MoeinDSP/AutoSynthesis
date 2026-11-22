#!/bin/sh
mkdir -p /app/outputs
chmod 777 /app/outputs

PDF_DIR="${DOWNLOADED_PDF_DIR:-downloaded_pdfs}"
case "$PDF_DIR" in
  /*)
    mkdir -p "$PDF_DIR"
    chmod 777 "$PDF_DIR"
    ;;
  *)
    mkdir -p "/app/outputs/$PDF_DIR"
    chmod 777 "/app/outputs/$PDF_DIR"
    ;;
esac

# APP_ROLE selects what this container instance does with the SAME image:
#   api     (default) -- the FastAPI dashboard, today's exact behaviour.
#   worker  -- a Celery worker consuming CELERY_TASK_QUEUE.
#   migrate -- run the Postgres migration runner once, then exit.
case "${APP_ROLE:-api}" in
  migrate)
    exec python -m persistence.migrate
    ;;
  worker)
    exec celery -A celery_app.app worker \
      -Q "${CELERY_TASK_QUEUE:-autosynthesis.pipeline}" \
      --concurrency "${CELERY_WORKER_CONCURRENCY:-2}" \
      --prefetch-multiplier 1 \
      --max-tasks-per-child "${CELERY_MAX_TASKS_PER_CHILD:-1}" \
      --loglevel "${CELERY_LOG_LEVEL:-INFO}" \
      -n "worker@%h-$$"
    ;;
  *)
    exec python dashboard.py
    ;;
esac
