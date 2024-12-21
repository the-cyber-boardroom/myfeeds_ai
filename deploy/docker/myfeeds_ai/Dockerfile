FROM python:3.12-slim

RUN pip install mangum uvicorn httpx fastapi
RUN pip install osbot-aws osbot-fast-api
RUN pip install myfeeds_ai

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

RUN python --version
ENV PORT=8080

WORKDIR /app
COPY ../../../myfeeds_ai /app/myfeeds_ai

ENV PYTHONPATH="/app"

COPY ./deploy/docker/myfeeds_ai/start.sh /app/start.sh

CMD ["./start.sh"]

