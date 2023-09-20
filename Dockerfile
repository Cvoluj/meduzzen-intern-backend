FROM python:3.9

ENV HOST=0.0.0.0
ENV PORT=8000
ENV RELOAD=True
ENV LOG_LEVEL=info

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR app

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
