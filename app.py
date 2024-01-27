import io
import requests
import streamlit as st
from PIL import Image

h_api = "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"
def query_stable_diffusion_model(payload, headers, model_id):
    API_URL = f'https://api-inference.huggingface.co/models/{model_id}'
    response = requests.post(API_URL, headers=headers, json=payload)
    print(response.content)
    return response.content
    


st.title('💬 Chatbot - Text2Image')
st.caption('🚀 A chatbot powered by Stable Diffusion models')

model_id = st.selectbox('Select a model', ['stabilityai/stable-diffusion-xl-base-1.0','stabilityai/stable-diffusion-2-1'])

if model_id == 'stable_diffusion/stable_diffusion_xl_base_1_0':
    st.write('Slower')
else:
    st.write('Faster')

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {'role': 'assistant', 'content': 'What kind of image that I need to draw? (example: cat wearing goggles)'}
    ]
    
for message in st.session_state.messages:
    st.chat_message(message['role']).write(message['content'])
    if 'image' in message:
        st.chat_message('assistant').image(message['image'], caption=message['prompt'], use_column_width=True)

if prompt := st.chat_input():
    if not h_api:
        st.info('Please add your Hugging Face Token to continue.')
        st.stop()
    
    # Input prompt
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    st.chat_message('user').write(prompt)
    
    # Query Stable Diffusion
    headers = {'Authorization': f'Bearer {h_api}'}
    
    image_bytes = query_stable_diffusion_model({
        'inputs': prompt,
    }, headers, model_id)
    print(image_bytes)
    # Return Image
    image = image = Image.open(io.BytesIO(image_bytes))
    msg = f'here is your image related to "{prompt}"'

    # Show Result
    st.session_state.messages.append({'role': 'assistant', 'content': msg, 'prompt': prompt, 'image': image})
    st.chat_message('assistant').write(msg)
    st.chat_message('assistant').image(image, caption=prompt, use_column_width=True)