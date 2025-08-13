FROM python:3.11-slim AS build

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM build AS development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]

FROM build AS production

RUN pip install --no-cache-dir gunicorn

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]