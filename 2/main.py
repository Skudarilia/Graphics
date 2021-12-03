import numpy
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *
from PIL import Image

global lightShiftX  # Перемещение света по Х
global lightShiftY  # Перемещение света по Y
global lightBrightness  # Яркость источника света
global lightColors
global lightColorSelectedIndex
global texture


def getTextureIdByPath(filename):
    img = Image.open(filename)
    img = img.convert("RGBA").rotate(180)
    imgData = numpy.array(list(img.getdata()), numpy.int8)

    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, imgData)
    return textureID


def onRender():
    global lightShiftX
    global lightShiftY
    global lightBrightness
    global lightColors
    global lightColorSelectedIndex
    global texture

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

    # Cylinder
    glColor4f(0.1, 0.3, 0.8, 1.0)
    glPushMatrix()
    glTranslated(1.5, -1.0, 0.0)
    glRotated(-90, 1.0, 0.0, 0.0)  # задаем поворот фигуры
    glRotated(180, 0.0, 0.0, 1.0)
    glRotated(25, 1.0, 0.0, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])  # фоновый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # отражаемый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])  # диффузионный свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 128.0)  # степень отражаемого света
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # излучаемый свет
    glutSolidCylinder(1.0, 2.5, 100, 100)
    glPopMatrix()

    # Sphere with texture
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glColor4f(0.5, 0.5, 0.5, 0.0)
    glPushMatrix()
    glTranslated(-1.5, 1.5, 0.0)
    glRotated(-90, 1.0, 0.0, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])  # фоновый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])  # отражаемый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])  # диффузионный свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0)  # степень отражаемого света
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # излучаемый свет
    sphere = gluNewQuadric()
    gluQuadricDrawStyle(sphere, GLU_FILL)
    gluQuadricTexture(sphere, GL_TRUE)
    gluQuadricNormals(sphere, GLU_SMOOTH)
    gluSphere(sphere, 1, 100, 100)
    gluDeleteQuadric(sphere)
    glPopMatrix()
    glDisable(GL_CULL_FACE)
    glDisable(GL_TEXTURE_2D)

    # Cone
    glDepthMask(GL_FALSE)
    glEnable(GL_BLEND)  # включаем функцию блендинга
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1., 0.85, 0.73, 0.5)
    glPushMatrix()
    glTranslated(-1.5, -2.0, 0.0)
    glRotated(-90, 1.0, 0.0, 0.0)
    glRotated(-25, 1.0, 0.0, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])  # фоновый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])  # отражаемый свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])  # диффузионный свет
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 0)  # степень отражаемого света
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # излучаемый свет
    glutSolidCone(1.0, 2.0, 100, 100)
    glPopMatrix()
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)

    glutSwapBuffers()


def onKeyPress(key, x, y):
    global lightShiftX
    global lightShiftY
    global lightBrightness
    global lightColors
    global lightColorSelectedIndex

    if key == b'w':
        lightShiftY += 0.2
        print('Pressed W')
    if key == b's':
        lightShiftY -= 0.2
        print('Pressed S')
    if key == b'd':
        lightShiftX += 0.2
        print('Pressed D')
    if key == b'a':
        lightShiftX -= 0.2
        print('Pressed A')
    if key == GLUT_KEY_UP:
        if lightBrightness < 1.0:
            lightBrightness += 0.1
        print('Pressed UP')
    if key == GLUT_KEY_DOWN:
        if lightBrightness > 0.0:
            lightBrightness -= 0.1
        print('Pressed DOWN')
    if key == GLUT_KEY_LEFT:
        if lightColorSelectedIndex > 0:
            lightColorSelectedIndex -= 1
        else:
            lightColorSelectedIndex = len(lightColors) - 1
        print('Pressed LEFT')
    if key == GLUT_KEY_RIGHT:
        if lightColorSelectedIndex < (len(lightColors) - 1):
            lightColorSelectedIndex += 1
        else:
            lightColorSelectedIndex = 0
        print('Pressed RIGHT')

    glutPostRedisplay()


def init():
    global lightShiftX
    global lightShiftY
    global lightBrightness
    global lightColors
    global lightColorSelectedIndex
    global texture

    lightShiftX = 0.0
    lightShiftY = 3.0
    lightBrightness = 1.0
    lightColors = [
        [1.0, 1.0, 1.0],
        [1.0, 1.0, 0.5],
        [1.0, 1.0, 0.0],
        [1.0, 0.5, 1.0],
        [1.0, 0.0, 1.0],
        [0.5, 1.0, 1.0],
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.5, 0.3, 0.5]
    ]
    lightColorSelectedIndex = 0
    texture = getTextureIdByPath('003.jpg')

    glClearColor(0.2, 0.2, 0.2, 1.0)  # Серый цвет для изначальной закраски
    glOrtho(-3.0, 3.0, -3.0, 3.0, -3.0, 3.0)  # Определяем границы рисования
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [lightBrightness, lightBrightness, lightBrightness, lightBrightness])  # Определяем текущую модель освещения
    glEnable(GL_LIGHTING)  # включаем освещение
    glEnable(GL_LIGHT0)  # включаем один источник света
    glLightfv(GL_LIGHT0, GL_POSITION, [lightShiftX, lightShiftY, -3.0])  # Определяем положение источника света
    glEnable(GL_NORMALIZE)  # нормализуем, для воизбежания артифактов
    glEnable(GL_COLOR_MATERIAL)  # Разрешаем перекрашивание материлов
    glCullFace(GL_FRONT)  # Задаем отброс фронтовой стороны полигона. Работает только когда включен GL_CULL_FACE


glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutInitWindowPosition(500, 100)
glutInit(sys.argv)
glutCreateWindow("2")
glutDisplayFunc(onRender)
glutSpecialFunc(onKeyPress)
glutKeyboardFunc(onKeyPress)
init()
glutMainLoop()
