import os

file_path = "../data/NEW-Desinventar-data/raw"
EMPTIES = [0, None]

directory = os.fsencode(file_path)
for file in os.listdir(directory):
    collected_headers = [["Event", []], ["Date", []], ["Affected", []], ["Deaths", []]]
    skip = False
    filename = os.fsdecode(file)
    country_directory = f"{file_path}/{filename}"
    try:
        print("\nCLEANING DATA\n")
        with open(country_directory, "r") as file:
            if filename == ".DS_Store":
                continue
            with open(
                f"../data/NEW-Desinventar-data/cleaned/{filename}", "w"
            ) as new_file:
                data = file.readlines()
                for line in data:
                    # print(f"original: {line}")
                    if skip == True:
                        skip = False
                        continue
                    line2 = (
                        str(line)
                        .encode()
                        .decode("utf-8")
                        .replace("\t", ", ")
                        .replace("&quot;", '"')
                        .replace("&#39;", "'")
                        .replace("&amp;", "&")
                        .replace("&lt;", "<")
                        .replace("&gt;", ">")
                        .strip("\n")
                    )
                    if line2 == "":
                        continue
                    line2 += "\n"

                    # Temporary fix for strings sthat have \n in them (ignores them)
                    cleaned_line_as_list = line2.split()
                    print(cleaned_line_as_list)
                    if cleaned_line_as_list[-1][-3] == ":\n":
                        # line has more on next line
                        # ignore line
                        skip = True
                        continue
                    if cleaned_line_as_list[0] == "'February 4th'":
                        # line is part of previous line
                        # ignore line
                        print(line)
                        skip = True
                        continue
                    # print(f"written to file: {line2}\n")
                    new_file.write(line2)
            with open(f"../data/NEW-Desinventar-data/out/{filename}", "w") as out_file:
                with open(
                    f"../data/NEW-Desinventar-data/cleaned/{filename}", "r"
                ) as cleaned_file:
                    print("\nFORMATTING DATA\n")
                    data = cleaned_file.readlines()
                    headers, data = data[0], data[1:]
                    headers = headers.split(", ")
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
                    line = ""
                    for heading in collected_headers:
                        for occurence in heading[1]:
                            line += f"{heading[0]}, "
                    line += "\n"
                    out_file.write(line)

                    save = collected_headers
                    for record in data:
                        # account for shift in data due to commas in location field
                        iterable = record.split(",")

                        collected_headers = save
                        for i in iterable:
                            if "/" in i:
                                date_questionMark = i.split("/")
                                if (
                                    len(date_questionMark) == 3
                                    and date_questionMark[0].isdigit()
                                    and date_questionMark[1].isdigit()
                                    and date_questionMark[2].isdigit()
                                ):
                                    date_position = iterable.index(i)
                                    break
                        else:
                            date_position = collected_headers[1][1][0]
                        shift = date_position - collected_headers[1][1][0]

                        for i_count, i_val in enumerate(collected_headers[1:]):
                            for j_count, j_val in enumerate(i_val[1]):
                                collected_headers[collected_headers.index(i_val)][1][
                                    j_count
                                ] += shift
                        try:
                            out = ""
                            for heading in collected_headers:
                                for occurence in heading[1]:
                                    out += f"{iterable[occurence]}, "
                            # print(out)
                        except Exception as e:
                            if len(iterable) == 1:
                                continue
                            print(f"Error: {e}")
                            print(f"Filename: {filename}")
                            print(f"Line: {record}")
                            print(f"List: {iterable}")
                            print(f"Output: {out}")
                            print("\n")
                        # fix error where data is split on two lines
        quit()

    except IsADirectoryError as e:
        print(f"Error: {e}")
