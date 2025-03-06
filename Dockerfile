FROM python:3.12

WORKDIR /src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["uvicorn", "src.server:create_app", "--host", "0.0.0.0", "--port", "8085"]
