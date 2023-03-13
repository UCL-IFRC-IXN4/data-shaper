import os
import copy

file_path = "../data/NEW-Desinventar-data/raw"
EMPTIES = [0, None]


def clean(raw_line):
    """
    Helper function - cleans a line of data from Desinventar

    @param raw_line: line of data from Desinventar
    @return: cleaned line of data
    """
    cleaned_line = (
        str(raw_line)
        .strip("\n")
        .encode()
        .decode("utf-8")
        .replace("\t", ", ")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
    )
    return cleaned_line


def copy(list):
    """
    Helper function - copies a list of lists

    @param list: list of lists
    @return: copy of list of lists
    """
    # only works for lists in form: [[a, [b, c]], [d, [e, f]], ...]
    new_list = []
    for i in list:
        # i = [a, [b, c]]
        if len(i[1]) == 1:
            new_list.append([i[0], [i[1][0]]])
        else:
            new_list.append([i[0], [i[1][0], i[1][1]]])
    return new_list


# loop through every file in directory
directory = os.fsencode(file_path)
for file in os.listdir(directory):
    filename = os.fsdecode(file)

    # list of columns to be collected
    collected_headers = [["Event", []], ["Date", []], ["Affected", []], ["Deaths", []]]

    # special case for Pacific Islands (PDN).csv file as is a collectino of countries
    if filename == "Pacific Islands (PDN).csv":
        collected_headers.append(["Country", [3]])

    # skip = True if line is incomplete
    skip = False
    country_directory = f"{file_path}/{filename}"
    prev_line = ""
    joined_line2 = []
    try:
        print(f"Opening {country_directory}...")
        print("Cleaning data...")
        with open(country_directory, "r") as file:

            # ignores github config file
            if filename == ".DS_Store":
                continue

            # create new file to write to
            with open(
                f"../data/NEW-Desinventar-data/cleaned/{filename}", "w"
            ) as new_file:
                data = file.readlines()
                CORRECT_LINE_LENGTH = len(clean(data[1]).split(", "))

                # loops through every line in raw data file
                for raw_line in data:
                    cleaned_line = clean(raw_line)
                    if cleaned_line == "":
                        continue

                    # check is line is complete
                    if len(cleaned_line.split(", ")) < CORRECT_LINE_LENGTH:
                        # line is incomplete
                        if cleaned_line.split(", ")[0] != "Serial":
                            if skip:
                                # there is a uncompleted line already - line is part of previous line
                                # cleaned_line[0] is part of joined_line2[-1]
                                joined_line2[-1] += cleaned_line.split(", ").pop(0)
                                joined_line2.extend(cleaned_line.split(", "))
                            else:
                                # line has more to be added
                                skip = True
                                joined_line2 = cleaned_line.split(", ")
                                continue
                            if len(joined_line2) >= CORRECT_LINE_LENGTH:
                                # line is complete
                                skip = False
                                joined_line2.append("\n")
                                new_file.write(", ".join(joined_line2))
                                joined_line2 = []
                    else:
                        # line is complete - write to cleaned file
                        cleaned_line += "\n"
                        new_file.write(cleaned_line)
                        prev_line = cleaned_line

            # format data to be used in the program
            with open(f"../data/NEW-Desinventar-data/out/{filename}", "w") as out_file:
                with open(
                    f"../data/NEW-Desinventar-data/cleaned/{filename}", "r"
                ) as cleaned_file:
                    print("Formatting data...\n")
                    data = cleaned_file.readlines()

                    # seperate the column headers from the data
                    headers, data = data[0], data[1:]
                    headers = headers.split(", ")

                    # find the location of the columns to be collected
                    for header in headers:
                        header = header.replace('"', "")
                        if "Date" in header:
                            collected_headers[1][1].append(headers.index(header))
                        if "Death" in header:
                            collected_headers[3][1].append(headers.index(header))
                        if "Affected" in header or "affected" in header:
                            collected_headers[2][1].append(headers.index(header))
                        if "Event" in header:
                            collected_headers[0][1].append(headers.index(header))
                    raw_line = ""
                    CORRECT_LINE_LENGTH = 0

                    # write inital line of csv and calculate correct line length
                    for heading in collected_headers:
                        for occurence in heading[1]:
                            raw_line += f"{heading[0]}, "
                            CORRECT_LINE_LENGTH += 1
                    raw_line += "\n"
                    out_file.write(raw_line)

                    # make a copy of collected_headers
                    save = copy(collected_headers)
                    for record in data:

                        iterable = record.split(",")
                        collected_headers = copy(save)

                        # finding date location in list
                        for i in iterable:
                            if "/" in i:
                                date_questionMark = i.strip(" ").split("/")
                                if (
                                    len(date_questionMark) == 3
                                    and date_questionMark[0].isdigit()
                                    and date_questionMark[1].isdigit()
                                    and date_questionMark[2].isdigit()
                                ):
                                    collected_headers[1][1][0] = iterable.index(i)
                                    break

                        # finding deaths and effected location in list
                        if filename != "Pacific Islands (PDN).csv":
                            for coloumn in collected_headers[-2:]:
                                for index, occurence in enumerate(coloumn[1]):
                                    collected_headers[collected_headers.index(coloumn)][
                                        1
                                    ][index] = int(
                                        collected_headers[
                                            collected_headers.index(coloumn)
                                        ][1][index]
                                    ) - len(
                                        headers
                                    )

                        # special case for Pacific islands (PDN).csv
                        else:
                            for coloumn in collected_headers[-3:-1]:
                                for index, occurence in enumerate(coloumn[1]):
                                    collected_headers[collected_headers.index(coloumn)][
                                        1
                                    ][index] = int(
                                        collected_headers[
                                            collected_headers.index(coloumn)
                                        ][1][index]
                                    ) - len(
                                        headers
                                    )

                        # write in correct order to out file
                        try:
                            out = []
                            for heading in collected_headers:
                                for occurence in heading[1]:
                                    out.append(iterable[occurence])
                            out = ", ".join(out)
                            out_file.write(out + "\n")
                        except Exception as e:
                            if len(iterable) == 1:
                                continue
                            print(f"Error: {e}")
                            print(collected_headers)
                            print(save)
                            print(f"Filename: {filename}")
                            print(f"Line: {record}")
                            print(f"List: {iterable}")
                            print(f"Output: {out}")
                            print("\n")
                            quit()
                        # fix error where data is split on two lines

    except IsADirectoryError as e:
        print(f"Error: {e}")
