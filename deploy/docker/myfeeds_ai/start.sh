#!/bin/bash

uvicorn myfeeds_ai.lambdas.handler:app --host 0.0.0.0 --port 8080