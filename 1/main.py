from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys


def display_all():
    j = 0.00
    k = 1.00
    for i in range(6401):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # Сфера
        color = [1., 0., 0., 1.]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glutWireSphere(5*(1-j), 20, 20)  # Масштабирование сферы
        # glutWireSphere(5 * 0.75, 20, 20)  # проверка

        if i % 256 == 0:  # 6400 / 25 = 256
            j = j + 0.01

        # Куб
        color = [0., 0., 1., 1.]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glTranslate(0, 20, -20)
        glutSolidCube(6)

        # Конус
        color = [0., 1., 1., 1.]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glTranslate(3, 3, 3)  # Смещаем на вершину куба
        glutSolidCone(2 * k, 4 * k, 20, 12)

        if i % 427 == 0: # 6400 // 427 = 15
            k = k + 0.1

        # Цилиндр
        color = [1., 1.0, 0., 1.]
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
        glTranslate(0, -23, 12) # Смещение цилиндра, чтобы центры фигур совпадали
        if i > 40:
            glTranslate(0, 0, -i/160) # Смещение цилиндра
        glutWireCylinder(5, 10, 20, 10) # radius, height

        glPopMatrix()
        glutSwapBuffers()

    return


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 1000)
    glutCreateWindow(b'1')
    glClearColor(0.6, 0.6, 0.6, 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING) # отвечает за цвет
    glEnable(GL_LIGHT0)

    glutDisplayFunc(display_all)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(90., 1., 1., 100.) # искажает пропроции
    # gluOrtho2D(-100, 100, -100, 100)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(40, 0, 0, # eye perspective 40 0 -20
              0, 0, -20, # center 0 0 -20
              0, 0, 1) # up 0 0 1
    glPushMatrix()
    glutMainLoop()
    return


main()
