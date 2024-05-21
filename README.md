# Mainfest:
* contest_data: 存放比赛数据以及代码生成的结果 
* experiments: 本次比赛的实验代码
  * chatgpt_llm: ChatGPT跑实验
  * wenxin_llm: 文心一言跑实验
  * tongyi_llm: 通义千问跑实验，注意通义调用API要加限速处理，代码中已加了sleep操作。
  * vote: 基于3家LLM的结果，进行投票和二次提示词确认最终结果
* utils: 封装的LLM API调用方法类:
  * chatgpt_tool: ChatGPT
  * wenxin_tool: 百度文心一言
  * tongyi_tool: 通义千问 
* requirements.txt: 依赖的Python包

# 如何运行代码：
* 本代码在PyCharm IDE中运行，如果是命令行运行，可能需要修改下文件的读取路径（改成绝对路径）
* 第一步，修改utils中封装的LLM中的apikey 、secrec key之类的信息，替换为自己的key
* 第二步，分别执行chatgpt_llm.py, wenxin_llm.py和tongyi_llm.py，得到3个LLM的运行结果，这一步的结果会写入到contest_data目录
* 第三步，执行vote.py，这一步的结果会写入到contest_data目录，为最终的提交结果。
