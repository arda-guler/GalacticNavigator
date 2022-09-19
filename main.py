import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

import keyboard

import os

from graphics import *
from loader import *
from star import *
from camera import *
from ui_text import *
from vector3 import *

def window_resize(window, width, height):
    glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)

def clear_cmd_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def main():
    global vp_size_changed
    star_data = read_data("hygdata_v3.csv")

    window_x = 1000
    window_y = 600
    near_clip = 1
    far_clip = 20000
    fov = 70
    point_size = 2
    
    cam_strafe_speed = 2
    cam_rotate_speed = 5
    cam_pitch_down = "W"
    cam_pitch_up = "S"
    cam_yaw_left = "A"
    cam_yaw_right = "D"
    cam_roll_ccw = "Q"
    cam_roll_cw = "E"
    cam_strafe_up = "U"
    cam_strafe_down = "O"
    cam_strafe_right = "L"
    cam_strafe_left = "J"
    cam_strafe_forward = "I"
    cam_strafe_backward = "K"

    incr_dist = "T"
    decr_dist = "G"

    use_command_line = "C"
    
    glfw.init()
    window = glfw.create_window(int(window_x),int(window_y),"Galactic Navigator", None, None)
    glfw.set_window_pos(window,100,100)
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    
    gluPerspective(fov, int(window_x)/int(window_y), near_clip, far_clip)
    glEnable(GL_CULL_FACE)
    glEnable(GL_POINT_SMOOTH)
    glPointSize(point_size)

    cam = camera("main_cam", [0,0,0], [[1,0,0],[0,1,0],[0,0,1]], True)
    cam.move([0,0,-10])

    max_dist = 64

    # available travel modes are 'commute' and 'sightseeing'
    travel_mode = "commute"
    max_jump = 10/3.262 # ly/3.262 = parsecs
    travel_speed = 0.9 # c
    stay_time = 0.25 # years

    system_start = None
    system_destination = None
    waypoints = []
    
    def get_dist_between(star1, star2):
        return ( (star1.x-star2.x)**2 + (star1.y-star2.y)**2 + (star1.z-star2.z)**2 )**(0.5)

    def get_stars_within(origin, dist):
        cstars = []
        for star in star_data:
            if (not star == origin) and get_dist_between(origin, star) < dist:
                cstars.append(star)

        return cstars

    def find_system_by_name(sysname):
        for star in star_data:
            if star.proper == sysname or star.hyg == sysname:
                return star

        print("Star system", sysname, "could not be found!")
        return None

    def compute_route():
        route = []
        route.append(system_start)

        if travel_mode == "commute":

            while not system_destination in route:
                cstars = get_stars_within(route[-1], max_jump)

                if system_destination in cstars:
                    route.append(system_destination)

                    # compute route properties
                    target_dist = get_dist_between(system_start, system_destination)
                    total_distance_covered = 0
                    for si in range(len(route)):
                        if si > 0:
                            total_distance_covered += get_dist_between(route[si-1], route[si])

                    total_stay_time = (len(route)-1) * stay_time
                    move_time = (total_distance_covered/travel_speed)
                    travel_time = (total_distance_covered/travel_speed) + (len(route)-1) * stay_time

                    print("\nRoute: ", end="")
                    for st in route:
                        if not st.proper:
                            print("HYG", st.hyg, end="")
                        else:
                            print(st.proper + " (HYG " + st.hyg + ")", end="")

                        if not st == route[-1]:
                            print(" --> ", end="")
                        else:
                            print("")

                    print("INPUT Travel speed (c) = ", travel_speed)
                    print("INPUT Stay time (years) = ", stay_time)
                    print("Target distance (ly):", target_dist/3.262)
                    print("Route length (ly):", total_distance_covered/3.262)
                    print("Total travel time (years):", travel_time)
                    print("Total in-system stay time (years):", total_stay_time)
                    print("Total time spent in interstellar medium (years):", move_time)
                    return route

                else:
                    travel_direction = vec3(system_destination.x, system_destination.y, system_destination.z) - vec3(route[-1].x, route[-1].y, route[-1].z)

                    best_attempt = None
                    best_system = None

                    for cstar in cstars:
                        if not best_attempt or get_dist_between(cstar, system_destination) < best_attempt:
                            best_attempt = get_dist_between(cstar, system_destination)
                            best_system = cstar

                    if best_system in route:
                        print("Can not plot route! Try increasing max jump distance.")
                        input("Press Enter to continue...")
                        return []

                    if best_system:
                        route.append(best_system)
                            
                    else:
                        print("Can not plot route! Try increasing max jump distance.")
                        input("Press Enter to continue...")
                        return []

            return route

    clear_cmd_terminal()
    print("Press", use_command_line, "to enter a command.")
    while not glfw.window_should_close(window):
            
        cam.rotate([(keyboard.is_pressed(cam_pitch_down) - keyboard.is_pressed(cam_pitch_up)) * cam_rotate_speed,
                    (keyboard.is_pressed(cam_yaw_left) - keyboard.is_pressed(cam_yaw_right)) * cam_rotate_speed,
                    (keyboard.is_pressed(cam_roll_ccw) - keyboard.is_pressed(cam_roll_cw)) * cam_rotate_speed])

        cam.move([(keyboard.is_pressed(cam_strafe_left) - keyboard.is_pressed(cam_strafe_right)) * cam_strafe_speed,
                  (keyboard.is_pressed(cam_strafe_down) - keyboard.is_pressed(cam_strafe_up)) * cam_strafe_speed,
                  (keyboard.is_pressed(cam_strafe_forward) - keyboard.is_pressed(cam_strafe_backward)) * cam_strafe_speed])

        if keyboard.is_pressed(incr_dist):
            max_dist *= 2
        elif keyboard.is_pressed(decr_dist):
            max_dist *= 0.5

        if keyboard.is_pressed(use_command_line):
            flush_input()
            frame_cmd = input(" > ")
        else:
            frame_cmd = ""

        # - - - COMMAND INTERPRETER - - -
        if frame_cmd:
            
            frame_cmd = frame_cmd.split(" ")
            frame_cmd[0] = frame_cmd[0].lower()
            
            if frame_cmd[0] == "set_start":
                system_start = find_system_by_name(frame_cmd[1])

            elif frame_cmd[0] == "set_destination":
                system_destination = find_system_by_name(frame_cmd[1])

            elif frame_cmd[0] == "set_max_jump":
                max_jump = float(frame_cmd[1])

            elif frame_cmd[0] == "set_travel_speed":
                travel_speed = float(frame_cmd[1])

            elif frame_cmd[0] == "set_stay_time":
                stay_time = float(frame_cmd[1])

            elif frame_cmd[0] == "set_max_jump":
                max_jump = float(frame_cmd[1]/3.262)

            elif frame_cmd[0] == "set_mode":
                travel_mode = frame_cmd[1]

            elif frame_cmd[0] == "compute":
                waypoints = compute_route()

            elif frame_cmd[0] == "h" or frame_cmd[0] == "help":
                print("")
                print("Congrats! You entered a command! Any commands can be entered this way.")
                print("Available commands: 'set_start <star_system_name>', 'set_destination <star_system_name>', 'compute', 'set_max_jump <number>', 'set_travel_speed <number>', 'set_stay_time <number>'")
                print("")

            else:
                pass
        
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawOrigin()
        drawStars(star_data, cam, max_dist)
        drawRoute(waypoints, cam)
        render_numbers(str(max_dist), [0,1,0], [-11,6], cam, 0.2)
        glfw.swap_buffers(window)

main()
