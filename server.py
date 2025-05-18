from itertools import count
import gradio as gr
def letter_counter(word: str, letter: str) -> int:
    """
    Count the number of times a letter appears in a word or text.
    
    Args:
        word (str): The input text to search through
        letter (str): The letter to search for
    
    Returns:
        The number of times the letter appears in the text.
    """
    word = word.lower()
    letter = letter.lower()
    return word.count(letter)
    return count

# Create a standard Gradio interface

demo = gr.Interface(
    fn=letter_counter,
    inputs=["textbox", "textbox"],
    outputs="number",
    title="Letter Counter",
    description="Enter text and letter to count how many times the letter apperas in the text." 
)
    # Launch both the Gradio web interface and the MCP server
if __name__ == "__main__":
    demo.launch(mcp_server = True)
    
    
        