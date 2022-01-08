FROM python:3.10-bullseye

WORKDIR /usr/app/

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/usr/app/:/usr/app/src"
ENV HOST=0.0.0.0
ENV PORT=80

EXPOSE 80

COPY . .

ENTRYPOINT ["./entrypoint.sh"]