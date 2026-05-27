import os
from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL
)

messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
response = client.chat.completions.create(
    model=settings.DEEPSEEK_MODEL,
    messages=messages,
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},  # 注意逗号
)

reasoning_content = ""
content = ""

for chunk in response:
    if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
        reasoning_content += chunk.choices[0].delta.reasoning_content
    else:
        if chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content

# 将第一个问题的回答添加到消息历史中
# 注意：通常我们只添加最终的content，但这里按照代码添加了reasoning_content和content。
# 但是，DeepSeek API可能不接受reasoning_content字段，所以我们可能需要调整。
# 一种常见的做法是只添加content作为assistant的回复。
# 这里我们按照原代码的结构，但请注意，如果API不支持，可能会出错。
messages.append({"role": "assistant", "content": content})

# 第二个问题
messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
response = client.chat.completions.create(
    model=settings.DEEPSEEK_MODEL,
    messages=messages,
    stream=True,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},  # 注意逗号
)

reasoning_content2 = ""
content2 = ""

for chunk in response:
    if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
        reasoning_content2 += chunk.choices[0].delta.reasoning_content
    else:
        if chunk.choices[0].delta.content:
            content2 += chunk.choices[0].delta.content

print("First question reasoning:", reasoning_content)
print("First question answer:", content)
print("Second question reasoning:", reasoning_content2)
print("Second question answer:", content2)