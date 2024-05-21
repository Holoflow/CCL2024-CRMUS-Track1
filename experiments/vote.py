"""
    script used to vote 3 llm results
"""
import json
from collections import Counter
import time
from utils import chatgpt_tool


CR_confirm_prompt = """你是一个语文老师，擅长寓言阅读理解。请根据故事内容以及涉及到的常识知识进行推理，给出最合理的答案。
故事标题是：{}
故事内容是：{}
问题是：{}
选项是：{}

目前已知答案在{}几个选项中，给出最终的答案。
输出{}的序号即可，不要输出多余的内容。在输出答案前，请再次确认答案是否正确。
"""


MU_confirm_prompt = """你是一个语文老师，擅长寓言阅读理解。请基于给定的故事，从4个候选答案中选择最恰当的、最符合故事情节的寓意。
故事标题是：{}
故事内容是：{}
问题是：{}
选项是：{}

目前已知答案在{}几个选项中，给出最终的答案。
输出{}的序号即可，不要输出多余的内容。在输出答案前，请再次确认答案是否正确。
"""


def find_most_common(arr):
    """
        func to get the max frequency term
    """
    counter = Counter(arr)
    return counter.most_common(1)[0][0]


def post_process(ret_code, llm_result):
    tag_list = ["A", "B", "C", "D"]
    llm_result = llm_result.strip()
    if ret_code == 0:
        if llm_result[0] in tag_list:
            return llm_result[0]
        else:
            for char in llm_result:
                if char in tag_list:
                    return char
            # default set A
            return "A"
    else: # set default answer to be A
        return "A"


def vote_cr():
    submit_cr = json.load(open("../contest_data/test_CRMUS_CR_public.json", encoding="utf-8"))
    chatgpt_cr = json.load(open("../contest_data/test_cr_chatgpt_final.json", encoding="utf-8"))
    wenxin_cr = json.load(open("../contest_data/test_cr_wenxin_final.json", encoding="utf-8"))
    tongyi_cr = json.load(open("../contest_data/test_cr_tongyi_final.json", encoding="utf-8"))

    print("Processing CR: ")
    for idx in range(len(submit_cr)):
        id = submit_cr[idx]["id"]
        title = submit_cr[idx]["title"]
        story = submit_cr[idx]["story"]
        question = submit_cr[idx]["question"]
        options = submit_cr[idx]["options"]

        confirm_flag = False
        selected_answer = list()

        chatgpt_answer = chatgpt_cr[idx]["answer"]
        tongyi_answer = tongyi_cr[idx]["answer"]
        wenxin_answer = wenxin_cr[idx]["answer"]
        # print(chatgpt_answer, tongyi_answer, wenxin_answer)
        answer_set = set()
        answer_set.add(chatgpt_answer)
        answer_set.add(wenxin_answer)
        answer_set.add(tongyi_answer)

        if len(answer_set) == 1:
            submit_cr[idx]["answer"] = chatgpt_answer
        if len(answer_set) == 2:
            vote_answer = find_most_common([chatgpt_answer, wenxin_answer, tongyi_answer])
            submit_cr[idx]["answer"] = vote_answer
            if vote_answer != chatgpt_answer:
                confirm_flag = True
                selected_answer = [chatgpt_answer, vote_answer]
        if len(answer_set) == 3:
            confirm_flag = True
            selected_answer = [chatgpt_answer, wenxin_answer, tongyi_answer]

        # confirm step using Chatgpt LLM:
        if confirm_flag:
            selected_answer.sort()
            prompt = CR_confirm_prompt.format(title, story, question, " ".join(options), "、".join(selected_answer), "、".join(selected_answer))
            print(prompt)
            start_time = time.time()
            messages = [
                {"role": "system", "content": prompt},
            ]
            ret_code, err_msg, response = chatgpt_tool.get_chat_result(messages, "gpt-4-turbo")
            end_time = time.time()
            print(response)
            print("time cost: {} seconds".format(end_time - start_time))
            confirm_answer = post_process(ret_code, response)
            submit_cr[idx]["answer"] = confirm_answer

    with open("../contest_data/test_CRMUS_CR.json", "w", encoding="utf-8") as output_data:
        json.dump(submit_cr, output_data, indent=2, ensure_ascii=False)


def vote_mu():
    submit_mu = json.load(open("../contest_data/test_CRMUS_MU_public.json", encoding="utf-8"))
    chatgpt_mu = json.load(open("../contest_data/test_mu_chatgpt_final.json", encoding="utf-8"))
    wenxin_mu = json.load(open("../contest_data/test_mu_wenxin_final.json", encoding="utf-8"))
    tongyi_mu = json.load(open("../contest_data/test_mu_tongyi_final.json", encoding="utf-8"))

    print("Processing MU: ")
    for idx in range(len(submit_mu)):
        id = submit_mu[idx]["id"]
        title = submit_mu[idx]["title"]
        story = submit_mu[idx]["story"]
        question = submit_mu[idx]["question"]
        options = submit_mu[idx]["options"]

        confirm_flag = False
        selected_answer = list()

        chatgpt_answer = chatgpt_mu[idx]["answer"]
        tongyi_answer = tongyi_mu[idx]["answer"]
        wenxin_answer = wenxin_mu[idx]["answer"]
        # print(chatgpt_answer, tongyi_answer, wenxin_answer)
        answer_set = set()
        answer_set.add(chatgpt_answer)
        answer_set.add(wenxin_answer)
        answer_set.add(tongyi_answer)

        if len(answer_set) == 1:
            submit_mu[idx]["answer"] = chatgpt_answer
        if len(answer_set) == 2:
            vote_answer = find_most_common([chatgpt_answer, wenxin_answer, tongyi_answer])
            submit_mu[idx]["answer"] = vote_answer
            if vote_answer != chatgpt_answer:
                confirm_flag = True
                selected_answer = [chatgpt_answer, wenxin_answer]
        if len(answer_set) == 3:
            confirm_flag = True
            selected_answer = [chatgpt_answer, wenxin_answer, tongyi_answer]

        # confirm step using ChatGPT LLM:
        if confirm_flag:
            selected_answer.sort()
            prompt = MU_confirm_prompt.format(title, story, question, " ".join(options), "、".join(selected_answer), "、".join(selected_answer))
            print(prompt)
            start_time = time.time()
            messages = [
                {"role": "system", "content": prompt},
            ]
            ret_code, err_msg, response = chatgpt_tool.get_chat_result(messages, "gpt-4-turbo")
            end_time = time.time()
            print(response)
            print("time cost: {} seconds".format(end_time - start_time))
            confirm_answer = post_process(ret_code, response)
            submit_mu[idx]["answer"] = confirm_answer

    with open("../contest_data/test_CRMUS_MU.json", "w", encoding="utf-8") as output_data:
        json.dump(submit_mu, output_data, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    vote_cr()
    vote_mu()
