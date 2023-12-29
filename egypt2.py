import tkinter as tk
from tkinter import *
from tkinter import messagebox
from vpython import box, vector, color, canvas, rate, sphere,sleep
from random import randint
from itertools import combinations, chain
from time import sleep
import requests
from io import BytesIO
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk




root = Tk()
root.title("Egyptian Aspheera Globes Game")
root.geometry('600x600')








def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return ImageTk.PhotoImage(Image.open(BytesIO(response.content)).convert("RGBA"))
    else:
        return None

image_url = "https://image.winudf.com/v2/image/Y29tLm9uZXRlbmdhbWVzLmFuY2llbnQuZWd5cHQucHlyYW1pZC5jb25zdHJ1Y3Rpb24uYnVpbGRlcmdhbWVzLnNpbXVsYXRpb25fc2NyZWVuXzNfanZycGsxbTQ/screen-3.jpg?fakeurl=1&type=.jpg"
bg_image = download_image(image_url)

# Add a label with instructions on how to play
instructions_text= """How to Play:
- Move the camera:
    - Forward: Press 'W'
    - Backward: Press 'S'
    - Left: Press 'A'
    - Right: Press 'D'
- Jump: Press the 'Space' key.
- Change altitude: Use the 'Q' key to move up and the 'E' key to move down.
- Rotate camera:
    - Rotate Left: Press 'Left Arrow' key
    - Rotate Right: Press 'Right Arrow' key
    - Rotate Up: Press 'Up Arrow' key
    - Rotate Down: Press 'Down Arrow' key
- Collect treasures: Move the camera close to a red treasure to collect it.
- Your goal: Collect all the red Egyptian Aspheera globes to win the game."""


  




# Add a label for the story
story_text = """In the heart of ancient Egypt, there exists a mystical land called Aspheera, known for its magical red globes. These extraordinary orbs are said to hold immense power, capable of granting the possessor unimaginable abilities.

Legend has it that the one who gathers all the red Egyptian Aspheera globes will be bestowed with ultimate wisdom and control over the elements. Many adventurers have embarked on this perilous journey to claim these magical spheres, but none have returned.

You, a brave and skilled explorer, have now set foot on this mystical land, determined to unravel its secrets. As you navigate through treacherous deserts and mysterious pyramids, you encounter challenges and puzzles that guard the coveted globes.

Your quest to collect the red Egyptian Aspheera globes begins now. Do you have what it takes to triumph over the ancient trials and emerge as the true master of Aspheera?

Press the 'Start Game' button to begin your extraordinary journey or 'Stop Game' to rest and reflect on the mysteries that await."""

story_label = Label(root, text=story_text, wraplength=500, font=("Helvetica", 14))
story_label.place(x=20, y=200)

def thegame():

    def find_pyramids(cubes):
        c = int(cubes ** 0.5)
        pyramids = []
        h = []
        le = []
        lo = []

        def H(cubes, c):
            for n in range(c, 1, -1):
                total_cubes = pyramid_cubes(n)
                if total_cubes <= cubes:
                    h.append([[n, "H"], total_cubes])

        def pyramid_cubes(n):
            return (n * (n + 1) * (2 * n + 1)) // 6

        def Leven(cubes, c):
            for n in range(c, 1, -1):
                total_cubes = (2 * n * (n + 1) * (2 * n + 1)) // 3
                if total_cubes <= cubes:
                    le.append([[2 * n, "L"], total_cubes])

        def Lodd(cubes, c):
            for n in range(c, 0, -1):
                total_cubes = (n * (2 * n + 1) * (2 * n - 1)) // 3
                if total_cubes <= cubes:
                    lo.append([[2 * n - 1, "L"], total_cubes])

        H(cubes, c)
        Leven(cubes, c)
        Lodd(cubes, c)
        l = h + le + lo
        l1 = list(chain.from_iterable(combinations(l, r) for r in range(len(l) + 1)))
        l1 = l1[1:]

        for i in l1:
            u = 0
            for j in i:
                u += j[1]
            if u == cubes:
                pyramids.append(list(i))
                break

        if not pyramids:
            return False

        j = []
        p=pyramids[0]
        for i in p:
            j.append(tuple(i[0]))
        return j
    
    def hex_to_rgb(hex_color):
        hex_color = hex_color.strip("#")
        return vector(int(hex_color[0:2], 16) / 255.0, int(hex_color[2:4], 16) / 255.0, int(hex_color[4:6], 16) / 255.0)

    def build_pyramid(num_cubes):
        scene = canvas(width=800, height=600, background=vector(0.93, 0.79, 0.69))
        colors_hex = ["#F5D3A5", "#C2985E", "#7A4F25", "#EDC9AF"]
        colors = [hex_to_rgb(hex_color) for hex_color in colors_hex]
        cube_size=2.5
        gap=5
        offset_x=0
        pyramid_height = 1

        for base, pyramid_type in find_pyramids(num_cubes):
            if pyramid_type == "H":
                pyramid_height=(base * (base + 1) * (2 * base + 1)) // 6
                for level in range(base, 0, -1):
                    layer_offset = (base - level) * 2.5 / 2
                    for row in range(level):
                        for col in range(level):
                            z_pos = col * cube_size - (level - 1) * cube_size / 2 
                            x_pos = row * cube_size - (level - 1) * cube_size / 2 +offset_x
                            y_pos = (base - level) * cube_size  / 2
                            cube_color = colors[(row + col) % 4]
                            edge_color = color.black
                            box(pos=vector(x_pos, y_pos, z_pos), size=vector(cube_size,cube_size,cube_size), color=cube_color, opacity=0.7, edgecolor=edge_color)
                            
                offset_x+=base*cube_size+gap
            elif pyramid_type == "L":
                for level in range(base, 0, -2):
                    if base%2==0:
                        pyramid_height=((2 * base * (base + 1) * (2 * base + 1)) // 3)//2
                    elif base%2!=0:
                        pyramid_height=((base * (2 * base + 1) * (2 * base - 1)) // 3)//2
                    layer_offset = (base - level) * 2.5 / 2
                    for row in range(level):
                        for col in range(level):
                            z_pos = col * cube_size - (level - 1) * cube_size / 2 
                            x_pos = row * cube_size - (level - 1) * cube_size / 2 +offset_x
                            y_pos = (base - level) * cube_size / 2
                            cube_color = colors[(row + col) % 4]
                            edge_color = color.black
                            box(pos=vector(x_pos, y_pos, z_pos), size=vector(cube_size, cube_size, cube_size), color=cube_color, opacity=0.7, edgecolor=edge_color)
                            
                offset_x+=base*cube_size+gap
        return scene

    def check_treasure_collection(scene, treasures):
        player_pos = scene.camera.pos
        collected_treasures = []
        for treasure in treasures[:]:  # Use [:] to create a copy of the list to avoid modification during iteration
            if is_close_to_treasure(player_pos, treasure.pos):
                treasure.visible = False
                collected_treasures.append(treasure)
        return collected_treasures


    def is_close_to_treasure(p1, p2):
        # Check if the distance between two points is less than a threshold (1.5 in this case)
        return distance(p1, p2) < 1.5

    def create_treasures(scene, num_cubes, num_treasures):
        treasures = []
        for _ in range(num_treasures):
            x = randint(-num_cubes//2, num_cubes//2)
            y = randint(1, num_cubes)
            z = randint(-num_cubes//2, num_cubes//2)
            treasure = sphere(pos=vector(x, y, z), radius=0.5, color=color.red)
            treasures.append(treasure)

        return treasures
    # Helper function to get the forward and right directions relative to the camera
    def get_forward_right(scene):
        forward = scene.camera.axis
        right = forward.cross(vector(0, 1, 0))
        return forward, right


    def distance(p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5

    def jump():
        global jumping, jump_speed, initial_y  # Make the 'jumping' variable global
        if jumping:
            scene.camera.pos.y += jump_speed
            jump_speed -= 0.02
            if scene.camera.pos.y <= initial_y:
                scene.camera.pos.y = initial_y
                jumping = False


    def handle_movement(scene, keys, speed):
        forward, right = get_forward_right(scene)
        direction = keys.key
        if direction == 'w':
            scene.camera.pos += forward * speed
        elif direction == 's':
            scene.camera.pos -= forward * speed
        elif direction == 'a':
            scene.camera.pos -= right * speed
        elif direction == 'd':
            scene.camera.pos += right * speed

    def open_game_window(root, num_cubes, player_name):
        #game_window = tk.Toplevel(root)
        #ame_window.title("Treasure Hunt")
        #game_window.geometry("800x600")
        global jumping

        scene = build_pyramid(num_cubes)
        treasures = create_treasures(scene, num_cubes, num_cubes)

        # Camera movement speed
        speed = 0.2

        # Jumping variables
        jump_height = 2.0
        jumping = False

        # Altitude control variables
        altitude_speed = 0.5

        # Camera rotation speed
        rotation_speed = 0.1

        # Player points
        points = 0

        # Create a label to show points in the canvas
        points_display = canvas(
            title="Treasure Hunt", width=800, height=600, background=color.black, align='left', text=f"Points: {points}"
        )

        while True:
            rate(60)  # Increase the frame rate for smoother animation

            collected_treasures = check_treasure_collection(scene, treasures)
            for treasure in collected_treasures:
                treasures.remove(treasure)
                if not treasures:
                    if num_cubes <= 8:
                        result_text = f"Congratulations, {player_name}! You collected all treasures. Case 1: {points}H {num_cubes}L {points + num_cubes * 10}"
                    else:
                        result_text = f"Sorry, {player_name}. It's impossible to collect all treasures with {num_cubes} cubes. Case 2: impossible"
                    points_display.text = result_text
                    messagebox.showinfo("Game Over", result_text)
                    scene.delete()  # Close the scene after the game ends
                    return

            keys = scene.waitfor('keydown')
            if keys.event == 'keydown':
                if keys.key in ['w', 's', 'a', 'd']:
                    handle_movement(scene, keys, speed)
                elif keys.key == 'space' and not jumping:
                    jumping = True
                    initial_y = scene.camera.pos.y
                    jump_speed = 0.5
                elif keys.key == 'q':
                    scene.camera.pos += vector(0, altitude_speed, 0)
                elif keys.key == 'e':
                    scene.camera.pos += vector(0, -altitude_speed, 0)
                elif keys.key == 'left':
                    scene.camera.rotate(angle=rotation_speed, axis=vector(0, 1, 0))
                elif keys.key == 'right':
                    scene.camera.rotate(angle=-rotation_speed, axis=vector(0, 1, 0))
                elif keys.key == 'up':
                    scene.camera.rotate(angle=rotation_speed, axis=scene.camera.axis.cross(vector(0, 1, 0)))
                elif keys.key == 'down':
                    scene.camera.rotate(angle=-rotation_speed, axis=scene.camera.axis.cross(vector(0, 1, 0)))

            jump()


            # Check if all treasures are collected
            if not treasures:
                if num_cubes <= 8:
                    result_text = f"Congratulations, {player_name}! You collected all treasures. Case 1: {points}H {num_cubes}L {points + num_cubes * 10}"
                else:
                    result_text = f"Sorry, {player_name}. It's impossible to collect all treasures with {num_cubes} cubes. Case 2: impossible"
                points_display.text = result_text  # Update points display
                messagebox.showinfo("Game Over", result_text)
                break


    def start_treasure_hunt():
        root = tk.Tk()
        root.title("Treasure Hunt")
        root.geometry("300x200")

        def on_start_game():
            num_cubes = int(num_cubes_entry.get())
            player_name = player_name_entry.get()

            if num_cubes < 3:
                messagebox.showerror("Invalid Input", "The number of cubes must be 3 or greater.")
            elif not player_name:
                messagebox.showerror("Invalid Input", "Please enter your name.")
            else:
                pyramids_combination = find_pyramids(num_cubes)
                if pyramids_combination:
                    messagebox.showinfo("Pyramid Combinations", f"Possible Pyramid Combination: {pyramids_combination}")
                    open_game_window(root, num_cubes, player_name)  # Pass 'root' as an argument
                else:
                    messagebox.showinfo("Pyramid Combinations", f"It's impossible to create {num_cubes} cubes with pyramids.")


        description_label = tk.Label(root, text="Welcome to the Treasure Hunt!\nAn Egyptian-themed game.", wraplength=250)
        description_label.pack(pady=10)

        player_name_label = tk.Label(root, text="Enter your name:")
        player_name_label.pack(pady=5)

        player_name_entry = tk.Entry(root)
        player_name_entry.pack(pady=5)

        num_cubes_label = tk.Label(root, text="Enter the number of cubes for the pyramid (3 or greater):")
        num_cubes_label.pack(pady=5)

        num_cubes_entry = tk.Entry(root)
        num_cubes_entry.pack(pady=5)

        start_game_button = tk.Button(root, text="Start Game", command=on_start_game)
        start_game_button.pack(pady=10)

        root.mainloop()

    start_treasure_hunt()

def start_game():
    thegame()
    pass

def stop_game():
    scene.delete()
    pass


# Add labels
title_label = Label(root, text="Egyptian Aspheera Globes Game", font=("Helvetica", 20))
title_label.pack()

# Add buttons
start_button = Button(root, text="Start Game", command=start_game, width=15, height=2, bg="#FF5733", fg="white", font=("Helvetica", 14, "bold"))
start_button.place(x=120, y=34)

stop_button = Button(root, text="Stop Game", command=stop_game, width=15, height=2, bg="#C70039", fg="white", font=("Helvetica", 14, "bold"))
stop_button.place(x=120, y=100)




root.mainloop()

