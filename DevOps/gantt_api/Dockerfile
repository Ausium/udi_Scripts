FROM python:3.10-alpine3.17
COPY ./gantt_api.py ./requirements.txt /root
WORKDIR /root
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "gantt_api.py"]
