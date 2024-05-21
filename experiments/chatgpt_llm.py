import json
import time

from utils import chatgpt_tool


CR_prompt = """你是一个语文老师，擅长寓言阅读理解。请根据故事内容以及涉及到的常识知识进行推理，给出最合理的答案。
故事标题是：{}
故事内容是：{}
问题是：{}
选项是：{}

直接给出答案，输出A、B、C、D的序号，不要输出多余的内容。在输出答案前，请再次确认答案是否正确。
"""

MU_prompt = """你是一个语文老师，擅长寓言阅读理解。请基于给定的故事，从4个候选答案中选择最恰当的、最符合故事情节的寓意。
故事标题是：{}
故事内容是：{}
问题是：{}
选项是：{}

直接给出答案，输出A、B、C、D的序号，不要输出多余的内容。在输出答案前，请再次确认答案是否正确。
"""


def llm_call(input_file, output_file, prompt_template, start_idx, record_count):
    """
        ipnut_file: dev/test file
        output_file: the llm intermediate result
        prompt_template: prompt template
        start_idx: start index
        record_count: record count
    """
    with open(input_file, encoding="utf-8") as input_data:
        json_content = json.load(input_data)
        json_content = json_content[start_idx: record_count]
        for story in json_content:
            story_id, story_title, story_content, question, options, answer = story["id"], story["title"], story[
                "story"], story["question"], story["options"], story["answer"]
            prompt = prompt_template.format(story_title, story_content, question, " ".join(options))
            print(prompt)
            messages = [
                {"role": "system", "content": prompt},
            ]
            start_time = time.time()
            ret_code, err_msg, response = chatgpt_tool.get_chat_result(messages, "gpt-4-turbo")
            end_time = time.time()
            print(response)
            print("time cost: {} seconds".format(end_time - start_time))
            story["llm_result"] = response
            story["ret_code"] = ret_code
            story["err_msg"] = err_msg
            with open(output_file, "w", encoding="utf-8") as output_data:
                json.dump(json_content, output_data, ensure_ascii=False, indent=2)


def post_process(input_file, output_file):
    tag_list = ["A", "B", "C", "D"]
    with open(input_file, encoding="utf-8") as input_data:
        json_content = json.load(input_data)
        for block in json_content:
            ret_code = block["ret_code"]
            llm_result = block["llm_result"].strip()
            if ret_code == 0:
                if llm_result[0] in tag_list:
                    block["answer"] = llm_result[0]
                else:
                    print(ret_code, block["id"], llm_result)
                    for char in llm_result:
                        if char in tag_list:
                            block["answer"] = char
                            break
                    # default set A
                    if block["answer"] == "":
                        block["answer"] = "A"
            else:
                print(ret_code, block["id"], llm_result)
                # default set A
                block["answer"] = "A"

        with open(output_file, "w", encoding="utf-8") as output_data:
            json.dump(json_content, output_data, indent=2, ensure_ascii=False)


if __name__ == "__main__":

    # test CR set:
    test_cr_file = "../contest_data/test_CRMUS_CR_public.json"
    test_cr_llm_output = "../contest_data/test_cr_chatgpt_raw.json"
    llm_call(test_cr_file, test_cr_llm_output, CR_prompt, 0, 1692)
    test_cr_final_output = "../contest_data/test_cr_chatgpt_final.json"
    post_process(test_cr_llm_output, test_cr_final_output)

    # test MU set:
    test_mu_file = "../contest_data/test_CRMUS_MU_public.json"
    test_mu_llm_output = "../contest_data/test_mu_chatgpt_raw.json"
    llm_call(test_mu_file, test_mu_llm_output, MU_prompt, 0, 1056)
    test_mu_final_output = "../contest_data/test_mu_chatgpt_final.json"
    post_process(test_mu_llm_output, test_mu_final_output)



