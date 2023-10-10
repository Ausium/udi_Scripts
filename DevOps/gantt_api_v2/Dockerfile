FROM python:3.10-alpine3.17
COPY ./gantt_fastapi.py ./requirements.txt /root
WORKDIR /root
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "gantt_fastapi.py"]