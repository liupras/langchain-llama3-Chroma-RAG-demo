#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author  : 刘立军
# @time    : 2024-10-9
# @function: langchian官方教程：callbacks 测试
# @version : V0.5


from langchain.callbacks import StdOutCallbackHandler
from langchain.chains import LLMChain
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate

handler = StdOutCallbackHandler()
llm = OllamaLLM(model="llama3.1")
prompt = PromptTemplate.from_template("1 + {number} = ")

# Constructor callback: First, let's explicitly set the StdOutCallbackHandler when initializing our chain
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
chain.run(number=2)

# Use verbose flag: Then, let's use the `verbose` flag to achieve the same result
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
chain.run(number=2)

# Request callbacks: Finally, let's use the request `callbacks` to achieve the same result
chain = LLMChain(llm=llm, prompt=prompt)
chain.run(number=2, callbacks=[handler])