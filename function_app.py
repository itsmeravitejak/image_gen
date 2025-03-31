import azure.functions as func
import logging
import json
import replicate
from redis_funcs import get_models_redis,create_model_redis,update_model_training,get_scenarios_redis
from replicate_apis import create_model_repl,get_training
import os


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    response_data = {
        "message": "Send a name in query",
        "status": "success",
        "data": {"id": 1, "name": "Azure"}
    }
    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )


@app.route(route="get_models")
def get_models(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Asked for all models')
    # config= { "host":os.getenv("REDIS_HOST"),"port":int(os.getenv("REDIS_PORT")),"password":os.getenv("REDIS_PASS"),"ssl":os.getenv("REDIS_HOST")=="True" }    
    # logging.info(config)
    return func.HttpResponse(
            json.dumps(get_models_redis()),
            mimetype="application/json",
            status_code=200
            )

@app.route(route="get_scenarios")
def get_scenarios(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Asked for all models')
    # config= { "host":os.getenv("REDIS_HOST"),"port":int(os.getenv("REDIS_PORT")),"password":os.getenv("REDIS_PASS"),"ssl":os.getenv("REDIS_HOST")=="True" }    
    # logging.info(config)
    return func.HttpResponse(
            json.dumps(get_scenarios_redis()),
            mimetype="application/json",
            status_code=200
            )


@app.route(route="check_training_status")
def check_training_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Checking Training Status')
    training_id = req.params.get('training_id')
    token = req.params.get('TOKEN')
    if training_id:
        training=get_training(training_id)
        if training['status']=="succeeded":
            update_model_training(training,token)
        return func.HttpResponse(
            json.dumps(training),
            mimetype="application/json",
            status_code=200
            )
    else:
        return func.HttpResponse(
            json.dumps({"error":True,"message":"missing training_id in query"}),
            mimetype="application/json",
            status_code=200
        )
      
    
@app.route(route="create_model")
def create_model(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Creating New Model')
    req_body={}
    try:
        req_body = req.get_json()
        logging.info("TOKEN {}".format(req_body.get("TOKEN")))
        logging.info("url {}".format(req_body['url']))
        logging.info("display_name {}".format(req_body['display_name']))
        logging.info("description {}".format(req_body['description']))
        training = create_model_repl(TOKEN=req_body['TOKEN'],zip_url=req_body['url'])
        
        if(training):   
            create_model_redis({"model":"itsmeravitejak/"+req_body['TOKEN'],                 
                "token":req_body['TOKEN'],
                "display_name":req_body['display_name'],
                "description":req_body['description'],
                "training_id":training.id
                })
            return func.HttpResponse(
            json.dumps({"training_id":training.id}),
            mimetype="application/json",
            status_code=200
            )
        else:
            return func.HttpResponse(
            json.dumps({"error":True}),
            mimetype="application/json",
            status_code=500
            )

    except ValueError:
        pass

    logging.info(str(req_body))
    return func.HttpResponse(
            json.dumps({"error":True}),
            mimetype="application/json",
            status_code=500
            )


@app.route(route="gen_image")
def gen_image(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Image Generate Request Generated')

    name = req.params.get('name')
    model= req.params.get('model')
    _prompt=req.params.get('prompt')
    # A stylish rooftop bar in Bangkok at night, overlooking a dazzling city skyline with neon lights and skyscrapers. {0} enjoys cocktails in a modern, luxurious setting with golden ambient lighting. The city below is a sea of lights, and the scene feels exclusive and elegant. The sky is deep blue with a hint of stars, and the mood is sophisticated yet lively. The bar’s glass railing reflects the glow of the city, adding a sleek and modern aesthetic
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    
    if name and model and _prompt:
        prompt=_prompt.format(name)
        output = replicate.run(
            model,
            input={
                "model": "dev",
                "prompt": prompt,
                "go_fast": False,
                "lora_scale": 1,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "guidance_scale": 3,
                "output_quality": 80,
                "prompt_strength": 0.8,
                "extra_lora_scale": 1,
                "num_inference_steps": 28
            }
        )
        urls=[]
        for i in output:
            urls.append(i.url)

        return func.HttpResponse(
            json.dumps({"status":True,"urls":urls}),
            mimetype="application/json",
            status_code=200
            )
    else:
        return func.HttpResponse(
            json.dumps({"status":False,"message":"Send both name and the model params"}),
            mimetype="application/json",
            status_code=500
        )