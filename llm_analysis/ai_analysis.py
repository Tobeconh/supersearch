from zhipuai import ZhipuAI
def ai_emotion_analsize():
    client =ZhipuAI(api_key='c7d8837d7596477e9a457cf38f6d0463.8uGIVHQ4SiCGNhfS')
    response = client.chat.completions.create(
        model='glm-4-air-250414',
        messages=[
            {'role': 'user', 'content': """
            简单讲述对先进无线的理解，150字以内
            """},

        ],

    )
    return response.choices[0].message.content

print(ai_emotion_analsize())