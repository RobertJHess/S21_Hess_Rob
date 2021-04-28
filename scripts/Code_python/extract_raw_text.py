from FileUtility import FileUtility
import sys
import re


def extract_text_statements(lines):
    extracted_text = []
    is_found = False
    for line in lines:
        if re.search(r"id\s*=\s*\"article\"", line) is not None:
            is_found = True
            print("Found article")
        if re.search(r"id\s*=\s*\"lastUpdate\"", line) is not None:
            is_found = False
            break
        if is_found:
            extracted_text.append(line.strip())

    if is_found:
        print("Never Found Ending Marker!")

    return "\n".join(extracted_text)


def clean_text_statements(lines):
    text_cleaned = []
    for line in lines:
        cleaned_line = re.sub("(<)|(>)", "", re.sub(r"(?<=<).*?(?=>)", "", line))
        if cleaned_line != "Share" and cleaned_line != "":
            text_cleaned.append(cleaned_line)
    return "\n".join(text_cleaned)


def main():
    if len(sys.argv) < 3:
        print("Expected 3 arguments.")
        print("Usage: python3 <script_name> <type_of_file> <root_path_of_files_to_extract> <root_path_to_save_files>")
        print("type_of_file: statement")
        exit()
    if sys.argv[1] not in extensions:
        print("Invalid argument")
        print("Usage: python3 script_name root_path_of_files_to_extract type_of_file")
        print("type_of_file: statement")

    file_names = FileUtility.get_list_of_filenames_of_type(extensions[sys.argv[1]], sys.argv[2])
    for file in file_names:
        lines = FileUtility.read_all_lines(file)
        extracted_text = extraction_type[sys.argv[1]](lines)
        cleaned_extracted_text = clean_type[sys.argv[1]](extracted_text.strip().split(sep="\n"))
        file_name_to_write = file[len(sys.argv[2]):len(file) - len(extensions[sys.argv[1]]):]
        FileUtility.write_lines(sys.argv[3] + file_name_to_write + ".txt", cleaned_extracted_text.split(sep="\n"))


extensions = {"statement": ".html"}
extraction_type = {"statement": extract_text_statements}
clean_type = {"statement": clean_text_statements}

if __name__ == "__main__":
    main()
