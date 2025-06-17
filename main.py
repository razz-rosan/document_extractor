import gradio as gr
from utils.file_loader import extract_text
from utils.llm_chain import get_chain

chain = get_chain()


def extract_info(file, instruction):
    if file is None or instruction.strip() == "":
        return "Please upload a file and provide instructions."
    
    filename = file.name  
    try:
        text = extract_text(file, filename)
    except Exception as e:
        return f"Error reading file: {e}"
    
    result = chain.invoke({"document": text, "instruction": instruction})
    return result




with gr.Blocks() as demo:
    gr.Markdown("# 📄 Document Information Extractor with Mistral + LangChain")
    with gr.Row():
        
        file = gr.File(label="Upload your Document (PDF, DOCX, TXT, JPG, PNG)", file_types=[".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png"])
        instruction = gr.Textbox(lines=2, label="What do you want to extract?")
    output = gr.Textbox(lines=10, label="Extracted Information")

    btn = gr.Button("Extract Info")
    btn.click(fn=extract_info, inputs=[file, instruction], outputs=output)

if __name__ == "__main__":
    demo.launch()

