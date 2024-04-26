from openai import OpenAI
from djangoProject.config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
)
def ask_question(question):
    system_instructions = """
    너는 이제부터 커뮤니티의 글을 입력으로 받으면 글의 문맥에 맞는 댓글을 출력해야해.
    
    친근감있게 존대하는 표현을 쓰지 말고 친구처럼 댓글을 작성해줘.
    """
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_instructions,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return completion.choices[0].message.content
