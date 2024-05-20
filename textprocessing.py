import re
from datetime import datetime


def remove_non_alphanumeric(input_str):
    # Use regex to replace non-alphanumeric characters with an empty string
    return re.sub(r"[^\w\n]", "", input_str)


def get_text_before_stopper(full_text):
    # PRETORIA 0001 is the stopping text in our case
    # Split the text at "PRETORIA 0001" and return the part before it
    before_pretoria = full_text.split("PRETORIA0001")[0]
    return before_pretoria


def isValidDate(year, month, day):

    try:
        if year > 2000 and year < 2025:
            datetime(year, month, day)
            return True
        else:
            return False
    except ValueError:
        return False


def replace_chars(text):
    # a helper dict to replace characters for the ocr to work more properly
    # eg 2023it12 will be converted to 20231113
    replace_dict = {
        "i": "1",
        "I": "1",
        "l": "1",
        "L": "1",
        "o": "0",
        "O": "0",
        "t": "1",
        "T": "1",
        "s": "5",
        "S": "5",
        "E": "3",
        "a": "4",
        "A": "4",
        "b": "6",
        "B": "8",
        "g": "9",
    }
    translation_table = str.maketrans(replace_dict)
    
    # Use the translation table to replace characters
    return text.translate(translation_table)


# print(replace_chars("2023it1E"))


def find_extraction_date(text):
    """Preprocessing"""

    text = replace_chars(get_text_before_stopper(remove_non_alphanumeric(text)))
    # print(f"Processed text: {text}")

    # Define the regex pattern for matching dates in the format YYYYMMDD
    pattern = r"(\d{4})(\d{2})(\d{2})"

    # Find all matches in the input string
    matches = re.findall(pattern, text)
    # print(f"Matches: {matches}")

    # Filter matches using isValidDate
    valid_dates = []
    for match in matches:
        year = int(match[0])
        month = int(match[1])
        day = int(match[2])
        if isValidDate(year, month, day):
            valid_dates.append(match)

    # print(f"Valid dates: {valid_dates}")

    if valid_dates:
        # Get the last valid match
        last_match = valid_dates[-1]
        year = int(last_match[0])
        month = int(last_match[1])
        day = int(last_match[2])

        # Create a datetime object and format it as YYYY-MM-DD
        formatted_date = datetime(year, month, day).strftime("%Y-%m-%d")
        return formatted_date

    return None


# Example usage
# txt = r"""
# #012#012alls#012qi: ansni#012#012South African Police Service#012#012Clearance Certificate#012#012asic 0 2e0is#012are oF ane 60721#012somos = Oh#012ane wes#012#012ers am m0,#012#012(SUID-AFRIRAANSE POUSIEDIENS]#012#0122 -H- 08#012#012[SOUTH AFRICAN POLICE SERVICE#012#012 #012#012 #012#012 #012#012 #012#012 #012#012 #012#012 #012#012   #012#012wo#012MP HLONEWANE#012#012 #012#012 #012#014 #012#012 #012#012{POSTILLE#012#012| Com REPUBLIC OF SOUTH AFRICA#012ie document miked y#012#012MORAGA PETER HLONGWANE#012#012   #012   #012#012ne WARRANT OFFICER#012the stamp of SOUTH AFRICAN POLICE SERVICE (SAPS)#012| CERTIFIED#012PRETORIA on 21 December 2022#012#012KARIEN VAN DER VYVER#012#012 #012#014 #012#012 #012#012APOSTILLE#012#012(Convention de La Haye du 5 Octobre 1961)#012#012Country REPUBLIC OF SOUTH AFRICA#012#012  #012  #012  #012 #012 #012  #012   #012#012 #012#012‘This public document marked#012#012has been signed by PHUMZILE MARTINA MTSWENI#012acting in the capacity of DEPUTY DIRECTOR: VERIFICATIONS#012PROJECT#012| bears the samp of SOUTH AFRICAN QUALIFICATIONS#012AUTHORITY (SAQA)#012CERTIFIED#012#01213 July 2023#012#012at PRETORIA on#012#012 #012#012 #012#012 #012#012 #012#012 #012#012 #012 #012#012 #012#012   #012#012hs Apt Cerificate only cris the authentic of the#012wh
# """
# input_string = txt

# formatted_date = find_extraction_date(input_string)
# print(formatted_date)  # Should print '2023-11-06'
