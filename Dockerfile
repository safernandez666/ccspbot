FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=America/Argentina/Buenos_Aires

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Compile the question bank into the image. content/*.json is the source of
# truth; the database is a build artifact and is never committed.
RUN python sql/build_db.py

# Attempt history lives here and must be mounted, or it is lost on restart:
#   docker run -e TOKEN_BOT=... -v ccspbot-data:/app/data ccspbot
VOLUME /app/data

# TOKEN_BOT is deliberately NOT a build ARG. Baking it in would write the
# token into a layer of a publicly pushed image. Supply it at run time.
CMD ["python", "app.py"]
