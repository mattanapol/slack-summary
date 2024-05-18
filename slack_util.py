from slack_sdk import WebClient

class SlackUtil:
    def __init__(self, token):
        self.client = WebClient(token=token)
        self.user_names = {}
        my_user = self.client.auth_test()
        self.user_names[my_user["user_id"]] = "Me"

    def get_user_name_by_id(self, user_id: str) -> str:
        # check cache first
        # if not found, call the API
        if user_id in self.user_names:
            return self.user_names[user_id]

        user_info_response = self.client.users_info(user=user_id)
        self.user_names[user_id] = user_info_response["user"]["profile"]["display_name_normalized"]
        return self.user_names[user_id]

    def replace_user_mentions(self, text: str) -> str:
        # Replace user mentions
        while True:
            start = text.find("<@")
            if start == -1:
                break
            end = text.find(">", start)
            user_id = text[start + 2:end]
            user_name = self.get_user_name_by_id(user_id)
            text = text[:start] + "<" + user_name + ">" + text[end + 1:]
        return text
    
    def replace_code_blocks(self, text: str) -> str:
        # Replace code blocks
        while True:
            start = text.find("```")
            if start == -1 or start + 3 >= len(text):
                break
            end = text.find("```", start + 3)
            text = text[:start] + "<code block>" + text[end + 3:]
        return text
    
    def get_text_from_message(self, message) -> str:
        text = message["text"]
        if "files" in message:
            text += "[with file: "
            text += ", ".join([file["name"] for file in message["files"]])
            text += "]"
        return text
    
    def to_chat_entry(self, message) -> str:
        text = self.get_text_from_message(message)
        text = self.replace_user_mentions(text)
        text = self.replace_code_blocks(text)
        return "{}: {}".format(self.get_user_name_by_id(message["user"]), text)