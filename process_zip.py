import zipfile
import os


def delete_pdf_files(pdf_file_path):
    """
    Deletes a PDF file if its name ends with ').pdf'.

    Args:
        pdf_file_path (str): The full path of the PDF file to delete.
    """
    if pdf_file_path.endswith(').pdf'):
        try:
            os.remove(pdf_file_path)
            print(f"Deleted: {pdf_file_path}")
        except OSError as e:
            print(f"Error deleting file {pdf_file_path}: {e}")


def process_all_zip_files(folder_path):
    """
    Processes all ZIP files in a directory by extracting them and deleting specific PDF files.

    Args:
        folder_path (str): The path of the folder containing ZIP files.
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(folder_path)
            print(f"Extracted: {file_name}")

        # Delete PDF files that end with ').pdf'
        if file_name.endswith(').pdf'):
            delete_pdf_files(file_path)


def count_log_lines(log_file_path):
    line_count = 0
    try:
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            for line in log_file:
                line_count += 1
    except FileNotFoundError:
        print(f"The file {log_file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    return line_count

