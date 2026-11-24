import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# --------------------------
# GLOBAL VARIABLES
# --------------------------
camera_angle_x = 20
camera_angle_y = 30
camera_distance = 10

time_of_day = 9.0   # 6.0 → 18.0 (6 AM → 6 PM)

# --------------------------
# INITIAL SETUP
# --------------------------
def init():
    glEnable(GL_DEPTH_TEST)

    # Enable lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    # Enable color material (so glColor works with lighting)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Background color
    glClearColor(0.5, 0.7, 1.0, 1.0)


# --------------------------
# SUN LIGHT (DIRECTIONAL)
# --------------------------
def update_light():
    global time_of_day

    # Convert time → angle (6AM–6PM → 0°–180°)
    angle = (time_of_day - 6) / 12 * math.pi

    # Light direction
    x = math.cos(angle)
    y = math.sin(angle)
    z = -0.5

    light_pos = [x, y, z, 0.0]  # 0 = directional light

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.9, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])


# --------------------------
# DRAW ROOM (FLOOR + WALLS)
# --------------------------
def draw_room():
    # Floor
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glEnd()

    # Back wall
    glColor3f(0.7, 0.7, 0.9)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, -5)
    glEnd()

    # Left wall
    glColor3f(0.9, 0.7, 0.7)
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    glEnd()


# --------------------------
# DRAW SIMPLE DESK
# --------------------------
def draw_desk():
    glPushMatrix()
    glTranslatef(0, 1, 0)

    glColor3f(0.5, 0.3, 0.1)
    glutSolidCube(2)

    glPopMatrix()


# --------------------------
# CAMERA
# --------------------------
def set_camera():
    glLoadIdentity()

    # Convert angles to radians
    rad_x = math.radians(camera_angle_x)
    rad_y = math.radians(camera_angle_y)

    # Camera position
    eye_x = camera_distance * math.cos(rad_x) * math.sin(rad_y)
    eye_y = camera_distance * math.sin(rad_x)
    eye_z = camera_distance * math.cos(rad_x) * math.cos(rad_y)

    gluLookAt(eye_x, eye_y, eye_z,
              0, 0, 0,   # look at center
              0, 1, 0)   # up vector


# --------------------------
# DISPLAY
# --------------------------
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    set_camera()
    update_light()

    draw_room()
    draw_desk()

    glutSwapBuffers()


# --------------------------
# KEYBOARD CONTROLS
# --------------------------
def keyboard(key, x, y):
    global camera_angle_x, camera_angle_y, time_of_day

    key = key.decode("utf-8")

    if key == 'w':
        camera_angle_x += 5
    elif key == 's':
        camera_angle_x -= 5
    elif key == 'a':
        camera_angle_y -= 5
    elif key == 'd':
        camera_angle_y += 5

    elif key == 'q':
        time_of_day += 0.5
    elif key == 'e':
        time_of_day -= 0.5

    # Clamp time
    time_of_day = max(6.0, min(18.0, time_of_day))

    glutPostRedisplay()


# --------------------------
# RESHAPE
# --------------------------
def reshape(w, h):
    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w / h if h != 0 else 1, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)


# --------------------------
# MAIN
# --------------------------
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Solar Lighting Simulation")

    init()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutMainLoop()


if __name__ == "__main__":
    main()