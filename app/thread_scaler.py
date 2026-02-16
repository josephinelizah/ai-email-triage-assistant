def compress_thread(thread_messages, max_chars=500):
    
    full_text = " ".join(thread_messages)
    if len(full_text) <= max_chars:
        return full_text
    compressed = full_text[-max_chars:]

    return compressed
