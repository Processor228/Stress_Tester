FROM python:3.10

WORKDIR app/

# Copy requirements.txt and sources
COPY requirements.txt .
COPY src ./src

# Install python libs
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uvicorn", "src.main:app"]
