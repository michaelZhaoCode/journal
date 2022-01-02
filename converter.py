from os import listdir, remove
from datetime import datetime
# Change name format of files
OLD_DATE_FORMAT = "%d-%m-%Y"
NEW_DATE_FORMAT = "%Y-%m-%d"
# Load current pages
pages = [page for page in listdir("pages") if ".txt" in page]

for page in pages:
    with open(f"pages/{page}") as file:
        text = file.read()
        dates = page[:-4].split("-")
        new_name = datetime.strptime(page[:-4], OLD_DATE_FORMAT).strftime(NEW_DATE_FORMAT) + ".txt"
        # Create new file
        with open(f"pages/{new_name}", "w") as new_file:
            new_file.write(text)
    # Remove old file
    remove(f"pages/{page}")
