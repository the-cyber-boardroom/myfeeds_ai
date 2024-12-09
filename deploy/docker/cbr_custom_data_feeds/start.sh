#!/bin/bash

uvicorn cbr_custom_data_feeds.lambdas.handler:app --host 0.0.0.0 --port 8080