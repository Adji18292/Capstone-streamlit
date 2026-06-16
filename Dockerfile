# Menggunakan base image Python 3.10
FROM python:3.10

# Membuat user non-root agar aman (Syarat Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy file requirements dan install
COPY --chown=user requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh file project
COPY --chown=user . /app/

# Pindah ke folder model_AI agar path model-model ML terbaca dengan benar
WORKDIR /app/model_AI

# Jalankan server FastAPI di port 7860 (Port default Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
