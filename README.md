 - Deploy the Repo to Azure functions  
 - Add Following environment variables
 
 
    

    > {
    >       "name": "REDIS_HOST",
    >       "value": "<hosturl>",
    >       "slotSetting": false
    >     },
    >     {
    >       "name": "REDIS_PASS",
    >       "value": "<password>",
    >       "slotSetting": false
    >     },
    >     {
    >       "name": "REDIS_PORT",
    >       "value": "6379",
    >       "slotSetting": false
    >     },
    >     {
    >       "name": "REDIS_SSL",
    >       "value": "True",
    >       "slotSetting": false
    >     },
    >     {
    >       "name": "REPLICATE_API_TOKEN",
    >       "value": "<replicate_token>",
    >       "slotSetting": false
    >     }
