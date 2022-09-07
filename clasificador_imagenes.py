#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Clasificador de imágenes
#
# Author:  Oscar Diaz <odiaz@ieee.org>
# Author: Andrés Puerto <andrespuertolara@gmail.com>
# Version: 0.2
# Date:    10-10-2019
#
#
# This code is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this package; if not, see 
# <http://www.gnu.org/licenses/>.
#

import os
import glob
import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd
import PIL.Image
import PIL.ImageTk

#from PIL import ImageTk,Image

class mainapp(object):
    def __init__(self, master):
        # base data
        self.sdirstr = None
        self.ddirstr = None
        self.watermarkfile = None
        
        # build app GUI
        self.master = master
        self.master.title("Clasificador")
        self.master.resizable(width=True, height=False)
        self.frame = tk.Frame(master)
        self.frame.pack()
        
        # title
        self.title = tk.Label(self.frame, text="Clasificador de imágenes")
        self.title.pack(fill=tk.X)
        
        # source dir
        self.sdirframe = tk.Frame(master)
        self.sdirframe.pack()
        self.sdirlabel = tk.Label(self.sdirframe, text="Origen de imágenes: \n(SIN DEFINIR)")
        self.sdirlabel.pack(fill = tk.X, expand = True, side=tk.LEFT)
        self.sdirbtn = tk.Button(self.sdirframe, text="Seleccionar directorio", command=self.set_sdir)
        self.sdirbtn.pack(side=tk.LEFT)
        
        # destination dir
        self.ddirframe = tk.Frame(master)
        self.ddirframe.pack()
        self.ddirlabel = tk.Label(self.ddirframe, text="Destino de imágenes: \n(SIN DEFINIR)")
        self.ddirlabel.pack(fill = tk.X, expand = True, side=tk.LEFT)
        self.ddirbtn = tk.Button(self.ddirframe, text="Seleccionar directorio", command=self.set_ddir)
        self.ddirbtn.pack(side=tk.LEFT)
        
        # watermark file
        self.wmarkframe = tk.Frame(master)
        self.wmarkframe.pack()
        self.wmarklabel = tk.Label(self.wmarkframe, text="Archivo de marca de agua: \n(SIN DEFINIR)")
        self.wmarklabel.pack(fill = tk.X, expand = True, side=tk.LEFT)
        self.wmarkbtn = tk.Button(self.wmarkframe, text="Seleccionar archivo", command=self.set_wmark)
        self.wmarkbtn.pack(side=tk.LEFT)
        
        # actions
        self.actframe = tk.Frame(master)
        self.actframe.pack()
        
        # run clasification
        self.actbtn = tk.Button(self.actframe, text="Clasificar", command=self.actrun)
        self.actbtn.pack(side=tk.LEFT)
        
        # exit button
        self.exitbtn = tk.Button(self.actframe, text="Salir", command=self.frame.quit)
        self.exitbtn.pack(side=tk.LEFT)
        
        
        
        
    def set_sdir(self):
        directory = tkfd.askdirectory(title = "Seleccionar directorio de origen de imágenes")
        if not isinstance(directory, str):
            return
        if directory == "":
            return
        if not os.access(directory, os.R_OK):
            tkmsg.showerror("Origen de imágenes", "No se puede leer desde el directorio seleccionado.")
            return
        if self.ddirstr == directory:
            tkmsg.showerror("Origen de imágenes", "Por favor seleccione un directorio diferente del destino de imágenes.")
            return
        self.sdirstr = directory
        self.sdirlabel.config(text = "Origen de imágenes: \n%s" % self.sdirstr)
        
    def set_ddir(self):
        directory = tkfd.askdirectory(title = "Seleccionar directorio de destino de imágenes")
        if not isinstance(directory, str):
            return
        if directory == "":
            return
        if not os.access(directory, os.W_OK):
            tkmsg.showerror("Destino de imágenes", "No se puede escribir en el directorio seleccionado.")
            return
        if self.sdirstr == directory:
            tkmsg.showerror("Destino de imágenes", "Por favor seleccione un directorio diferente del origen de imágenes.")
            return
        self.ddirstr = directory
        self.ddirlabel.config(text = "Destino de imágenes: \n%s" % self.ddirstr)
        
    def set_wmark(self):
        wfile = tkfd.askopenfilename(title = "Seleccionar archivo de marca de agua", filetypes = (("Archivo JPG","*.jpg"), ("Archivo PNG","*.png"), ("Todos los archivos","*.*")))
        if not isinstance(wfile, str):
            return
        if wfile == "":
            return
        if not os.access(wfile, os.F_OK):
            tkmsg.showerror("Marca de agua", "No se puede leer el archivo seleccionado.")
            return
        try:
            PIL.Image.open(wfile)
        except:
            tkmsg.showerror("Marca de agua", "El archivo seleccionado no es una imagen. Seleccione otro archivo.")
            return
        self.watermarkfile = wfile
        self.wmarklabel.config(text = "Archivo de marca de agua: \n%s" % self.watermarkfile)
        
    def actrun(self):
        if self.sdirstr is None:
            tkmsg.showerror("Origen de imágenes", "No se ha seleccionado algún directorio de origen.")
            return
        if self.ddirstr is None:
            tkmsg.showerror("Destino de imágenes", "No se ha seleccionado algún directorio de destino.")
            return
        if self.watermarkfile is None:
            tkmsg.showerror("Marca de agua", "No se ha seleccionado algún archivo de marca de agua.")
            return
        if not os.access(self.sdirstr, os.R_OK):
            tkmsg.showerror("Origen de imágenes", "No se puede leer desde el directorio seleccionado.")
            return
        if not os.access(self.ddirstr, os.W_OK):
            tkmsg.showerror("Destino de imágenes", "No se puede escribir en el directorio seleccionado.")
            return
        try:
            PIL.Image.open(self.watermarkfile)
        except:
            tkmsg.showerror("Marca de agua", "No se puede leer el archivo de marca de agua.")
            return
            
        # prepare image file list

        srclist = []
        for p in glob.glob(os.path.join(self.sdirstr, "*")):
            try:
                PIL.Image.open(p)
            except:
                continue
            srclist.append(p)
        
        if len(srclist) == 0:
            tkmsg.showerror("Clasificador de imágenes", "No hay imágenes en el directorio de origen.")
            return
            
        newwin = tk.Toplevel(self.master)
        newwin.title("Clasificador en: %s" % self.sdirstr)
        newwin.transient(self.master)
        newwin.grab_set()
        clasifyapp(self.master, newwin, srclist, self.ddirstr, self.watermarkfile)
        self.master.wait_window(newwin)
        
class clasifyapp(object):
    def __init__(self, root, master, imglist, ddirstr, wmfile):
        # Fixed parameters
        self.alphaorig = 1
        self.alphawatermark = 1
        self.heightwatermark =400
        
        # base data
        self.imglist = imglist
        self.ddirstr = ddirstr
        self.wmimg = PIL.Image.open(wmfile)
        self.curimgidx = 0
        self.cldict = {}
        self.curbaseimg = None
        self.curimg = None
        self.curimgdata = {
            "ww": 100, 
            "wh": 100,
            "wbbx1": None, 
            "wbby1": None, 
            "wbbx2": None, 
            "wbby2": None,
            "imgw": None, 
            "imgh": None, 
            "bbx1": None, 
            "bby1": None, 
            "bbx2": None, 
            "bby2": None
        }
        self.zoomstate = {
            "State": False, 
            "CanvasImg": None, 
            "Rectobj": None, 
            "Init": None, 
            "End": None, 
        }
    
        # build app GUI
        self.root = root
        self.master = master
        self.master.resizable(width=True, height=True)
        self.frame = tk.Frame(master)
        self.frame.pack(fill = tk.BOTH, expand = True)
        
        # title
        self.title = tk.Label(self.frame, text=self.getcurimgtitle())
        self.title.pack(fill=tk.X)
        
        # image
        #self.imagelabel = tk.Label(self.frame, image=self.getcurimgdata())
        self.imagelabel = tk.Canvas(self.frame, width=320, height=320)
        self.imagelabel.pack(fill = tk.BOTH, expand = True)
        
        self.curimgdata["ww"] = 320
        self.curimgdata["wh"] = 320
        self.loadnewimage()
        self.drawimage()
        
        # image clasification data
        self.imageclas = tk.Label(self.frame, text=self.getcurimgclas())
        self.imageclas.pack(fill=tk.X)
        
        # clasification text
        self.clasframe = tk.Frame(master)
        self.clasframe.pack()
        self.clastext = tk.Entry(self.clasframe)
        self.clastext.pack(side=tk.LEFT)
        self.clasbtn = tk.Button(self.clasframe, text="Añadir clasificación", command=self.appendclas)
        self.clasbtn.pack(side=tk.LEFT)
        
        # actions
        self.actframe = tk.Frame(master)
        self.actframe.pack()
        
        # prev image
        self.prevbtn = tk.Button(self.actframe, text="Anterior imagen", command=self.previmage)
        self.prevbtn.pack(side=tk.LEFT)
        
        # next image
        self.nextbtn = tk.Button(self.actframe, text="Siguiente imagen", command=self.nextimage)
        self.nextbtn.pack(side=tk.LEFT)
        
        # exit button
        self.exitbtn = tk.Button(self.actframe, text="Salir", command=self.exit)
        self.exitbtn.pack(side=tk.LEFT)
        
        # mouse events
        self.imagelabel.bind("<Button-1>", self.dozoom_click)
        self.imagelabel.bind("<ButtonRelease-1>", self.dozoom_release)
        self.imagelabel.bind("<B1-Motion>", self.dozoom_motion)
        self.imagelabel.bind("<Button-3>", self.restorezoom)
        self.imagelabel.bind("<Configure>", self.resizewindow)
        
        # wslider
        
        self.wslider=tk.Scale(self.actframe,from_=0,to=1,resolution=0.01,tickinterval=0.1,label='AnchoC')
        self.wslider.pack(side=tk.LEFT)
        self.wslider.set(1)
        #self.labelw=tk.Label(self.actframe,text='Calw').place(x=320,y=1)
        #hslider
              
        self.hslider=tk.Scale(self.actframe,from_=0,to=1,resolution=0.01,tickinterval=0.1,label='AltoC')
        self.hslider.pack(side=tk.RIGHT)
        self.hslider.set(1)
        #self.labelh=tk.Label(self.actframe,text='Calh').place(x=420,y=1)
    
    def getcurimgtitle(self):
        return "Imagen: %d de %d\n%s" % (self.curimgidx+1, len(self.imglist), self.imglist[self.curimgidx])
        
    def loadnewimage(self):
        # load image
        try:
            img = PIL.Image.open(self.imglist[self.curimgidx])
        except:
            img = PIL.Image.new("L", (16, 16), 255)
            
        # extract basic info
        w, h = img.size
        self.curimgdata["imgw"] = w
        self.curimgdata["imgh"] = h
        self.curimgdata["bbx1"] = 0
        self.curimgdata["bby1"] = 0
        self.curimgdata["bbx2"] = w
        self.curimgdata["bby2"] = h
        
        # save a reference
        self.curbaseimg = img
        
    def drawimage(self):
        if self.zoomstate["CanvasImg"] is not None:
            self.imagelabel.delete(self.zoomstate["CanvasImg"])
            
        # widget size
        ww = self.curimgdata["ww"]
        wh = self.curimgdata["wh"]
            
        # find midpoint in canvas
        midx = ww // 2
        midy = wh // 2
        
        # calculate bbox width and height
        bbw = self.curimgdata["bbx2"] - self.curimgdata["bbx1"]
        bbh = self.curimgdata["bby2"] - self.curimgdata["bby1"]
        
        # scaling factors
        wfactor = ww/bbw
        hfactor = wh/bbh
        
        if wfactor <= hfactor:
            factor = wfactor
        else:
            factor = hfactor

        wfactor = int(bbw*factor)
        hfactor = int(bbh*factor)

        imgbox = (self.curimgdata["bbx1"], 
            self.curimgdata["bby1"], 
            self.curimgdata["bbx2"], 
            self.curimgdata["bby2"])
            
        # rescale bbox to current widget size
        imgbb = self.curbaseimg.resize(size = (800, 600), box = imgbox)
        
        # convert value for canvas use
        pi = PIL.ImageTk.PhotoImage(imgbb)
        self.curimg = pi
        
        self.zoomstate["CanvasImg"] = self.imagelabel.create_image((midx, midy), image=pi)
        
        # bbox inside canvas
        self.curimgdata["wbbx1"] = midx - (wfactor // 2)
        self.curimgdata["wbby1"] = midy - (hfactor // 2)
        self.curimgdata["wbbx2"] = self.curimgdata["wbbx1"] + wfactor
        self.curimgdata["wbby2"] = self.curimgdata["wbby1"] + hfactor
        
    def getcurimgclas(self):
        if self.curimgidx not in self.cldict:
            self.cldict[self.curimgidx] = []
            
        if len(self.cldict[self.curimgidx]) == 0:
            return "(Sin clasificación)"
        else:
            clstr = ",".join(self.cldict[self.curimgidx])
            return "Etiquetas: %s" % clstr
            
    def appendclas(self):
        if self.curimgidx not in self.cldict:
            self.cldict[self.curimgidx] = []
            
        newclas = self.clastext.get()
        self.clastext.delete(0, tk.END)
        
        if newclas == "":
            return
        
        if newclas in self.cldict[self.curimgidx]:
            # already classified. Ignoring
            return

        self.cldict[self.curimgidx].append(newclas)
        
        basedir = os.path.join(self.ddirstr, newclas)
        if not os.path.isdir(basedir):
            os.mkdir(basedir)
            
        basefile = os.path.basename(self.imglist[self.curimgidx])
        
        # Watermark
        # shutil.copyfile(self.imglist[self.curimgidx], os.path.join(basedir, basefile))
        imgbase = PIL.Image.new('RGBA', self.curbaseimg.size, (0,0,0,0))
        
        baseimg = PIL.Image.blend(imgbase, self.curbaseimg.convert("RGBA"), self.alphaorig)

        wmscaled = self.wmimg.resize((int(self.wslider.get()*self.curbaseimg.size[0]), int(self.hslider.get()*self.heightwatermark)))
        

        wmssize = imgbase.copy()
        wmssize.paste(wmscaled, (0, (self.curimgdata["imgh"] - wmscaled.size[1])))
        
        wmsimg = PIL.Image.blend(imgbase, wmssize, self.alphawatermark)
        
        imgbase.paste(baseimg, (0, 0))
        imgbase.paste(wmsimg, (0, 0), mask=wmsimg)
        imgbase = imgbase.convert("RGB")
        imgbase.save(os.path.join(basedir, basefile))
        #
        
        self.updateclasinfo()
        
    def updateclasinfo(self):
        self.imageclas.config(text=self.getcurimgclas())
        
    def updateimage(self):
        self.title.config(text=self.getcurimgtitle())
        self.drawimage()
        self.imageclas.config(text=self.getcurimgclas())
        
    def nextimage(self):
        self.curimgidx += 1
        if self.curimgidx >= len(self.imglist):
            self.curimgidx = 0
            
        self.loadnewimage()
        self.updateimage()
        
    def previmage(self):
        self.curimgidx -= 1
        if self.curimgidx < 0:
            self.curimgidx = len(self.imglist)-1
            
        self.loadnewimage()
        self.updateimage()
        
    def resizewindow(self, evdata):
        # set new data
        self.curimgdata["ww"] = evdata.width
        self.curimgdata["wh"] = evdata.height
        
        self.drawimage()
        
    def checkcoordimage(self, point):
        try:
            x = point[0]
            y = point[1]
        except:
            return False
        
        for i in ("wbbx1", "wbbx2", "wbby1", "wbby2"):
            if self.curimgdata[i] is None:
                return False
                
        if x < self.curimgdata["wbbx1"] or x > self.curimgdata["wbbx2"]:
            return False
        if y < self.curimgdata["wbby1"] or y > self.curimgdata["wbby2"]:
            return False
            
        return True
        
    def dozoom_click(self, evdata):
        # state machine
        if self.zoomstate["State"] == False:    # no zoom active
            inittmp = (evdata.x, evdata.y)
            if self.checkcoordimage(inittmp):
                # start zoom
                self.zoomstate["Init"] = inittmp
                self.imagelabel.config(cursor = "crosshair")
                self.zoomstate["State"] = True
                
                if self.zoomstate["Rectobj"] is not None:
                    self.imagelabel.delete(self.zoomstate["Rectobj"])
                    
                self.zoomstate["Rectobj"] = self.imagelabel.create_rectangle((evdata.x, evdata.y, evdata.x, evdata.y))
            
    def dozoom_release(self, evdata):
        # delete rectangle and recover cursor
        self.imagelabel.delete(self.zoomstate["Rectobj"])
        self.zoomstate["Rectobj"] = None
        self.imagelabel.config(cursor = "")
        
        # state machine
        if self.zoomstate["State"] == True:
            # check endpoint
            endtmp = (evdata.x, evdata.y)
            if self.checkcoordimage(endtmp):
                self.zoomstate["End"] = endtmp
                
                # canvas box
                cbbx1 = min(self.zoomstate["Init"][0], self.zoomstate["End"][0])
                cbbx2 = max(self.zoomstate["Init"][0], self.zoomstate["End"][0])
                cbby1 = min(self.zoomstate["Init"][1], self.zoomstate["End"][1])
                cbby2 = max(self.zoomstate["Init"][1], self.zoomstate["End"][1])
                                
                # build new bbox
                wc = self.curimgdata["wbbx2"] - self.curimgdata["wbbx1"]
                hc = self.curimgdata["wbby2"] - self.curimgdata["wbby1"]
                wbb = self.curimgdata["bbx2"] - self.curimgdata["bbx1"]
                hbb = self.curimgdata["bby2"] - self.curimgdata["bby1"]

                # calculate scaling
                wfactor = wbb/wc
                hfactor = hbb/hc

                # proposed new bbox
                bbx1 = int((cbbx1 - self.curimgdata["wbbx1"]) *wfactor) + self.curimgdata["bbx1"]
                bbx2 = int((cbbx2 - self.curimgdata["wbbx1"]) *wfactor) + self.curimgdata["bbx1"]
                bby1 = int((cbby1 - self.curimgdata["wbby1"]) *hfactor) + self.curimgdata["bby1"]
                bby2 = int((cbby2 - self.curimgdata["wbby1"]) *hfactor) + self.curimgdata["bby1"]
                
                # check if bbox is at least 5x5
                if ((bbx2 - bbx1) > 5) and ((bby2 - bby1) > 5):
                
                    # load bbox
                    self.curimgdata["bbx1"] = bbx1
                    self.curimgdata["bbx2"] = bbx2
                    self.curimgdata["bby1"] = bby1
                    self.curimgdata["bby2"] = bby2
                
                    # and finally redraw
                    self.drawimage()
                
        self.zoomstate["State"] = False

    def dozoom_motion(self, evdata):
        # state machine
        if self.zoomstate["State"] == True:
            endtmp = (evdata.x, evdata.y)
            if self.checkcoordimage(endtmp):
                rectcolor = "black"
            else:
                rectcolor = "red"

            self.imagelabel.coords(self.zoomstate["Rectobj"], self.zoomstate["Init"][0], self.zoomstate["Init"][1], endtmp[0], endtmp[1])
            self.imagelabel.itemconfigure(self.zoomstate["Rectobj"], outline=rectcolor)
        
    def restorezoom(self, evdata):
        # default bbox
        self.curimgdata["bbx1"] = 0
        self.curimgdata["bby1"] = 0
        self.curimgdata["bbx2"] = self.curimgdata["imgw"]
        self.curimgdata["bby2"] = self.curimgdata["imgh"]
        
        self.drawimage()
        
    def exit(self):
        self.root.focus_set()
        self.master.destroy()
        
def launchapp():
    root = tk.Tk()
    mainapp(root)
    root.mainloop()
    
if __name__ == "__main__":
    launchapp()
