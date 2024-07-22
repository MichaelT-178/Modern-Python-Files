import json
import os
import shutil
import subprocess
import time
from termcolor import colored as c

class FlashDrive:
    """ 
    Class to perform various flash drive operations

    Methods 
    open_flash_drive_in_finder: Opens flash drive path in Finder 
    add_file_to_flash_drive: Adds a file/folder to the flash drive
    delete_file_on_flash_drive: Deletes file from flash drive
    unmount_drive: Unmounts drive from computer 
    remount_drive: Remounts drive from computer 
    eject_drive: ejects drive from computer 
    get_all_files: Gets all the files from the flash drive as a list.
    explain_unmount_and_eject: Explains the difference between unmounting and ejecting a Flash Drive.
    
    Example code at the bottom of this file.
    """

    def __init__(self, flash_drive_name: str, flash_drive_identifier: str):
        """
        Initializes the flash drives path and identifier 
        :param flash_drive_name: Name of the flash drive ex: USBMST1
        :param flash_drive_identifier: Identifies the flash drive to eject it. Ex: /dev/disk4
        """
        self.flash_drive_path = f"/Volumes/{flash_drive_name}"

        # Flash drive identifier. Find this path using the command: diskutil list
        self.flash_drive_identifier = flash_drive_identifier


    def open_flash_drive_in_finder(self):
        """
        Opens flash drive directory in Finder. If error 
        occurs because flash drive can't be found print the 
        error in red.
        """
        command = ["open", self.flash_drive_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(c(result.stderr.strip(), 'red'))
        else:
            print(c("Flash Drive's Content is being displayed in Finder!\n", 'blue'))


    def add_file_to_flash_drive(self) -> None:
        """
        Adds a file/folder to the flash drive.
        """

        while True:
            file_path = input("Please enter the path of the file/folder you want to add (or 'q' to quit): ")

            if file_path.lower().strip() == 'q':
                print(c("Operation cancelled.", "red"))
                time.sleep(1)
                os.system('clear')
                print_menu()
                return

            if os.path.isfile(file_path) or os.path.isdir(file_path):
                print(c("File/folder path is valid.", "green"))

                confirm = input(f"Are you sure you want to add \"{file_path}\" to your flash drive? (yes/y): ")

                if confirm.lower().strip() in ["yes", "y"]:
                    break
                else:
                    print(f"The file/folder will {c('NOT', 'red')} be added to your flash drive. Please enter a new path.")
            else:
                print(c("Invalid file/folder path. Please try again.", "red"))

        file_name = os.path.basename(file_path)
        destination_path = os.path.join(self.flash_drive_path, file_name)

        try:
            if os.path.isfile(file_path):
                shutil.copy(file_path, destination_path)
            elif os.path.isdir(file_path):
                shutil.copytree(file_path, destination_path)

            print(c(f'The file/folder: "{file_name}" was successfully added to the flash drive. Destination: "{destination_path}"', "green"))
            self.open_flash_drive_in_finder()
        except Exception as e:
            print(c(f'An error occurred while trying to add the file/folder to the flash drive: {str(e)}', 'red'))


    def delete_file_on_flash_drive(self) -> None:
        """
        Deletes a file or folder from the flash drive.
        """

        while True:
            self.open_flash_drive_in_finder()

            all_files = self._get_files_recursive(self.flash_drive_path)
            
            if not all_files:
                print(c("\nThere are currently no files or folders on your Flash Drive.", "red"))
                return

            file_path = input("Please enter the path of the file/folder you want to delete (or 'q' to quit): ")

            if file_path.lower().strip() == 'q':
                print(c("Operation cancelled.", "red"))
                time.sleep(1)
                os.system('clear')
                print_menu()
                return

            file_name = os.path.basename(file_path)
            destination_file = os.path.join(self.flash_drive_path, file_name)

            if os.path.exists(destination_file):
                confirm = input(f"Are you sure you want to delete \"{file_path}\" from your flash drive? (yes/y): ")

                if confirm.lower().strip() in ["yes", "y"]:
                    try:
                        if os.path.isdir(destination_file):
                            shutil.rmtree(destination_file)
                        else:
                            os.remove(destination_file)
                        print(c(f'The file/folder: "{file_path}" was successfully removed from the flash drive!', 'green'))
                    except Exception as e:
                        print(f'Error occurred while trying to remove the file/folder from the flash drive: {str(e)}')
                else:
                    print(f'The file/folder: "{file_path}" will {c("NOT", "red")} be deleted. Please enter a new path.')

            else:
                print(c(f"Can't delete the file/folder: \"{file_path}\". Does not exist on flash drive.", 'red'))


    def unmount_drive(self) -> None:
        """
        Unmounts the flash drive from the computer without full on 
        ejecting it. 
        """

        try:
            command = ['diskutil', 'unmountDisk', self.flash_drive_identifier]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.stderr.strip():
                print(c(result.stderr.strip(), 'red'))
            else:
                print(c(f"Flash drive at '{self.flash_drive_identifier}' has been successfully unmounted!\n", 'green'))

        except Exception as e:
            print(c(f'Error occurred while unmounting the flash drive: {str(e)}', 'red'))

    def remount_drive(self):
        """
        Remounts the flash drive. Prints an error
        if process can't be completed.
        """

        try:
            command = ['diskutil', 'mountDisk', self.flash_drive_identifier]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.stderr.strip():
                print(c(result.stderr.strip(), 'red'))
                print(c("Make sure you've physically removed your flash drive after the last ejection.\n", 'red'))
                exit(0)
            else:
                print(c(f"Flash drive at '{self.flash_drive_identifier}' has been successfully remounted!\n", 'green'))
        except Exception as e:
            print(c(f'Error occurred while remounting the flash drive: {str(e)}', 'red'))

    def eject_drive(self) -> None:
        """
        Ejects the flash drive from the computer.
        """

        try:
            command = ['diskutil', 'eject', self.flash_drive_identifier]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.stderr.strip():
                print(c(result.stderr.strip(), 'red'))
                print(c("Make sure to connect and mount your Flash Drive.\n", "red"))
                exit(0)
            else:
                print(c(f"Flash drive at '{self.flash_drive_identifier}' has been successfully ejected!", 'green'))
                print(c("Physically remove the flash drive from your computer to eject it completely.\n", 'blue'))
                exit(0)

        except Exception as e:
            print(c(f'Error occurred while ejecting the flash drive: {str(e)}', 'red'))
            exit(0)

    def get_all_files(self) -> [str]:
        """
        Gets all files from the drive and returns them as a string list. Doesn't include 
        hidden files.
        """
        try:
            if not os.path.exists(self.flash_drive_path):
                print(c("The specified flash drive path does not exist.\n", "red"))
                exit(0)

            all_files = self._get_files_recursive(self.flash_drive_path)

            if all_files:
                print("\nThese are all the Files on your Flash Drive:")
                for file in all_files:
                    print(file)
            else:
                print(c("\nThere are currently no files on your Flash Drive.", "red"))
                
        except Exception as e:
            print(f'Error occurred while getting files from the flash drive: {str(e)}')


    def _get_files_recursive(self, path, level=0):
        """
        Helper function to recursively get files and folders.
        """
        items = []
        try:
            for entry in os.listdir(path):
                if not entry.startswith('.'):
                    full_path = os.path.join(path, entry)
                    indent = '    ' * level

                    if os.path.isdir(full_path):
                        items.append(f"{indent}{entry}")
                        items.extend(self._get_files_recursive(full_path, level + 1))
                    else:
                        items.append(f"{indent}- {entry}")

        except Exception as e:
            print(f'Error occurred while accessing the path {path}: {str(e)}')

        return items
    
    def copy_file_to_new_location(self, old_file_name, new_path):
        """
        Copys a file from the flash drive to a new location
        :param old_file_name: The name of the file on the flash to be copied.
        :param new_path: The new path the file will be copied to.
        """
        fd_file_path = f"{self.flash_drive_path}/{old_file_name}"
        os.system(f"cp {fd_file_path} {new_path}")

    def explain_unmount_and_eject(self):
        print("\nDefinitions")
        print(f"{c('Unmount', 'blue')}: Temporarily disconnect the Flash Drive logically, but not physically. Do this if you plan to reconnect Flash Drive without physically removing it first.")
        print(f"{c('Eject', 'blue')}: Logically and Physically remove the Flash Drive\n") 
        
        understood = input("Understood? (y/yes): ")

        if understood.lower().strip() in ["yes", "y"]:
            print(c("Great!", "green"))
            time.sleep(1)
            os.system('clear')
            print_menu()
            return

def print_menu():
    print("Flash Drive Options")
    print("1. Open flash drive contents in Finder ")
    print("2. Add files/folders to your flash drive")
    print("3. Delete files from your flash drive")
    print("4. Unmount your flash drive")
    print("5. Remount your flash drive")
    print("6. Eject flash drive from your computer ")
    print("7. Displays all the files from your flash drive")
    print("8. Explains unmounting vs ejecting a Flash Drive\n")


def choose_option(flash_drive, choice: int):
    match choice:
        case 1:
            flash_drive.open_flash_drive_in_finder()
        case 2:
            flash_drive.add_file_to_flash_drive()
        case 3:
            flash_drive.delete_file_on_flash_drive()
        case 4:
            flash_drive.unmount_drive()
        case 5:
            flash_drive.remount_drive()
        case 6:
            flash_drive.eject_drive()
        case 7:
            flash_drive.get_all_files()
        case 8:
            flash_drive.explain_unmount_and_eject()
        case _:
            print(c("Invalid number", "red"))


def get_flash_drive():

    with open("data.json", "r") as file:
        content = json.load(file)
        
    name = content['Name']
    identifier = content["Identifier"]

    return FlashDrive(name, identifier)


def prompt_user(flash_drive):
    while True:
        user_input = input("Choose an option 1-8 (or 'q' to quit): ")
        
        if user_input.lower() == 'q':
            print(c("Program quite successfully", "green"))
            flash_drive.eject_drive()
            break
        
        try:
            user_number = int(user_input)
            if 1 <= user_number <= 8:
                choose_option(flash_drive, user_number)
            else:
                print(c("Invalid input. Please enter an integer between 1 and 8.", "red"))
        except ValueError:
            print(c("Invalid input. Please enter an integer between 1 and 8.", "red"))


def main():

    flash_drive = get_flash_drive()

    print_menu()
    prompt_user(flash_drive)

main()