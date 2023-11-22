CHUNK_SUMMARY_PROMPT = (
    "Summarize the following text enclosed within triple backticks "
    "in 100-200 words."
    "Ignore meta text like table of contents, acknowledgements, "
    "preface, etc. and only focus on the core content. "
    "Return only the generated summary and nothing else. "
    "Refer only to the content in the provided text and "
    "don't spoil anything from future chapters. "
    "Don't talk about the book, only about the "
    "text provided below within triple backticks. "
    "The summary must be between 100-200 words long. "
    "\n```\n{}\n```\n"
)

FINAL_SUMMARY_PROMPT = (
    "Summarize the following text within triple backticks "
    "in at least 500 words. "
    "Return only the generated summary and nothing else. "
    "Refer only to the content in the provided text and "
    "don't spoil anything from future chapters. "
    "Don't talk about the book, only about the "
    "text provided within triple backticks. "
    "The summary must include everything that happens below."
    "\n```\n{}\n```\n"
)
