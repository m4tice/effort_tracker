"""TEST"""

# import hashlib

def get_hashed_entry(input_string: str):
    """
    Get hashed form
    """
    non_whitespace_input_string = input_string.replace(" ", "")
    lowercase_input_string = non_whitespace_input_string.lower()
    print(lowercase_input_string)
    # return hashlib.sha256(non_whitespace_input_string.encode('utf-8')).hexdigest()


example = "RQONE210696 -[rba_Nds][ComService] AnH yeU bE Chang NhIeU lAm!! @ ra ar awrx1r1 >"
get_hashed_entry(example)
