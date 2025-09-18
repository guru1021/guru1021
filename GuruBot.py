import os
from PIL import Image

# ---------------- Base Agent ----------------
class BaseAgent:
    def __init__(self, name="Agent"):
        self.name = name

    def process(self, message):
        raise NotImplementedError("Subclasses should implement this method.")


# ---------------- Text Agent ----------------
class TextAgent(BaseAgent):
    def __init__(self, name="TextAgent"):
        super().__init__(name)
        self.text_data = ""

    def load_file(self, file_name):
        # ✅ Works with just filename inside CodePad
        if not file_name.endswith(".txt"):
            return "Please upload a .txt file."
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as f:
                self.text_data = f.read().lower()
            return f"Text file '{file_name}' loaded successfully."
        else:
            return f"File '{file_name}' not found in workspace. Please import it into CodePad."

    def process(self, message):
        if not self.text_data:
            return "Please upload a text file first."
        keyword = message.lower()
        results = [line for line in self.text_data.splitlines() if keyword in line]
        return "\n".join(results) if results else "No relevant information found."


# ---------------- Image Agent ----------------
class ImageAgent(BaseAgent):
    def __init__(self, name="ImageAgent"):
        super().__init__(name)

    def load_file(self, file_name):
        if not (file_name.endswith(".png") or file_name.endswith(".jpg") or file_name.endswith(".jpeg")):
            return "Please upload an image file (.png, .jpg, .jpeg)."
        if os.path.exists(file_name):
            self.image = Image.open(file_name)
            return f"Image '{file_name}' loaded successfully."
        else:
            return f"File '{file_name}' not found in workspace. Please import it into CodePad."

    def process(self, message):
        if not hasattr(self, "image"):
            return "Please upload an image first."
        return f"Processing image... (Pretend I’m detecting objects for query: '{message}')"


# ---------------- GuruBot ----------------
class GuruBot:
    def __init__(self, name="GuruBot"):
        self.name = name
        self.text_agent = TextAgent()
        self.image_agent = ImageAgent()
        self.active_agent = None

    def switch_agent(self, agent_type):
        if agent_type == "text":
            self.active_agent = self.text_agent
            return "Switched to TextAgent."
        elif agent_type == "image":
            self.active_agent = self.image_agent
            return "Switched to ImageAgent."
        else:
            return "Unknown agent type. Use 'text' or 'image'."

    def upload_file(self, file_name):
        if not self.active_agent:
            return "Please select an agent first (text/image)."
        return self.active_agent.load_file(file_name)

    def process(self, message):
        msg = message.lower()

        # GuruBot small talk
        if "hello" in msg or "hi" in msg:
            return "Hello! How can I help you today?"
        elif "your name" in msg:
            return f"My name is {self.name}."
        elif "bye" in msg:
            return "Goodbye! Have a nice day."

        # Delegate to active agent
        if self.active_agent:
            return self.active_agent.process(message)

        return "Sorry, I didn't understand that. Can you rephrase?"

    def chat(self):
        print(f"{self.name} is online. Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.startswith("switch "):
                _, agent_type = user_input.split(" ", 1)
                print(self.switch_agent(agent_type))
                continue
            elif user_input.startswith("upload "):
                _, file_name = user_input.split(" ", 1)
                print(self.upload_file(file_name))
                continue

            response = self.process(user_input)
            print(f"{self.name}: {response}")

            if "bye" in user_input.lower():
                break


if __name__ == "__main__":
    bot = GuruBot(name="GuruBot")
    bot.chat()