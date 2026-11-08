FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd --create-home atlas && mkdir /data && chown atlas:atlas /data
COPY --chown=atlas:atlas app ./app
USER atlas
ENV DATABASE_PATH=/data/atlas.sqlite3 COOKIE_SECURE=true
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips '*' "]
