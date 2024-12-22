osbot_utils=${PWD}/modules/OSBot-Utils/
osbot_aws=${PWD}/modules/OSBot-AWS/

export PYTHONPATH=$osbot_fast_api:$osbot_utils:$osbot_aws:$PYTHONPATH

uvicorn myfeeds_ai.lambdas.handler:app --reload --host 0.0.0.0 --port 7777