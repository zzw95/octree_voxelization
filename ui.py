import wx
import sys
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
import octree_1


# https://stackoverflow.com/questions/19893734/how-to-combine-wxpython-matplotlib-and-pyopengl
# http://www.siafoo.net/snippet/97

class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)

        # initial mouse position
        self.lastx = self.x = 0
        self.lasty = self.y = 0
        self.size = None
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

        tree = octree_1.Octree("ball.stl")
        self.bounding_box = tree.bounding_box
        tree.traverse()
        self.voxelBoxes = tree.voxelBoxes


    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(True)
            self.OnDraw()

class CubeCanvas(MyCanvasBase):
    def InitGL(self):
        # set viewing projection
        glMatrixMode(GL_PROJECTION)
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)

        # position viewer
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -2.0)

        # position object
        glRotatef(self.y, 1.0, 0.0, 0.0)
        glRotatef(self.x, 0.0, 1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_LIGHTING)
        # glEnable(GL_LIGHT0)

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        d=0.5
        glScalef(d/(self.bounding_box[3]-self.bounding_box[0]), d/(self.bounding_box[4]-self.bounding_box[1]), d/(self.bounding_box[5]-self.bounding_box[2]))

        for box in self.voxelBoxes:
             self.DrawCube(box)



        if self.size is None:
            self.size = self.GetClientSize()
        w, h = self.size
        w = max(w, 1.0)
        h = max(h, 1.0)
        xScale = 180.0 / w
        yScale = 180.0 / h
        glRotatef((self.y - self.lasty) * yScale, 1.0, 0.0, 0.0);
        glRotatef((self.x - self.lastx) * xScale, 0.0, 1.0, 0.0);

        self.SwapBuffers()

    def DrawCube(self, box):
        # glBegin(GL_LINE_LOOP)
        # glVertex3f(box[0], box[1], box[2])
        # glVertex3f(box[3], box[1], box[2])
        # glVertex3f(box[3], box[4], box[2])
        # glVertex3f(box[0], box[4], box[2])
        # glEnd()
        #
        # glBegin(GL_LINE_LOOP)
        # glVertex3f(box[3], box[4], box[5])
        # glVertex3f(box[3], box[1], box[5])
        # glVertex3f(box[0], box[1], box[5])
        # glVertex3f(box[0], box[4], box[5])
        # glEnd()
        #
        # glBegin(GL_LINES)
        # glVertex3f(box[0], box[1], box[2])
        # glVertex3f(box[0], box[1], box[5])
        #
        # glVertex3f(box[3], box[1], box[2])
        # glVertex3f(box[3], box[1], box[5])
        #
        # glVertex3f(box[3], box[4], box[2])
        # glVertex3f(box[3], box[4], box[5])
        #
        # glVertex3f(box[0], box[4], box[2])
        # glVertex3f(box[0], box[4], box[5])
        # glEnd()

        glBegin(GL_QUADS)
        glVertex3f(box[0], box[1], box[2])
        glVertex3f(box[3], box[1], box[2])
        glVertex3f(box[3], box[4], box[2])
        glVertex3f(box[0], box[4], box[2])

        glVertex3f(box[0], box[1], box[2])
        glVertex3f(box[0], box[1], box[5])
        glVertex3f(box[0], box[4], box[5])
        glVertex3f(box[0], box[4], box[2])

        glVertex3f(box[0], box[1], box[2])
        glVertex3f(box[0], box[1], box[5])
        glVertex3f(box[3], box[1], box[5])
        glVertex3f(box[3], box[1], box[2])

        glVertex3f(box[3], box[4], box[2])
        glVertex3f(box[3], box[4], box[5])
        glVertex3f(box[3], box[1], box[5])
        glVertex3f(box[3], box[1], box[2])

        glVertex3f(box[3], box[4], box[2])
        glVertex3f(box[3], box[4], box[5])
        glVertex3f(box[0], box[4], box[5])
        glVertex3f(box[0], box[4], box[2])

        glVertex3f(box[3], box[4], box[5])
        glVertex3f(box[3], box[1], box[5])
        glVertex3f(box[0], box[1], box[5])
        glVertex3f(box[0], box[4], box[5])

        glEnd()

#----------------------------------------------------------------------
class RunDemoApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        canvasClass = eval('CubeCanvas')


        frame = wx.Frame(None, -1, 'CubeCanvas', size=(800,800), pos=(200,200))
        canvasClass(frame) # CubeCanvas(frame) or ConeCanvas(frame); frame passed to         MyCanvasBase
        frame.Show(True)

        self.frame = frame
        return True

    def OnExitApp(self, evt):
        self.frame.Close(True)

    def OnCloseFrame(self, evt):
        if hasattr(self, "window") and hasattr(self.window, "ShutdownDemo"):
            self.window.ShutdownDemo()
        evt.Skip()

app = RunDemoApp()
app.MainLoop()
