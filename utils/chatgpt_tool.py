from openai import OpenAI
import time

api_key = "REPLACE YOUR APIKEY"
client = OpenAI(api_key=api_key)


def get_chat_result(messages, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        # print(response)
        return 0, "", response.choices[0].message.content
    except Exception as e:
        return 99, str(e), str(e)


if __name__ == "__main__":
    prompt = """你是一个语文老师，擅长寓言阅读理解。请基于给定的故事，从4个候选答案中选择最恰当的、最符合故事情节的寓意。
    故事标题是：蝙蝠、荆棘与水鸟
    故事内容是：蝙蝠、荆棘、水鸟商定，合伙经商为生。于是蝙蝠借来钱作为资金，荆棘带来了他自己的衣服，水鸟带着赤铜，然后，他们装好货，扬帆远航。在海上不巧碰到了强大的风暴，船翻了，所有的货物全沉没了。幸运的是，他们被海浪冲到岸上，未被淹死。从此以后，水鸟总是站到水中，想把丢失的赤铜找回来；蝙蝠怕见债主，白天不敢出来，只有夜间才出来觅食；荆棘则到处寻找衣服，总把过路人的衣服抓住，看是否是自己的。
    问题是：下列哪个选项最符合故事说明的寓意？
    选项是：A.合作伙伴的选择至关重要，要确保大家相互信任，而且有共同目标。 B.吃一堑长一智。 C.不要贪图一时的利益而忽略了可能的风险和后果。 D.人生充满变数，需要学会适应和调整计划。

    直接给出答案，输出A、B、C、D的序号，不要输出多余的内容。在输出答案前，请再次确认答案是否正确。
    """
    messages = [
        {"role": "system", "content": "你是一个百科全书."},
        {"role": "user", "content": prompt},
    ]
    start_time = time.time()
    model = "gpt-4-turbo"
    ret_code, err_msg, result = get_chat_result(messages, model)
    end_time = time.time()
    print(result)
    print("time cost: {} seconds".format(end_time - start_time))
