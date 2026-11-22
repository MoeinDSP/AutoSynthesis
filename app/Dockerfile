FROM python:3.11-slim

# System dependencies required by numpy/scipy/matplotlib, plus R + metafor
# (the actual meta-analysis statistics engine, called via rpy2 -- see
# statistics/metafor_engine.py) and the -dev packages rpy2's C extension
# needs to link against libR.so and everything it depends on -- this exact
# set of -l flags comes from rpy2's own build-time test-link command
# (libtirpc alone was enough on a fuller Debian/Ubuntu base, but this slim
# image needs the rest spelled out too).
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
        libglib2.0-0 \
        libgl1 \
        fonts-dejavu-core \
        r-base-core \
        r-cran-metafor \
        build-essential \
        libtirpc-dev \
        libpcre2-dev \
        libdeflate-dev \
        libzstd-dev \
        liblzma-dev \
        libbz2-dev \
        zlib1g-dev \
        libicu-dev \
        libblas-dev \
        liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Explicit, not relied-upon-by-accident: `python dashboard.py` and
# `python -m persistence.migrate` both already get /app on sys.path for
# free (CPython adds the script's own directory / CWD respectively). The
# `celery` console-script entry point (APP_ROLE=worker) does NOT -- it's a
# script installed under /usr/local/bin, so sys.path[0] is THAT directory,
# not /app, and top-level modules (run_service, tasks, celery_app) fail to
# import from inside a forked worker child. PYTHONPATH fixes it uniformly
# for every role built from this image.
ENV PYTHONPATH=/app

# Install Python dependencies first (layer is cached unless requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps chromium

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
