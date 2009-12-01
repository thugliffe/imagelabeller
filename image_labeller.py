from Tkinter import *
import Image, ImageTk
import os

from directorychooser import *
import glob
#path = 'd:\\images\\'
class DataSource(object):
    def __init__(self):
        files=open("settings.txt",'r')
        path=files.readline()
        self.pic_files = glob.glob(path+("*.jpg*" or "*.bmp" or "*.gif"))
    def __len__(self):
        return len(self.pic_files)
    def __iter__(self):
        return iter(self.pic_files)

class ImageViewer(Frame):
	def __init__(self,source,master):
		Frame.__init__(self, master)
		self.master.title("Image Labeller")
		self.pics = []
		self.current = 0
		self.names=[]
		self.porn_path='d:\\porn\\'
		self.not_porn_path='d:\\notporn\\'
        	self.images=iter(source)
                Button(root, text='Change Destination Porn Folder',command=self.set_porn_path).place(x=600,y=200)
                Button(root, text='Set Destination not Porn Folder',command=self.set_nporn_path).place(x=600,y=300)
	       	self._create_widgets()
		#print self.images.next()
		temp_image=self.images.next()
		self.pics.append(ImageTk.PhotoImage(Image.open(temp_image)))
		self.names.append(temp_image)
		
		
		#print Image.open('d:\\images\\1.jpg')
		self._load_image(self.pics[0],self.names[0])
		self.pack(fill=BOTH, expand=1)
	def set_porn_path(self):
            self.porn_path=askdirectory()+'\\'

        def set_nporn_path(self):
            self.not_porn_path=askdirectory()+'\\'
            
      
	 
	def _create_widgets(self):
		self.canvas = Canvas(self, bg='gray', highlightthickness=0)
		
		
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		xscroll = Scrollbar(self, orient=HORIZONTAL)
		yscroll = Scrollbar(self, orient=VERTICAL)
		xscroll.configure(command=self.canvas.xview)
		yscroll.configure(command=self.canvas.yview)
		self.canvas.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
		xscroll.grid(row=1, column=0, sticky='e'+'w')
		yscroll.grid(row=0, column=1, sticky='n'+'s')
		self.canvas['scrollregion'] = (0, 0, 1, 1)
		self.canvas.grid(row=0, column=0, sticky='n'+'s'+'e'+'w')
		f = Frame(self) ;f.grid(row=2, column=0, columnspan=2)
	
		Button(f, text='NOT PORN', command=self.next_image_nporn).pack(side='left', padx=5, pady=5)
		Button(f, text='PORN', command=self.next_image_porn).pack(side='left', padx=5, pady=5)

	def _load_image(self, image,name):
		self.canvas.delete(ALL)
		w, h = image.width(), image.height()
		self.canvas.create_image(1,1, anchor=NW, image=image)
		font=('courier', 12)
		self.canvas.create_text(800,100,text=name.split('\\')[-1],font=font)

		self.canvas['scrollregion'] = (0, 0, w, h)
		
		
	def next_image_nporn(self):

		im=Image.open(self.names[0])
		im.save(self.not_porn_path+self.names[0].split('\\')[-1])
		del self.names[0]
		del self.pics[0]
		temp_image=self.images.next()
		self.names.append(temp_image)
		self.pics.append(ImageTk.PhotoImage(Image.open(temp_image)))#print 'loading image %d' %self.current
		self._load_image(self.pics[0],self.names[0])

		
		
	def next_image_porn(self):

		im=Image.open(self.names[0])
		im.save(self.porn_path+self.names[0].split('\\')[-1])
		del self.pics[0]
		del self.names[0]
		temp_image=self.images.next()
		self.names.append(temp_image)
		self.pics.append(ImageTk.PhotoImage(Image.open(temp_image)))#print 'loading image %d' %self.current
		self._load_image(self.pics[0],self.names[0])


if __name__=="__main__":

    source = DataSource()
    root = Tk()
    pv = ImageViewer(source,root)

    top = pv.winfo_toplevel()
    top.state('zoomed')
    pv.mainloop()
