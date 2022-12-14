import os
import logging
import traceback

import tkinter as tk

from tkinter import filedialog


def get_folder_and_file_information():
    """
    Get project folder root (the folder where the invoices are to be sorted by project and invoce number)
    Also select invoices to be sorted to the said folder.

    Parameters:
    None.
  
    Returns:
    Project folder root location.
    List of invoices selected.
  
    """
    root = tk.Tk()
    root.withdraw()

    try:
        project_folder = filedialog.askdirectory(parent=root, title="Valitse kansio, minne ostolaskut lajitellaan.")
        invoices = filedialog.askopenfilenames(parent=root, title="Valitse kuitatut ostolaskut kansiosta.")
    except OSError:
        print("================= Something went wrong reading the file... =================")
        exit()

    print()
    print("=============== Valittu kansio johon ostolaskut lajitellaan: ===============")
    print(project_folder)
    print()

    #Save invoices to a list:
    invoices = list(invoices)

    return project_folder, invoices

def sort_files(parent_dir, files):
    """
    Sorts the invoices to their folders.

    Parameters:
    parent_dir: Selected folder where invoices are to be sorted.
    files: Selected invoices to be sorted.
  
    Returns:
    True if everything went allright.
    False if not.
    """

    try:
        for f in files:
            #Extract the base filename from the selected files.
            #They are now in a list of filepaths prior to this.
            #We dont like that...
            fname = os.path.basename(f)
            #Extract project number from the filename
            #Invoices are named with the convention: XXXYYYYY
            #Where "XXX" is Project number and "YYYYY" is invoice number
            #So pretty much first 3 numbers are the project number
            #and from there the next 5 numbers are the invoice number
            #the remaining numbers are not really relevant in this operation its just the nth invoice of the day and date formatted
            project_no = fname[:3]
            invoice_no = fname[3:8]

            print("========================== Lajitellaan ostolaskua: =========================")
            print(project_no, invoice_no)
            print()

            file_path = os.path.join(parent_dir, os.path.join(project_no, invoice_no))
            
            #Make project folders to the destination folder
            try:
                os.makedirs(file_path, exist_ok=True)
            except OSError as e:
                print("================================= FAILURES =================================")
                print("_________________________ Kansiota ei voida tehd??: _________________________")
                print(file_path)

            #Move files to destination folders
            os.rename(f, os.path.join(file_path, fname))

    except Exception as e:
        print("================================= FAILURES =================================")
        print("__________________________ Jotain meni pieleen... __________________________")
        logging.error(traceback.format_exc())
        return False

    return True

def main():
    project_folder, invoices = get_folder_and_file_information()
    
    if sort_files(project_folder, invoices):
        print()
        print("================================= SUCCESS =================================")
        print("_____________________ Ostolaskujen lajittelu onnistui _____________________")


    else:
        print()
        print("================================= FAILURES =================================")
        print("___________________ Ostolaskujen lajittelu ei onnistunut ___________________")

    

if __name__ == "__main__":
    main()