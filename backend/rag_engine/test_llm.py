
from backend.rag_engine.llm_client import llm, prompt


user_input = prompt.format(
    text="What is Docker? Explain in simple words."
)


response = llm.invoke(user_input)


print("\n========== LLM RESPONSE ==========")
print(response)
