from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_chunks(transcript_data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 200
    )
    print(transcript_data)
    chunks= splitter.split_text(transcript_data[0].page_content)
    return chunks
