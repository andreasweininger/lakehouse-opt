def load_conf():
    import os
    from dotenv import load_dotenv

    load_dotenv(home+'/utils/config.env')

    # Load config from environment
    config = {
        "api_key" : os.getenv("API_KEY", None),
        "ibm_cloud_url" : os.getenv("IBM_CLOUD_URL", None),
        "project_id" : os.getenv("PROJECT_ID", None),
        "space_id" :  os.getenv("SPACE_ID", None),
        "host" : os.getenv("LH_HOST_NAME", "localhost"),
        "user" : os.getenv("LH_USER", "ibmlhadmin"),
        "password" : os.getenv("LH_PW", "password"),
        "lh_port": os.getenv("LH_PORT", "8443"),
        "lh_cert": os.getenv("LH_CERT", "/wxd-install/ibm-lh-dev/localstorage/volumes/infra/tls/cert.crt"),
        "lh_schema": os.getenv("LH_SCHEMA", "tiny"),
        "lh_catalog": os.getenv("LH_CATALOG", "tpch"),
        "milvus_port": os.getenv("MILVUS_PORT", "19530"),
        "minio_access_key": os.getenv("MINIO_ACCESS_KEY", None),
        "minio_secret_key": os.getenv("MINIO_SECRET_KEY", None),
        "default_query": os.getenv("DEFAULT_QUERY", "Who is Jon Fosse?")
    }

    return(config)

def connect_wxd(config):

    import ssl
    import urllib3
    import os
    from sqlalchemy import create_engine
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable https warning

    quick_engine = create_engine(
        f'presto://{config["user"]}:{config["password"]}@{config["host"]}:{config["lh_port"]}/{config["lh_catalog"]}/{config["lh_schema"]}',
        connect_args={
            'protocol': 'https', 
            'requests_kwargs': {'verify': ssl.CERT_NONE }
            }
        )

    return quick_engine

def get_token(conf):

    from ibm_cloud_sdk_core import IAMTokenManager

    access_token = IAMTokenManager(
        apikey = api_key,
        url = "https://iam.cloud.ibm.com/identity/token"
    ).get_token()

    return access_token

def load_model(conf, model_id):
    #        model_id='meta-llama/llama-2-70b-chat'
    #        model_id='mistralai/mixtral-8x7b-instruct-v01'

    logger.info(f"load_model> model_id: {model_id}")

    from ibm_watsonx_ai.foundation_models import Model
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

    creds = {
        "url": conf["ibm_cloud_url"],
        "apikey": conf["api_key"] 
    }

    # Model Parameters
    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.TEMPERATURE: 0,
    }

    try:
        model = Model(model_id=model_id, 
            params=params, credentials=creds, 
            project_id=conf["project_id"]
        )
        print(f"Model {model_id} loaded")
        return model
    except Exception as e:
        logger.error(f"load_model> error loading model: {str(e)}")
        print(f"load_model> error loading model: {str(e)}")

    return None

def load_embedding_model(conf, model_id):

    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import Embeddings
    from ibm_watsonx_ai.metanames import EmbedTextParamsMetaNames as EmbedParams
    from ibm_watsonx_ai.foundation_models.utils.enums import EmbeddingTypes

    logger.info(f"load_embedding_model> model_id: {model_id}")

    creds = {
        "url": conf["ibm_cloud_url"],
        "apikey": conf["api_key"] 
    }

    embed_params = {
        EmbedParams.TRUNCATE_INPUT_TOKENS: 512,
        EmbedParams.RETURN_OPTIONS: {
            'input_text': True
            }
    }

    try:

        if model_id == '':
            print("model_ids available are:")
            embeddingList = client.foundation_models.EmbeddingModels
            print(embeddingList.show())
            return None
 
        embedding = Embeddings(
            model_id=model_id,
            params=embed_params,
            credentials=creds,
            project_id=conf["project_id"]
            )
        return embedding

    except Exception as e:
        logger.error(f"load_embedding_model> error loading model: {str(e)}")
        print(f"load_embedding_model> error loading model: {str(e)}")

        print("Maybe an incorect model_id has been given. model_ids available are:")
        embeddingList = client.foundation_models.EmbeddingModels
        print(embeddingList.show())

    return None

def vectorize (embedding, text):

    logger.info(f"vectorize> {text}")

    try: 

        vector = embedding.embed_query(text=text)
        return vector

    except Exception as e:
        logger.error(f"vectorize> error generating vector: {str(e)}")
        print(f"vectorize> error generating vector: {str(e)}")

    return None

def vectorize_list (embedding, text):

    logger.info(f"vectorize_list> {text}")

    try: 

        vector = embedding.embed_documents(texts=text)
        return vector

    except Exception as e:
        logger.error(f"vectorize_list> error generating vector: {str(e)}")
        print(f"vectorize_list> error generating vector: {str(e)}")

    return None

def load_model_deployment(conf, model_id):

    logger.info(f"load_model_deployment> model_id: {model_id}")

    from ibm_watsonx_ai import APIClient, Credentials
    global client

    creds = {
        "url": conf["ibm_cloud_url"],
        "apikey": conf["api_key"] 
    }

    try:

        if client == None:
            client=APIClient(creds, space_id=conf['space_id'])

        deploymentList = client.deployments.get_details()

        deployedPrompts = {}
        for deployment in deploymentList['resources']:
            deployedPrompts[deployment['entity']['name']] = {
                'name': deployment['entity']['name'], 
                'id': deployment['metadata']['id'] 
            }

        logger.info(f"load_model_deployment> Deployments: {deployedPrompts}")

        if model_id == '':
            print("model_ids available are:")
            for key in deployedPrompts:
                print("- ", key)
            return None
        else:
            deployment_id = deployedPrompts[model_id]

        return deployment_id

    except Exception as e:
        logger.error(f"load_model_deployment> error loading model: {str(e)}")
        print(f"load_model_deployment> error loading model: {str(e)}")

        print("Maybe an incorect model_id has been given. model_ids available are:")
        for key in deployedPrompts:
            print("- ", key)

    return None

def query_milvus(query, embedding, basic_collection, num_results=5):

    logger.info(f"query_milvus> {query} ({num_results})")

    # Vectorize query
    query_embeddings = vectorize_list(embedding, [query])

    # Search
    search_params = {
        "metric_type": "L2", 
        "params": {"nprobe": 5}
    }
    results = basic_collection.search(
        data=query_embeddings, 
        anns_field="vector", 
        param=search_params,
        limit=num_results,
        expr=None, 
        output_fields=['article_text'],
    )
    return results

def query_milvus_chunks(query, embedding, basic_collection, num_results=5):

    logger.info(f"query_milvus_chunks> {query} ({num_results})")
    
    results = query_milvus(query, embedding, basic_collection, num_results)

    relevant_chunks = []

    for hits in results:
        for hit in hits:
            relevant_chunks.append(hit.article_text)

    logger.info(f"query_milvus_chunks> {relevant_chunks}")

    return relevant_chunks

# Prompt LLM
def ask_llm(prompt, model):
    logger.info(f"ask_llm> Call model with {prompt}")
    response = model.generate_text(prompt)
    logger.info(f"ask_llm>\nQuestion: {prompt}\nResponse: {response}")
    return response

def ask_llm_prompt(prompt, deployment):

    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames

    try:
        response = client.deployments.generate_text(
            deployment_id=deployment['id'],
            params={
                GenTextParamsMetaNames.PROMPT_VARIABLES: {
                    "query": prompt
                }})

        return response

    except Exception as e:
        logger.error(f"ask_llm_prompt> error generating text: {str(e)}")
        print(f"ask_llm_prompt> error generating text: {str(e)}")
    
    return None

def set_prompt_template(new_template):
    from string import Template

    global prompt_template

    if new_template == '':
        prompt_template=Template("$context\n\nPlease answer a question using this text. "
          + "If the question is unanswerable, say \"unanswerable\"."
          + "\n\nQuestion: $question")
    else:
        prompt_template=Template(new_template)

    return(prompt_template)

def get_prompt_template():
    return prompt_template.template

def make_prompt(context, question):
    logger.info(f"make_prompt>\ncontext: {context}\nquestion: {question}")
    context = "\n\n".join(context)
    data={"context": context, "question": question}
    prompt = prompt_template.substitute(data)
    logger.info(f"make_prompt>\nprompt: {prompt}")
    return prompt

# Chunk data
def split_into_chunks(text, chunk_size):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def chunk_articles(articles, chunk_size):
    split_articles = {}
    for k,v in articles.items():
        split_articles[k] = split_into_chunks(v, chunk_size)

    chunks = []
    for article_title, article_chunks in split_articles.items():

        for i, chunk in enumerate(article_chunks):
            
                escaped_chunk = chunk.replace("'", "''").replace("%", "%%")
                chunks.append({'id': i+1, 'chunk': escaped_chunk, 'title': article_title})
            
        logger.info(f"chunk_articles> {article_title} DONE")

    return chunks

def run_gui(deployment, question):
    from ipywidgets import widgets

    text_input = widgets.Textarea(value=question, disabled=False)
    result_text = widgets.Textarea(value='', disabled=True)
    prompt_text = widgets.Textarea(value='', disabled=True)

    def on_click(b):
        logger.info(f"run_gui/on_click> You clicked the button! {text_input.value}")
        result_text.value = "asking LLM ..."
        prompt = text_input.value
        prompt_text.value = prompt
        result_text.value = ask_llm_prompt(prompt, deployment)

    button = widgets.Button(description='Ask LLM');
    button.on_click(on_click)

    input_box  = widgets.Box([widgets.Label('Your question!'), text_input, button, widgets.Label(f"model: {deployment['name']}")])
    result_box = widgets.Box([widgets.Label('Answer:'), result_text])
    prompt_box = widgets.Box([widgets.Label('Prompt:'), prompt_text])

    box = widgets.VBox(children=[input_box , prompt_box, result_box])

    result_text.layout.width = '100%'
    result_text.layout.height = '200px'
    prompt_text.layout.width = '100%'

    display(box)

def run_gui_with_context(deployment, question, context):
    from ipywidgets import widgets

    text_input = widgets.Textarea(value=question, disabled=False)
    result_text = widgets.Textarea(value='', disabled=True)
    prompt_text = widgets.Textarea(value='', disabled=True)
    context_text = widgets.Textarea(value=context, disabled=True)

    def on_click(b):
        logger.info(f"run_gui_with_context/on_click> You clicked the button! {text_input.value}")
        result_text.value = "asking LLM ..."
        prompt = make_prompt([context_text.value], text_input.value)
        prompt_text.value = prompt
        result_text.value = ask_llm_prompt(prompt, deployment)

    button = widgets.Button(description='Ask LLM');
    button.on_click(on_click)

    input_box  = widgets.Box([widgets.Label('Your question!'), text_input, button, widgets.Label(f"model: {deployment['name']}")])
    context_box = widgets.Box([widgets.Label('Context:'), context_text]) 
    result_box = widgets.Box([widgets.Label('Answer:'), result_text])
    prompt_box = widgets.Box([widgets.Label('Prompt:'), prompt_text])

    box = widgets.VBox(children=[context_box, input_box, prompt_box, result_box])

    context_text.layout.width = '100%'
    result_text.layout.width = '100%'
    result_text.layout.height = '200px'
    prompt_text.layout.width = '100%'

    display(box)

def run_gui_with_rag(deployment, embedding, basic_collection, question):
    from ipywidgets import widgets

    text_input = widgets.Textarea(value=question, disabled=False)
    result_text = widgets.Textarea(value='', disabled=True)
    prompt_text = widgets.Textarea(value='', disabled=True)
    context_text = widgets.Textarea(value='', disabled=True)

    def on_click(b):
        logger.info(f"run_gui_with_rag/on_click> You clicked the button! {text_input.value}")
        try:
            context = query_milvus_chunks(text_input.value, embedding, basic_collection)
            context_text.value = "\n\n".join(context)
            result_text.value = "asking LLM ..."
            prompt = make_prompt(context, text_input.value)
            prompt_text.value = prompt
            result_text.value = ask_llm_prompt(prompt, deployment)
        except Exception as e:
            logger.error(f"run_gui_with_rag/on_click> error: {str(e)}")
            print(f"run_gui_with_rag/on_click> error: {str(e)}")


#------------------------------------------------------------------------------------------------
# global 
#------------------------------------------------------------------------------------------------

    button = widgets.Button(description='Ask LLM');
    button.on_click(on_click)

    input_box  = widgets.Box([widgets.Label('Your question!'), text_input, button, widgets.Label(f"model: {deployment['name']}")])
    context_box = widgets.Box([widgets.Label('Context:'), context_text]) 
    result_box = widgets.Box([widgets.Label('Answer:'), result_text])
    prompt_box = widgets.Box([widgets.Label('Prompt:'), prompt_text])

    box = widgets.VBox(children=[input_box, context_box, prompt_box, result_box])

    context_text.layout.width = '100%'
    result_text.layout.width = '100%'
    result_text.layout.height = '200px'
    prompt_text.layout.width = '100%'

    display(box)

def write_log(level, text):
    if level == 'INFO':
        logger.info(text)
    elif level == 'ERROR':
        logger.error(text)
    else:
        logger.info(text)

# global variables
client = None
prompt_template = set_prompt_template('')

# initialize logging
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
cwd=os.getcwd()
home=cwd[:cwd.find('simple-rag')+11]
handler = logging.FileHandler(home+'logs/simple-rag.log', mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)