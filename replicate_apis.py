import replicate

def get_training(training_id):
    training=replicate.trainings.get(training_id)
    return {"status":training.status,"logs":training.logs,"output":training.output}

def create_model_repl(TOKEN:str,zip_url:str):
    model=False
    model = replicate.models.create(
        owner="itsmeravitejak",
        name=TOKEN,
        visibility="private",
        hardware="gpu-a100-large"
    )

    if(model):
        training = replicate.trainings.create(
        # You need to create a model on Replicate that will be the destination for the trained version.
        destination="itsmeravitejak/"+TOKEN,
        version="ostris/flux-dev-lora-trainer:b6af14222e6bd9be257cbc1ea4afda3cd0503e1133083b9d1de0364d8568e6ef",
        input={
            "steps": 1000,
            "lora_rank": 16,
            "optimizer": "adamw8bit",
            "batch_size": 1,
            "resolution": "512,768,1024",
            "autocaption": True,
            "input_images": zip_url,
            "trigger_word": TOKEN,
            "learning_rate": 0.0004,
            "wandb_project": "flux_train_replicate",
            "wandb_save_interval": 100,
            "caption_dropout_rate": 0.05,
            "cache_latents_to_disk": False,
            "wandb_sample_interval": 100,
            "gradient_checkpointing": False
        })
        if(training):
            return training
        return False
    else:
        return False