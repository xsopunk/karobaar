from langchain_core.messages import HumanMessage
from core.workflow import build_workflow

if __name__ == "__main__":
    app = build_workflow()
    messages = []
    print("🤖 KarobaarAI Agent ready. Type 'quit' to exit.\n")

    while True:
        user = input("👤 You: ")
        if user.lower() in ["quit", "exit"]:
            break

        messages.append(HumanMessage(content=user))
        result = app.invoke({"messages": messages})
        ai_response = result["messages"][-1]
        text = ai_response.content if isinstance(ai_response.content, str) else str(ai_response.content)
        print(f"🤖 {text}\n")
        messages.append(ai_response)
