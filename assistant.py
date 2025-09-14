import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import gradio as gr
import PyPDF2

def read_pdf(file_path):
    """
    Reads a PDF file and returns all the text content.
    """
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or "" 
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None
    return text

model_id = "google/gemma-2b-it"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto", 
    dtype=torch.bfloat16
)


def summarize(file_input, text_input, max_len_param):
    """
    Summarizes either a text string or a PDF file, with a user-specified max length.
    """
    text = ""
    

    if file_input is not None:
        file_path = file_input.name
        if file_path.lower().endswith(".pdf"):
            text = read_pdf(file_path)
            if text is None:
                return "Could not process the PDF file."
        else:
            return "Please upload a PDF file."

    elif text_input.strip() != "":
        text = text_input
    else:
        return "Please upload a file or paste text to summarize."

    try:
        max_length = int(max_len_param)
        if max_length <= 0:
            return "Max length must be a positive number."
    except (ValueError, TypeError):
        return "Error: Max length must be a number."

    if not text.strip():
        return "The document is empty or text could not be extracted."


    prompt = f"Please read the following text and provide a concise summary of it. The summary should capture the main points and key findings. Ensure the output is only the summary and nothing else.\n\nText to summarize:\n{text}\n\nConcise Summary:"

    # prompt = f"Based on the following document, answer the question: '{user_question}'.\n\nDocument:\n{text}\n\nAnswer:"

    # prompt = f"From the following text, list the most important keywords and keyphrases. Separate them with commas.\n\nText:\n{text}\n\nKeywords:"
    
    # prompt = f"Based on the following text, write a more detailed explanation of the section on '{section}'.\n\nText:\n{text}\n\nExpanded Explanation:"

    input_ids = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **input_ids,
        max_new_tokens=max_length,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95
    )
    
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    summary = summary.replace(prompt, "").strip()
    return summary


with gr.Blocks(theme="huggingface", title="Offline AI Research Assistant with Gemma") as demo:
    gr.Markdown("# Offline AI Research Assistant with Gemma 🤖")
    gr.Markdown("Summarize any text or PDF using a local Gemma model. Your data stays on your machine!")
    
    with gr.Row():
        file_input = gr.File(label="Upload a PDF file 📄", file_types=[".pdf"])
        text_input = gr.Textbox(lines=15, label="... or paste text here ✍️", interactive=True)
    
    max_length_slider = gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max Output Tokens", interactive=True)
        
    output_text = gr.Textbox(label="Generated Summary ✨")
    
    summarize_btn = gr.Button("Summarize")


    summarize_btn.click(
        fn=summarize,
        inputs=[file_input, text_input, max_length_slider],
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch()
