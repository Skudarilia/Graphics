from OpenGL.GLUT import *
from OpenGL.GL import *
import math


global lightShiftX  # Перемещение света по Х
global lightShiftY  # Перемещение света по Y
global lightBrightness  # Яркость источника света
global lightColors
global lightColorSelectedIndex
global texture
global step
global lats
global longs
global r
global footAmplifier
global footAmplifierLowerSphere
global footAmplifierDegree
global stickAmplifier
global bulbAmplifier


def drawSphere(lats, longs, r, footAmplifier, footAmplifierDegree, amplifierLowerSphere):
    for i in range(lats):
        lat0 = math.pi * (-0.5 + i / lats)
        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)

        lat1 = math.pi * (-0.5 + (i + 1) / lats)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        if zr0 > r / 4:
            zr0 = (zr0 ** footAmplifierDegree - footAmplifier)
        if zr1 > r / 4:
            zr1 = (zr1 ** footAmplifierDegree - footAmplifier)

        # чтобы убрать нижнюю часть сферы
        if z0 < 0:
            z0 *= amplifierLowerSphere
        if z1 < 0:
            z1 *= amplifierLowerSphere

        glBegin(GL_QUAD_STRIP)
        for j in range(longs + 1):
            lng = 2 * math.pi * (j + 1) / longs
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal(x * zr0, y * zr0, z0)
            # glTexCoord(r * y * zr0, r * z0)
            glVertex(r * x * zr0, r * y * zr0, r * z0)
            glNormal(x * zr1, y * zr1, z1)
            # glTexCoord(r * y * zr1, r * z1)
            glVertex(r * x * zr1, r * y * zr1, r * z1)
        glEnd()
    glDisable(GL_CULL_FACE)


def drawBulb(lats, longs, r):
    for i in range(lats):
        lat0 = math.pi * (-0.5 + i / lats)
        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)

        lat1 = math.pi * (-0.5 + (i + 1) / lats)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)

        if zr0 > r / 4:
            zr0 = (zr0 ** footAmplifierDegree)
        if zr1 > r / 4:
            zr1 = (zr1 ** footAmplifierDegree)

        glBegin(GL_QUAD_STRIP)
        for j in range(longs + 1):
            lng = 2 * math.pi * (j + 1) / longs
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal(x * zr0, y * zr0, z0)
            glVertex(r * x * zr0, r * y * zr0, r * z0)
            glNormal(x * zr1, y * zr1, z1)
            glVertex(r * x * zr1, r * y * zr1, r * z1)
        glEnd()
    glDisable(GL_CULL_FACE)


def onRender():
    global lightShiftX
    global lightShiftY
    global lightBrightness
    global lightColors
    global lightColorSelectedIndex
    global texture
    global lats
    global longs
    global r
    global footAmplifier
    global footAmplifierDegree
    global footAmplifierLowerSphere
    global stickAmplifier
    global bulbAmplifier

    correctionOnBrightness = 1.0 - lightBrightness

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом, который задали в init

    glLightfv(GL_LIGHT0, GL_POSITION, [lightShiftX, lightShiftY, -3.0])  # задаем местоположение источника света
    # задаем цвет излучаемого света
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [
        lightColors[lightColorSelectedIndex][0] - correctionOnBrightness,
        lightColors[lightColorSelectedIndex][1] - correctionOnBrightness,
        lightColors[lightColorSelectedIndex][2] - correctionOnBrightness,
        lightBrightness
    ])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [
        lightColors[lightColorSelectedIndex][0] - correctionOnBrightness,
        lightColors[lightColorSelectedIndex][1] - correctionOnBrightness,
        lightColors[lightColorSelectedIndex][2] - correctionOnBrightness,
        lightBrightness
    ])
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [lightBrightness, lightBrightness, lightBrightness, lightBrightness])

    glPushMatrix()
    # ножка
    glRotated(-90, 1.0, 0.0, 0.0)
    glTranslated(0.0, 0.0, -2.0)
    glEnable(GL_CULL_FACE)
    glEnable(GL_TEXTURE_2D)
    glColor4f(0.5, 0.5, 0.5, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])  # фоновый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])  # отражаемый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.5, 0.5, 0.5])  # диффузионный свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0)  # степень отражаемого света
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # излучаемый свет

    drawSphere(lats, longs, r, footAmplifier / 100, footAmplifierDegree / 10, footAmplifierLowerSphere / 10)

    glDisable(GL_CULL_FACE)
    glDisable(GL_TEXTURE_2D)

    if step == 1 or step == 2:
        # ствол
        glColor4f(0.41, 0.31, 0.05, 1.0)
        glTranslated(0.0, 0.0, 0.5)  # задаем мастоположениевв
        # Устанавливаем материал: рисовать с 2 сторон, тип освещения, цвет
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])  # фоновый свет
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])  # отражаемый свет
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.5, 0.5, 0.5])  # диффузионный свет
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0)  # степень отражаемого света
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # излучаемый свет
        glutSolidCylinder(0.14, stickAmplifier / 10, lats, longs)  # рисуем цилиндр

    if step == 2:
        # лампа
        glTranslated(0.0, 0.0, 2.0 + bulbAmplifier / 250)
        glColor4f(0.6, 0.6, 0.0, 0.0)
        glRotated(90, 0.0, 1.0, 0.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])  # фоновый свет
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])  # отражаемый свет
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.5, 0.5, 0.5])  # диффузионный свет
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0)  # степень отражаемого света
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.2, 0.2, 0.0, 1.0])  # излучаемый свет
        drawBulb(lats, longs, bulbAmplifier / 250)

    glPopMatrix()
    glutSwapBuffers()


def onKeyPress(key, x, y):
    global lightShiftX
    global lightShiftY
    global lightBrightness
    global lightColors
    global lightColorSelectedIndex
    global lats
    global longs
    global r
    global step
    global footAmplifier
    global footAmplifierLowerSphere
    global footAmplifierDegree
    global stickAmplifier
    global bulbAmplifier

    if key == b'w':
        lightShiftY += 0.2
    if key == b's':
        lightShiftY -= 0.2
    if key == b'd':
        lightShiftX += 0.2
    if key == b'a':
        lightShiftX -= 0.2
    if key == GLUT_KEY_UP:
        if lightBrightness < 1.0:
            lightBrightness += 0.1
    if key == GLUT_KEY_DOWN:
        if lightBrightness > 0.0:
            lightBrightness -= 0.1
    if key == GLUT_KEY_RIGHT:
        if lightColorSelectedIndex < (len(lightColors) - 1):
            lightColorSelectedIndex += 1
        else:
            lightColorSelectedIndex = 0
    if key == GLUT_KEY_LEFT:
        if lightColorSelectedIndex > 0:
            lightColorSelectedIndex -= 1
        else:
            lightColorSelectedIndex = len(lightColors) - 1
    if key == b'e':
        if step == 0:
            if 0 <= footAmplifier < 30:
                footAmplifier += 3
                footAmplifierLowerSphere -= 1
                footAmplifierDegree += 15
        elif step == 1:
            if 0 <= stickAmplifier < 20:
                stickAmplifier += 2
        elif step == 2:
            if 0 <= bulbAmplifier < 50:
                bulbAmplifier += 5
    if key == b'q':
        if step == 0:
            if 0 < footAmplifier <= 30:
                footAmplifier -= 3
                footAmplifierLowerSphere += 1
                footAmplifierDegree -= 15
        elif step == 1:
            if 0 < stickAmplifier <= 20:
                stickAmplifier -= 2
        elif step == 2:
            if 0 < bulbAmplifier <= 50:
                bulbAmplifier -= 5

    if step == 0:
        if footAmplifier >= 30:
            step += 1
    elif step == 1:
        if stickAmplifier >= 20:
            step += 1
        elif stickAmplifier <= 0:
            step -= 1
    elif step == 2:
        if bulbAmplifier <= 0:
            step -= 1
    else:
        step = 0
        footAmplifier = 0
        footAmplifierLowerSphere = 10
        footAmplifierDegree = 10
        stickAmplifier = 0
        bulbAmplifier = 0

    glutPostRedisplay()


def init():
    global lightShiftX
    global lightShiftY
    global lightBrightness
    global lightColors
    global lightColorSelectedIndex
    global texture
    global step
    global lats
    global longs
    global r
    global footAmplifier
    global footAmplifierLowerSphere
    global footAmplifierDegree
    global stickAmplifier
    global bulbAmplifier

    lightShiftX = -3.0
    lightShiftY = 3.0
    lightBrightness = 1.0
    lightColors = [
        [1.0, 1.0, 1.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.55, 0.0, 1.0]
    ]
    lightColorSelectedIndex = 0
    step = 0
    # sphere init
    lats = 100
    longs = 100
    r = 0.5
    footAmplifier = 0  # from 0 to 10
    footAmplifierLowerSphere = 10  # from 10 to 0
    footAmplifierDegree = 10  # from 10 to 160
    stickAmplifier = 0  # from 0 to 20
    bulbAmplifier = 0  # from 0 to 50

    glClearColor(0.4, 0.4, 0.4, 1.0)  # Серый цвет для изначальной закраски
    glOrtho(-3.0, 3.0, -3.0, 3.0, -3.0, 3.0)  # Определяем границы рисования
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [lightBrightness, lightBrightness, lightBrightness,
                                            lightBrightness])  # Определяем текущую модель освещения
    glEnable(GL_LIGHTING)  # включаем освещение
    glEnable(GL_LIGHT0)  # включаем один источник света
    glLightfv(GL_LIGHT0, GL_POSITION, [lightShiftX, lightShiftY, -3.0])  # Определяем положение источника света
    glEnable(GL_NORMALIZE)  # нормализуем, для воизбежания артифактов
    glEnable(GL_COLOR_MATERIAL)  # Разрешаем перекрашивание материлов
    glCullFace(GL_BACK)  # Задаем отброс фронтовой стороны полигона. Работает только когда включен GL_CULL_FACE


glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(500, 100)
glutInit(sys.argv)
glutCreateWindow("lab3 Skudar")
glutDisplayFunc(onRender)
glutSpecialFunc(onKeyPress)
glutKeyboardFunc(onKeyPress)
init()
glutMainLoop()
