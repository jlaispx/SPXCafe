from rapidfuzz import fuzz, process, utils
from rapidfuzz.fuzz import partial_ratio
from rapidfuzz.utils import default_process
from rapidfuzz.process import extract, extractOne

options = ["hawaiian pizza","supreme pizza","pizza marinara", "fish fillets","ice cream","potato soup"]
# options = ["yes", "no"]


    # (match, confidence, index) = process.extractOne(choice, options,processor=utils.default_process )

# print(f"You have chosen : {match} with confidence level of {confidence}%")
matches = []
maxConfidence = 60

while len(matches)!=1:
    # choice = input(f"Choose from: {','.join(options)}: ").strip().lower()
    choice = input(f"Choose one").strip().lower()
    if not choice:
        break

    results = process.extract(choice, options, scorer=fuzz.partial_ratio, processor=utils.default_process)
    for result in results:
        (match, confidence, index) = result
        print(f"Checking: {result}")
        if confidence > maxConfidence:
            maxConfidence = confidence
            matches = [match]
        elif confidence == maxConfidence:
            matches.append(match)

    print(f"You have matched: {','.join(matches)} with confidence level {maxConfidence}% {len(matches)}")
    if len(matches)>1:
        print("Sorry, you need to choose only one! Try again")
        options = matches
        matches = []
        maxConfidence = 0

