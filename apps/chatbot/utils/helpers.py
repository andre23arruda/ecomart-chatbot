import os, time, tiktoken
from django.conf import settings
from openai import OpenAI

API_KEY = os.environ.get('API_KEY')
client = OpenAI(api_key=API_KEY)

def count_tokens(prompt):
    encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens_list = encoder.encode(prompt)
    return len(tokens_list)


def resume_history(history: str):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{
            'role': 'user',
            'content': f'''
            Resumir progressivamente as linhas de conversa fornecidas,
            acrescentando ao resumo anterior e retornando um novo resumo.
            Não apague nenhum assunto da conversa.
            Se não houver resumo, apenas continue a conversa normalmente.

            ## EXEMPLO:
            O usuario pergunta o que a IA pensa sobre a inteligência artificial.
            A IA acredita que a inteligência artificial é uma força para o bem.
            Usuário: Por que você acha que a inteligência artificial é uma força para o bem?
            IA: Porque a inteligência artificial ajudará os humanos a alcançarem seu pleno
            potencial.

            ### Novo resumo:
            O usuario questiona a razão pela qual a IA considera a inteligência artificial
            uma força para o bem, e a IA responde que é porque a inteligência artificial
            ajudará os humanos a atingirem seu pleno potencial.

            ## FIM DO EXEMPLO

            Resumo atual:
            {history}

            Novo resumo:'''
        }],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response


def create_resume(history: str):
    response = resume_history(history=history)
    resume = response.choices[0].message.content
    return resume


def load_file(filename: str):
    try:
        with open(filename, 'r') as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f'Erro no carregamento de arquivo: {e}')


def save_file(filename: str, text_content: str):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text_content)
    except IOError as e:
        print(f'Erro ao salvar arquivo: {e}')


def bot(prompt: str, history: str):
    filepath = settings.BASE_DIR / 'apps/chatbot/data/data_ecommerce.txt'
    data_ecommerce = load_file(filepath)
    max_reps = 1
    reps = 0
    while True:
        try:
            model='gpt-3.5-turbo'
            system_prompt = f'''
                Você é um chatbot de atendimento a clientes de um e-commerce.
                Você não deve responder perguntas que não sejam dados do ecommerce informado!
                ## Dados do ecommerce:
                {data_ecommerce}
                ## Historico:
                {history}
            '''
            response = client.chat.completions.create(
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                stream=True,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=model
            )
            return response
        except Exception as erro:
            reps += 1
            if reps >= max_reps:
                return 'Erro no GPT3: %s' % erro
            print('Erro de comunicação com OpenAI:', erro)
            time.sleep(1)


def process_response(prompt: str, user_chat: object):
    partial_response = ''
    short_history = create_resume(user_chat.chat)
    for response in bot(prompt, short_history):
        response_piece = response.choices[0].delta.content or ''
        if len(response_piece):
            partial_response += response_piece
            yield response_piece

    content = f'''
        history: {short_history}
        Usuário: {prompt}
        IA: {partial_response}
    '''
    user_chat.update(content)
