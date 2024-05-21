import requests
import json
import time

API_KEY = "REPLACE YOUR APIKEY"
SECRET_KEY = "REPLACE YOUR SECRET KEY"

"""
QPS/RPM/TPM: https://console.bce.baidu.com/qianfan/ais/console/onlineService
"""


def get_wenxin_result(prompt):
    """
        API: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t
        error code: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/tlmyncueh
    """
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "max_output_tokens": 2048
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def get_wenxin4_result(prompt):
    """
        API: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t
        error code: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/tlmyncueh
    """
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "max_output_tokens": 2048
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    if "error_code" in response_json:
        return response_json["error_code"], response_json["error_msg"], ""
    else:
        return 0, "", response_json["result"]


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    prompt = """你是一个语文老师，擅长寓言阅读理解。请基于给定的故事，从4个候选答案中选择最恰当的、最符合故事情节的寓意。
    故事标题是：蝙蝠、荆棘与水鸟
    故事内容是：蝙蝠、荆棘、水鸟商定，合伙经商为生。于是蝙蝠借来钱作为资金，荆棘带来了他自己的衣服，水鸟带着赤铜，然后，他们装好货，扬帆远航。在海上不巧碰到了强大的风暴，船翻了，所有的货物全沉没了。幸运的是，他们被海浪冲到岸上，未被淹死。从此以后，水鸟总是站到水中，想把丢失的赤铜找回来；蝙蝠怕见债主，白天不敢出来，只有夜间才出来觅食；荆棘则到处寻找衣服，总把过路人的衣服抓住，看是否是自己的。
    问题是：下列哪个选项最符合故事说明的寓意？
    选项是：A.合作伙伴的选择至关重要，要确保大家相互信任，而且有共同目标。 B.吃一堑长一智。 C.不要贪图一时的利益而忽略了可能的风险和后果。 D.人生充满变数，需要学会适应和调整计划。

    直接给出答案，输出A、B、C、D的序号，不要输出多余的内容。在输出答案前，请再次确认答案是否正确。
    """
    start_time = time.time()
    result = get_wenxin_result(prompt)
    print(type(result))
    end_time = time.time()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print('time cost: {} seconds'.format(end_time - start_time))
    print(result["result"])
