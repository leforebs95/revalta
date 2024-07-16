# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Add curl for healthcheck
RUN apt-get update && apt-get install -y curl

WORKDIR /usr/src/api

# Copy the source code into the container.
COPY . .

ENV PYTHONPATH=/usr/src/api

ENV AWS_ACCESS_KEY_ID="ASIA6GBMARJ6NYNFFFCE"
ENV AWS_SECRET_ACCESS_KEY="6aRPLN6QsLJpzUWDf6hP61IemnqDcrulATagCRv3"
ENV AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEAAaCXVzLXdlc3QtMiJHMEUCIQDxB1X2ZjHHiearzCbDbQ1GQnHA5hmai+0MUkzrw0wUBwIgNAeHCLIfH0kUNT+vdDgWjTraJc5mocPv6ptObm5IUY0q9AIIyf//////////ARAAGgw5NzUwNDk4ODYzMzIiDBj7OtGkB71pJ5AwWirIAh2Y2g3RD6x27s8Yr7LzlO+nvn9+vEidKTiVAvGzlW4zyPJWdfX0g2MJ8EgQNWLhFEldGBM2PPEB1jxA2vu1GbttyV6t9GHsd6Jaf44Yp2z++TByA+g5hjTW9fVnzxHjDNZI8DNbcmu4UbGp0G9fT7zCj71nOQBcnuXIcsVqTRNj4f7E0c8v2CRHGeMqbWdKXIyY9mAcYmMyQnyICb8zXjf8P9aqnov3uWpXUvKHov97RB1VmHGQugmByH86xNBLffQ9LL/e5g1HH+ylLl7ZOXJ69aGfEhCOu1Vn2kW0MzPkuOIZc9rXr5fJ3g23xG/BonWYks1pYNWVPHVUMz/KNhqmQSTh/aiuYKR4HZHAAyYKa7BOwCEJaiPbhAyDgxmlw9HaI7sJ2jMxDCJB7/Z9vTcFVWwccWRYzm23RVyaXG2v42i8Zh0Mho0wvfHWtAY6pwHgdcSbE5sSTyx1AVPVeZwfFpoTFMIItDGqjOBfAYDGhVTfBr1PFQszyokbsCsgRT0ojPDfT+zOFV/3JEYXQqKK7VorqREkKMlKO4eniwXtORK56RPHl/eoBCDeA0SJvChptzDTneJBTG2d/jxn3TCSPbLTarm29gzpRoUC3CNWHTuff3gmYENiOv7V0SPR9+9dyYfIbOM3PQjZtAYt4wXA9AhWQ+/4pQ=="

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install dependencies for MariabDB Connector/C
RUN apt-get update && apt-get install -y \
gcc \
python3-dev \
openssl

# Install MariaDB Connector/C
RUN apt-get update && apt-get install -y \
libmariadb3 \
libmariadb-dev

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r /usr/src/api/requirements.txt

# Create log dirs
RUN mkdir -p /var/log/gunicorn/ && chown -R appuser:appuser /var/log/gunicorn/

# Switch to the non-privileged user to run the application.
USER appuser

EXPOSE 5000

# Run the application.
CMD ["gunicorn", "--chdir", "/usr/src/api", "-c", "/usr/src/api/gunicorn_dev.py"]