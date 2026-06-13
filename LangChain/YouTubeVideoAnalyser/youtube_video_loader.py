from langchain_community.document_loaders import YoutubeLoader

def get_transcript_data():
    def take_vid_id_input():
        return input("Enter Youtube Video ID: ")
    
    vid_id = take_vid_id_input()
    while not vid_id:
        print("please enter a valid youtube video id.")
        vid_id = take_vid_id_input()
    
    loader = YoutubeLoader(video_id=vid_id, language="en")
    transcript_data = loader.load()
    return transcript_data