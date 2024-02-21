import os
import shutil
import subprocess
from termcolor import colored as c

class FlashDrive:
    """ 
    Class to perform various flash drive operations

    Methods 
    open_flash_drive_in_finder: Opens flash drive path in finder 
    add_file_to_flash_drive: Adds file from flash drive
    delete_file_on_flash_drive: Deletes file from flash drive
    unmount_drive: Unmounts drive from computer 
    remount_drive: Remounts drive from computer 
    eject_drive: ejects drive from computer 
    get_all_files: Gets all the files from the flash drive as a list.
    
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

    @staticmethod
    def open_flash_drive_in_finder(self):
        """
        Opens flash drive directory in finder. If error 
        occurs because flash drive can't be found print the 
        error in red.
        """
        command = ["open", self.flash_drive_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result:
            print(c(result.stderr.strip(), 'red'))


    def add_file_to_flash_drive(self, path_to_src_file: str) -> None:
        """
        Adds a file to the flash drive.
        :param path_to_src_file: The path to the file that will be added.
        """

        FlashDrive.open_flash_drive_in_finder(self)

        file_name = os.path.basename(path_to_src_file)

        destination_file = os.path.join(self.flash_drive_path, file_name)

        try:
            shutil.copy(path_to_src_file, destination_file)
            print(c(f'The file: "{file_name}" was successfully added to the flash drive. Destination: "{destination_file}"', "green"))
        except Exception as e:
            print(c(f'An error occurred while trying to add the file to the flash drive: {str(e)}', 'red'))
    

    def delete_file_on_flash_drive(self, path_to_src_file: str) -> None:
        """
        Deletes a file from the flash drive.
        :param path_to_src_file: The path to the file that will be deleted.
        """

        FlashDrive.open_flash_drive_in_finder(self)

        file_name = os.path.basename(path_to_src_file)

        destination_file = os.path.join(self.flash_drive_path, file_name)

        try:
            if os.path.exists(destination_file):
                os.remove(destination_file)
                print(c(f'The file: "{path_to_src_file}" was successfully removed from the flash drive!', 'green'))
            else:
                print(c(f'Can\'t delete the file: "{path_to_src_file}". Does not exist on flash drive.', 'red'))
        except Exception as e:
            print(f'Error occurred while trying to remove the file from the flash drive: {str(e)}')


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
                print(c(f"Flash drive at '{self.flash_drive_identifier}' has been unmounted successfully!", 'green'))
                print(c("Physically remove the flash drive from the computer to eject it", 'blue'))

        except Exception as e:
            print(c(f'Error occurred while unmounting the flash drive: {str(e)}', 'red'))

    def remount_drive(self):
        """
        Remounts the flash drive. Prints an error
        if process can't be completed.
        """

        FlashDrive.open_flash_drive_in_finder(self)

        try:
            command = ['diskutil', 'mountDisk', self.flash_drive_identifier + 's1']
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.stderr.strip():
                print(c(result.stderr.strip(), 'red'))
            else:
                print(c(f"Flash drive at '{self.flash_drive_identifier}' has successfully been remounted!", 'green'))
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
            else:
                print(c(f"Flash drive at '{self.flash_drive_identifier}' has successfully been ejected!", 'green'))
                print(c("Physically remove the flash drive from the computer to eject it completely", 'blue'))

        except Exception as e:
            print(c(f'Error occurred while ejecting the flash drive: {str(e)}', 'red'))
    
    def get_all_files(self) -> [str]:
        """
        Gets all files from the drive and returns them as a string list. Doesn't include 
        hidden files.
        """
        try:
            file_list = [f for f in os.listdir(self.flash_drive_path) if not f.startswith('.')]
            return [os.path.join(self.flash_drive_path, file_name) for file_name in file_list] 
        except Exception as e:
            print(c(f'Error occurred while getting files from the flash drive: {str(e)}', 'red'))

    def copy_file_to_new_location(self, old_file_name, new_path):
        """
        Copys a file from the flash drive to a new location
        :param old_file_name: The name of the file on the flash to be copied.
        :param new_path: The new path the file will be copied to.
        """
        fd_file_path = f"{self.flash_drive_path}/{old_file_name}"
        os.system(f"cp {fd_file_path} {new_path}")
                                  


def driver_code():  
    flash_drive = FlashDrive('USBMST1', '/dev/disk4')
    
    add_tok = input("Do you want to add a tok? : ")

    florida_tok = '/Users/michaeltotaro/tiktoks/Florida.mp4'

    if add_tok.upper() in ["YES", "Y"]:
        flash_drive.add_file_to_flash_drive(florida_tok)

    delete_tok = input("\nDo you want to delete tok? : ")

    if delete_tok.upper() in ["YES", "Y"]:
        flash_drive.delete_file_on_flash_drive(florida_tok)


    eject_fd = input("\nDo you want to unmount flash drive? : ")

    if eject_fd.upper() in ["YES", "Y"]:
        flash_drive.unmount_drive()

    remount_fd = input("\nDo you want to remount flash drive? : ")

    if remount_fd.upper() in ["YES", "Y"]:
        flash_drive.remount_drive()

    eject_fd = input("\nDo you want to fully eject flash drive? : ")

    if eject_fd.upper() in ["YES", "Y"]:
        flash_drive.eject_drive()


driver_code()

















