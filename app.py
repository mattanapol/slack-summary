import streamlit as st
from config import load_conf
from langchain_core.prompts import ChatPromptTemplate
from slack_util import SlackUtil

config = load_conf("./config.yaml")
def get_chat_history(
        channel_id: str,
        limit: int):

    slack = SlackUtil(token=config.slack.token)

    conversation_history = slack.client.conversations_history(
        channel=channel_id,
        limit=limit
    )
    chat_history = []
    for message in reversed(conversation_history["messages"]):
        chat = slack.to_chat_entry(message)
        chat_history.append(chat)
    return chat_history

def summarize_action_items(chat_history):
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(api_key=config.open_ai.api_key,
                    model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_messages([
        ("system",
        """
        I'd like you to analyze the following conversation and identify all my pending action items that not resolved and still require my attention.
        Please format these action items as a bulleted list with clear and concise descriptions of what needs to be done.
        """),
        ("user",
        """
        {conversation}
        """),
    ])
    from langchain_core.output_parsers import StrOutputParser
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    output = chain.invoke({"conversation": chat_history})
    return output

st.title('Slack action items summarizer')
selected_channel_list = st.sidebar.multiselect("Select channel", 
                                               config.slack.channels, 
                                               default=config.slack.channels)
if st.button("Get chat history", type="primary"):
    for selected_channel in selected_channel_list:
        data_load_state = st.text('Loading chat data...')
        chat_history = get_chat_history(channel_id=config.slack.channels[selected_channel], limit=10)
        data_load_state.text('Summarizing action items...')
        action_items = summarize_action_items(chat_history)
        data_load_state.text("{channel} Action Items:".format(channel=selected_channel))
        st.write(action_items)


    