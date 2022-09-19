import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import glfw

from math_utils import *
from ui_text import *

def drawOrigin():
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3f(0,0,0)
    glVertex3f(0,3,0)
    glColor(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(3,0,0)
    glColor(0,0,1)
    glVertex3f(0,0,0)
    glVertex3f(0,0,3)
    glEnd()

def drawStars(stars, cam, max_dist=None):
    
    for star in stars:
        if max_dist and ((star.x + cam.pos[0])**2 + (star.y + cam.pos[1])**2 + (star.z + cam.pos[2])**2)**(0.5) > max_dist:
            pass
        elif float(star.dist) >= 100000:
            pass
        else:
            x = float(star.x)
            y = float(star.y)
            z = float(star.z)

            lum = float(star.lum)
            bright = max(min(lum, 10), 4) / 10

            if star.spect:
                main_spect = star.spect[0]

                if main_spect == "O":
                    glColor(0, bright * 0.1, bright)
                elif main_spect == "B":
                    glColor(0, bright * 0.4, bright)
                elif main_spect == "A":
                    glColor(bright * 0.85, bright * 0.85, bright)
                elif main_spect == "F":
                    glColor(bright, bright, bright)
                elif main_spect == "G":
                    glColor(bright, bright * 0.8, bright * 0.8)
                elif main_spect == "K":
                    glColor(bright, bright * 0.6, bright * 0.6)
                elif main_spect == "M":
                    glColor(bright, bright * 0.2, bright * 0.2)
                else:
                    glColor(bright, bright, bright)
                    
            else:
                glColor(bright, bright, bright)
            
            glBegin(GL_POINTS)
            glVertex3f(x, y, z)
            glEnd()

def drawRoute(waypoints, cam):
    if not waypoints:
        return

    glColor(0,1,1)

    glBegin(GL_LINE_STRIP)
    for wp in waypoints:
        glVertex3f(wp.x, wp.y, wp.z)
    glEnd()

    for wp in waypoints:
        if world2cam(wp.pos, cam):
            label_render_start = world2cam(wp.pos, cam)
            label_render_start[0] += 0.2
            label_render_start[1] -= 0.2

            lum = float(wp.lum)
            bright = max(min(lum, 10), 4) / 10

            if wp.spect:
                main_spect = wp.spect[0]

                if main_spect == "O":
                    wp_color = (0, bright * 0.1, bright)
                elif main_spect == "B":
                    wp_color = (0, bright * 0.4, bright)
                elif main_spect == "A":
                    wp_color = (bright * 0.85, bright * 0.85, bright)
                elif main_spect == "F":
                    wp_color = (bright, bright, bright)
                elif main_spect == "G":
                    wp_color = (bright, bright * 0.8, bright * 0.8)
                elif main_spect == "K":
                    wp_color = (bright, bright * 0.6, bright * 0.6)
                elif main_spect == "M":
                    wp_color = (bright, bright * 0.2, bright * 0.2)
                else:
                    wp_color = (bright, bright, bright)
                    
            else:
                wp_color = (bright, bright, bright)

            if wp.proper:
                render_AN(wp.proper, vector_scale(wp_color, 2), label_render_start, cam)
            else:
                render_AN(("HYG " + wp.hyg), vector_scale(wp_color, 2), label_render_start, cam)
