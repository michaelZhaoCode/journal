from os import listdir, remove
from datetime import datetime

OLD_DATE_FORMAT = "%d-%m-%Y"
NEW_DATE_FORMAT = "%Y-%m-%d"

pages = [page for page in listdir("pages") if ".txt" in page]

for page in pages:
    with open(f"pages/{page}") as file:
        text = file.read()
        dates = page[:-4].split("-")
        new_name = datetime.strptime(page[:-4], OLD_DATE_FORMAT).strftime(NEW_DATE_FORMAT) + ".txt"

        with open(f"pages/{new_name}", "w") as new_file:
            new_file.write(text)

    remove(f"pages/{page}")
