#!/usr/bin/python

######################################################################
# Created on 4 August 2015 by Egbie 
#
# Option 1
# A simple script that automates the process of writing
# information to the top bit of a file or script. When run the script adds
# a title, a shebang, an author, script or file information, time it was
# created to the top of the file. 
#
# Option 2
# The script when run with the option
# python createInfo.py -f <filepath> -a can also add the same information 
# in option 1 to an existing script. It does so without altering the data 
# that already exists within that script.
# 
########################################################################

import webbrowser
from time import sleep
import time
import optparse
import os

class Time(object):
    """The current date and time"""

    def get_date(self, format='%d/%m/%Y'):
        """returns the current date"""
        return time.strftime(format)

    def get_time(self):
        """returns the current date"""
        return time.strftime("%X")

class Description(object):
    """The description of the script"""

    def get_script_description(self, message):
        """Get a description for the file"""
        text = []

        if len(message) < 80:
            return False, message

        # ensure that length of the characters does not exceed 80 chars for each new line
        while len(message) > 80:
            text.append(message[:80])
            message = message[80:]
        text.append(message[0:])

        return True, text
        
class Format(object):
    """A simple class creates the format for the page"""

    def draw_border(self, num):
        return "#" * num
        
class FileInputOutput(Format):
    """Class handles anything related to files"""

    def __init__(self, file_name, loc, text_file=False):
        
        self._file_location = os.path.join(loc, file_name)      # createe a file path
        self.create_new_file(self._file_location)               # create a file at that location
        
        # if the file is a text file do not add shebang to file, new line or draw border
        if not text_file:
            self.add_string('#!/usr/bin/python')               # add a shebang to the top of the file
            self.add_string('\n')
            self.add_string(self.draw_border(80))			   # add a border to the top of that page

    def load(self, file_name):
        """load an existing file"""
        with open(file_name) as f:
            my_file = f.read()
        return my_file

    def create_new_file(self, file_name):
        """Create an empty file"""

        f = open(file_name, "w")
        f.close()

    def add_string(self, string):
        """append text to a file"""
        f = open(self._file_location, "a")
        f.write(str(string))
        f.write('\n')
        f.close()

def get_user_input():
    """Get input from the user"""

    title, script_description, version, author = False, False, False, False

    while True:

        print
        if not author:
            author = raw_input("[+] Enter the author for the file : ")
        if not title:
            title = raw_input("[+] Enter name of the script : ")
        if not script_description:
            script_description = raw_input("[+] Enter the description for the script : ")
        if not version:
            version = raw_input("[+] Enter the version number : ")
        if title and script_description and version and author:
            break

    return title, script_description, version, author
            
def create_header(user_obj):
    """ create_header(obj) -> return (None)
    creates the information heading for the file
    """

    info = Description()
    time = Time()
    border = Format()
    title, description, version, author = get_user_input()
    user_obj.add_string(border.draw_border(1))

    # create a string with following information
    time_str = "{} Created on the {} at {} hrs".format(border.draw_border(1), time.get_date(), time.get_time())
    author_name = "{} Created by : {} ".format(border.draw_border(1), author)
    script_name = "{} Name of the program : {} ".format(border.draw_border(1), title)
    ver = "{} This is version : {} ".format(border.draw_border(1), version)
    val, script_description = info.get_script_description(description)

    # write the string to file
    user_obj.add_string(author_name.title())
    user_obj.add_string(script_name.title())
    user_obj.add_string(time_str)
    user_obj.add_string(ver)
    user_obj.add_string(border.draw_border(1))
    user_obj.add_string(border.draw_border(1))
    user_obj.add_string("{} File description ".format(border.draw_border(1)))
    user_obj.add_string(border.draw_border(1))

    # write the main text to file
    if not val:
        user_obj.add_string("{} {}".format(border.draw_border(1), script_description))

    else:
        for text in script_description:
            user_obj.add_string("{} {}".format(border.draw_border(1), text))

    # finish of by creating the border
    user_obj.add_string(border.draw_border(1))
    user_obj.add_string(border.draw_border(80))


def display(f):
    """display the file to the user"""

    print "[+] Opening file please wait .."
    sleep(0.5)
    webbrowser.open(f)
    print "[+] Done, have a nice day!!!\n"

def main():

    parser = optparse.OptionParser("usage -f <filename> -l <dir location> or -f <file_path> -c" )
    parser.add_option('-f', '--filename', dest="filename", type=str, help="Enter the name of a file")
    parser.add_option('-l', '--location', dest="location", type=str, help="Enter location")
    parser.add_option('-a', '--add', action="store_true", dest="add", default=False, 
                              help="edit existing file")
    options, args = parser.parse_args()

    # option 1
    # adds information to a new file.
    if (options.filename and options.location) and not options.add: 
        if not os.path.exists(options.location) and not os.path.isdir(options.location):
            print "[+] The location for the file is not valid. Enter a valid file location"
            exit(0)

        user = FileInputOutput(options.filename, options.location)
        create_header(user) # create the template
        display(user._file_location)

    # option 2
    # Enables information to be added to the top of a file or script that already
    # has information without overiding the information that already exists in the file.
    elif not options.location and options.filename and options.add:
        if os.path.exists(options.filename):

            file_path = os.path.dirname(options.filename)
            user = FileInputOutput("log.txt", file_path, True)
            old_file = user.load(options.filename)
            user.add_string('[+] Successful copied the content of the old file')
            user = FileInputOutput(options.filename, file_path)
            create_header(user)
            user.add_string('\n')
            user.add_string(old_file)
            print "[+] Successful added header info to existing file."
            display(options.filename)
    else:
        print """
            Script usage:

            option 1 for new files
            python createInfo.py -f <filename> -l <location for new file>
            
            
            option 2 modifies existing file without over riding the data
            python createInfo.py -f <file path> -a
        """

if __name__ == "__main__":
    main()

