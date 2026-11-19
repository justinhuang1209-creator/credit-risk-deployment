FROM python:3.11-slim
RUN useradd -m -u 1000 user
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=user:user . .
USER user
ENV HOME=/home/user GRADIO_ANALYTICS_ENABLED=False
EXPOSE 7860
CMD ["python", "app.py"]
