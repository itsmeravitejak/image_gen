import json
import redis
import os

r = redis.Redis(
  host=os.getenv("REDIS_HOST"),
  port=int(os.getenv("REDIS_PORT")),
  password=os.getenv("REDIS_PASS"),
  ssl=os.getenv("REDIS_SSL")=="True"
)
if r.ping():
    print("✅ Redis is connected!")
else:
    print("❌ Redis is not responding.")

def update_model_training(training,token):
    record=r.get("model_"+token)
    if(record):
        record=json.loads(record)
        record['version']=training['output']['version']
        return r.set("model_"+token, json.dumps(record))
    

def get_models_redis():
    model_response=[]
    for model in list(r.scan_iter("model_*")):
        model_response.append(json.loads(r.get(model)))
    return model_response

def get_scenarios_redis():    
    scenario_response=[]
    for scenario in list(r.scan_iter("scenario_*")):
        scenario_response.append(json.loads(r.get(scenario)))
    return scenario_response

def create_model_redis(model):
    return r.set("model_"+model['token'], json.dumps(model))