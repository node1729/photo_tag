import os
from tkinter import *
from PIL import Image, ImageTk
import json


#Checks to see if image is valid, returns True if valid
def check_valid_image(path):
    try:
        Image.open(path)
    except IOError:
        return False
    return True

path = "./photos"

test_dir = os.listdir(path)
test_dir.sort()

tempdir = []
for item in test_dir:
    if check_valid_image(path + "/" + item):
        tempdir.append(item)

test_dir = tempdir.copy()

print(test_dir)

current_photo = 0
tags = []

canvas_width = 700
canvas_height = 700

#create master, canvas, and entry box
master = Tk()
canvas = Canvas(master, width=canvas_width, height=canvas_height)
canvas.grid(row=0, columnspan=2)
e = Entry(master)
e.grid(row=1, columnspan=2)

#create a tags.json file if it doesn't exist
try:
    tags_file = open("tags.json")
except FileNotFoundError:
    tags_dict = {}
    for item in test_dir:
        tags_dict[item] = {"tags": []}
    tags_file = open("tags.json", "w")
    json.dump(tags_dict, tags_file, indent=4)

tags_file = open("tags.json")
tags_dict = json.load(tags_file)

for item in test_dir:
    if item not in tags_dict:
        print("New item found: " + item)
        print("Adding new item to tags_dict")
        tags_dict[item] = {"tags": []}

to_del = []
for key in tags_dict:
    if key not in test_dir:
        print("Suspected Item Deletion of " + key)
        delete_photo = input("Delete entry from tags.json? [y/n]: ")
        if delete_photo.lower() == "y":
            to_del.append(key)

for item in to_del:
    del tags_dict[item]


#makes the image fit the canvas
def resize_photo(in_img):
    width, height = in_img.size
    ratio = width / height
    if ratio > 1:
        in_img = in_img.resize((canvas_width, int(canvas_height/ratio)))
    elif ratio < 1:
        in_img = in_img.resize((int(canvas_width*ratio), canvas_height))
    else:
        in_img = in_img.resize((canvas_width, canvas_height))

    return in_img


#add tag
def add_tag():
    tags.append(e.get())
    print(tags)

#delete tag
def del_tag():
    if e.get() in tags:
        print("Removing tag: " + e.get())
        print(tags)
        tags.remove(e.get())
    else:
        print("tag not found in tags[]")

#store tags, might remove the need for store tags button
def store_tags():
    global tags_dict
    global tags
    tags_dict[test_dir[current_photo]]["tags"] = tags
    print("Written tags to file")

#displays the photo, resizing it before being displayed, and removes the previous image from canvas to prevent memory leak
def display_photo():
    canvas.delete("all")
    global img
    img = ImageTk.PhotoImage(resize_photo(Image.open(path + "/" + test_dir[current_photo])))
    canvas.create_image(0, 0, anchor=NW, image=img)
    print("Current Tags: " + str(tags))

#cycle to next photo
def next_photo():
    global current_photo
    global tags_dict
    global tags
    max_photo = len(test_dir)
    current_photo = (current_photo + 1) % max_photo
    tags = tags_dict[test_dir[current_photo]]["tags"]
    display_photo()

#cycle to previous photo
def prev_photo():
    global current_photo
    global tags_dict
    global tags
    max_photo = len(test_dir)
    current_photo = (current_photo - 1) % max_photo
    tags = tags_dict[test_dir[current_photo]]["tags"]
    display_photo()
    
#jump to a photo by having the filename in the entry
def jump_to_photo():
    global current_photo
    global tags_dict
    global tags
    jump_to = e.get()
    if jump_to not in test_dir:
        print("File not found")
    else:
        current_photo = test_dir.index(jump_to)
        tags = tags_dict[test_dir[current_photo]]["tags"]
        display_photo()

#def disp_tags():

def search_tag():
    search_term = e.get()
    search_list = []
    for key in tags_dict:
        if search_term in tags_dict[key]["tags"]:
            search_list.append(key)
    if not search_list:
        print("No matches found")
    else:
        print(search_list)
    
#create an image and add to canvas
img = ImageTk.PhotoImage(resize_photo(Image.open(path + "/" + test_dir[current_photo])))
canvas.create_image(0, 0, anchor=NW, image=img)

#create frame for housing buttons
f_buttons = Frame(master, width=350)

#create buttons
b_get_tag = Button(f_buttons, text="Get tag!", command=add_tag)
b_del_tag = Button(f_buttons, text="Remove Tag", command=del_tag)
b_store_tags = Button(f_buttons, text="Store Tags!", command=store_tags)
b_next_photo = Button(f_buttons, text="Next photo", command=next_photo)
b_prev_photo = Button(f_buttons, text="Previous photo", command=prev_photo)
b_jump_to_photo = Button(f_buttons, text="Jump to photo", command=jump_to_photo)
b_search_tags = Button(f_buttons, text="Search by tag", command=search_tag)

#create grid for buttons
b_get_tag.grid(row=2, column=0, sticky=E+W)
b_del_tag.grid(row=3, column=0, sticky=E+W)
b_search_tags.grid(row=4, column=0, sticky=E+W)
b_next_photo.grid(row=2, column=1, sticky=E+W)
b_prev_photo.grid(row=3, column=1, sticky=E+W)
b_jump_to_photo.grid(row=4, column=1, sticky=E+W)

f_buttons.grid(row=2, columnspan=2)

tags = tags_dict[test_dir[current_photo]]["tags"]
print(tags)

master.mainloop()
tags_file.close()
tags_file = open("tags.json", "w")
json.dump(tags_dict, tags_file, indent=4)
print("Successfully saved files")
input("Press Enter to close program.")
