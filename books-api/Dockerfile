FROM python:3.11-slim AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM build AS development

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001", "--debug"]

FROM build AS production

RUN pip install --no-cache-dir gunicorn

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]