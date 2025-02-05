import sys
import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.llms import HuggingFaceEndpoint
# Assuming secret_key.py is in the 'keys' directory relative to your notebook
key_dir = os.path.join(os.getcwd(), 'keys')
sys.path.append(key_dir)

from  secret_key import huggingface_api
import os
os.environ['api'] = huggingface_api

llm3=HuggingFaceEndpoint(endpoint_url="https://api-inference.huggingface.co/models/openai-community/gpt2",  # Hugging Face model endpoint
    huggingfacehub_api_token=os.environ['api'],                  # Your Hugging Face API token
    temperature=0.7,
     model_kwargs={"max_length": 256} ,
                         max_new_tokens=200
                         )




def generate_restaurant_name_and_items(cuisine):
    #chain 1: restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="i want to open a restaurant for {cuisine} food. Suggest concise name for this."
    )
    name_chain = LLMChain(llm=llm3, prompt=prompt_template_name, output_key="restaurant_name")

    #chain 2: menu items
    prompt_template_items = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest some menu items for {restaurant_name}."
    )
    food_items_chain = LLMChain(llm=llm3, prompt=prompt_template_items, output_key="menu_items")
    chain = SequentialChain(chains=[name_chain, food_items_chain], input_variables=["cuisine"],
                            output_variables=["restaurant_name", "menu_items"])
    response = chain({'cuisine': cuisine})
    return response

if __name__ == '__main__':
    print(generate_restaurant_name_and_items(cuisine="Indian"))