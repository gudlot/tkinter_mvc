
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import cm

from matplotlib import pyplot as plt

import numpy as np



class View():
    # The view will be responsible for displaying widgets
    # and getting some information from user and from model.

    def __init__(self, model):
        """ Creates the main frame and links other frames to it. Only this layer should be visible to the model and controller. """

        self._model = model

        self._master = tk.Tk()
 
        self._frame = tk.Frame(self._master)
        self.fig = Figure(figsize=(7.5, 4), dpi=80)

        self.ax0 = self.fig.add_subplot()
        self._frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        
        # The canvas is the drawing arrea
        self.canvas = FigureCanvasTkAgg(self.fig, master=self._frame)
        # Navigation toolbar for the canvas
        toolbar = NavigationToolbar2Tk(self.canvas, self._frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.sidepanel = SidePanel(self._frame, self,  self._model)   #parent,  guicontrol, model as parame for SidePannel, this is how you establish communication :-)
        self.motorpanel= MotorPanel(self._frame, self, self._model)   #parent,  guicontrol, model as parame for Motorpanel 


        self.cbVariables={}
        self.cb={}
        #self.cbTexts={}
        #create checkboxes for diodes
        for diode_name in self._model.diode_names():
            self.cbVariables[diode_name]=tk.IntVar() #default value=0   #master=self.view.sidepanel.frame3
            #self.cbTexts[diode_name] = tk.StringVar()
            self.cb[diode_name]=ttk.Checkbutton(self.sidepanel.frame3,text=diode_name, variable=self.cbVariables[diode_name], state=['!alternate','!selected'], offvalue=0, onvalue=1, command=lambda diode_name=diode_name: self.on_cb_diode_selection(diode_name))
            self.cb[diode_name].pack(side=tk.TOP, anchor=tk.W) 
            print(f"Test on diode {diode_name} state at start: !alternate: {self.cb[diode_name].instate(['!alternate'])}, !selected: {self.cb[diode_name].instate(['!selected'])}") 


        self.cbVariables_cam={}
        self.cb_cam={}
        # create checkboxes for cameras
        for camera_name in self._model.camera_names():
            self.cbVariables_cam[camera_name]=tk.IntVar()
            self.cb_cam[camera_name]=ttk.Checkbutton(self.sidepanel.frame5,text=camera_name, variable=self.cbVariables_cam[camera_name], state=['!alternate','!selected'], offvalue=0, onvalue=1, command=lambda camera_name=camera_name: self.on_cb_cam_selection(camera_name))
            self.cb_cam[camera_name].pack(side=tk.TOP, anchor=tk.W) 
            print(f"Test on camera {camera_name} state at start: !alternate: {self.cb_cam[camera_name].instate(['!alternate'])}, !selected: {self.cb_cam[camera_name].instate(['!selected'])}") 


    # Methods 
           
    def on_create_scanplot(self, m):
        """ Connects the 1D scan plot button to a method """
        self.sidepanel.plotBut.bind("<Button>", m)

    def on_create_camplot(self, m):
        """ Connects the plot cam scan button to a method """
        self.sidepanel.plotCamBut.bind("<Button>", m)

    def on_clear(self, m):
        """ Clear canvas area """
        self.sidepanel.clearButton.bind("<Button>", m)

    def on_combobox_selection(self, m):  
        """ Connects combobox to a method """
        self.sidepanel.motor_selCombo.bind("<<ComboboxSelected>>", m)    

    def on_show_scan_settings(self,m):
        """ Connects the button show scan settings to a method """
        self.motorpanel.show_scan_settingsButton.bind("<Button>", m)

    def on_cb_diode_selection(self,diode_name): 
        """ Prints out the current state of a diode """
        print(f"Diode {diode_name} is {self.cb[diode_name].state()}")

    def on_cb_cam_selection(self,camera_name): 
        """ Prints out the current state of a camera """
        print(f"Camera {camera_name} is {self.cb_cam[camera_name].state()}")

        
    def run(self):
        """ Main method to start the GUI """
        self._master.geometry("1200x600")
        self._master.title("Tkinter MVC example")
        self._master.deiconify()
        self._master.mainloop()

    def on_motor_selection(self, mot_selected):
        """ Sends information about current motor to the label """
        # shows the selected motor and its position in the label
        #self.sidepanel.curr_motor_valLabel.configure(text=self._model.motors[mot_selected])
        self.sidepanel.curr_motor_val.set(self._model.motors[mot_selected])

        print(f"{mot_selected} was selected.")

        # adjust the units shown above the motor input values, when the motor is changed by the user 
        for column in self.motorpanel.motor_inputTexts:
            self.motorpanel.motor_inputTexts[column].set(f"{column} [{self._model.motors[mot_selected].units}]")
           
        # return motor as object 
        return self._model.motors[mot_selected]


    def motor_selection(self, event):
        """ Selects motors on event action """
        # this method is directly bound to the function, so we can make use of this option
        mot_selected = event.widget.get()
        #show the current motor value after selection in the GUI
        self.view.on_motor_selection(mot_selected)


    def update_current_motor_pos(self, step, mot_selected):
        """ Sends current motor information to the label """
        # The plan was to use this function to show a continuous update of the motor values. 
        # We do this with self._master.update()

        self.sidepanel.curr_motor_val.set(f"Step {step}: {mot_selected}")
        # this updates the GUI while the function runs
        self._master.update()

    def get_motor_selection(self):
        """ Get current motor selection from combobox and return motor """
        try:
            if self.sidepanel.motor_selCombo.get() == "":     #returna a string
                raise ValueError('No motor selected')
            else:
                print('Current selected motor ', self.sidepanel.motor_selCombo.get(), type(self.sidepanel.motor_selCombo.get()))


                #returns only the motor name, i.e. str
                #return self.sidepanel.motor_selCombo.get()   #string : MY-TINY-MOTOR 
                # returns a motor object
                print('get motor selection func will return ', type(self._model.motors[self.sidepanel.motor_selCombo.get()] ))
                return self._model.motors[self.sidepanel.motor_selCombo.get()]   #returns <class 'toydaq.devices.Motor'>
                                                                             
        except ValueError as e:
            self.no_motor_selected()
            showwarning(title='Empty motor selection', message="Select motor.")
            return
        
    def get_diode_selection(self):
        """ Returns which diodes is selected. Two choices: by state or by variable. I went with by variable."""
        #for label in self.cbVariables:
        #    print(label, self.cbVariables[label].get())

        for diode_name in self.cb:
            if self.cb[diode_name].instate(['selected']) == True:
                print(f"Diode {diode_name} is selected.")

        diodes_cb_values=[v.get() for v in self.cbVariables.values()]
        print(f"Diode counter selection: {diodes_cb_values}")
     

        if all([ w == 0 for w in diodes_cb_values]):
            self.no_diode_selected()
            return 
        else:
            all_selected_diodes={k:v for (k,v) in self.cbVariables.items() if v.get() == 1}
            
        # returns a dict of selected diodes
        return all_selected_diodes

    def get_camera_selection(self):
        """ Gets the current camera selection """
        cameras_cb_values=[v.get() for v in self.cbVariables_cam.values()]

        if all([ w == 0 for w in cameras_cb_values]):
            self.no_camera_selected()
            return 
        else:
            all_selected_cameras={k:v for (k,v) in self.cbVariables_cam.items() if v.get() == 1}
            print(all_selected_cameras, "type is", type(all_selected_cameras))

        # Our model beamline has only one camera curently. 
        if np.sum(cameras_cb_values) !=1:
            showwarning(title="Select one camera", message="Select one camera.")

        # returns a dict of selected cameras
        return all_selected_cameras
 

    def show_scan_settings(self): 
        """ Current motor, start, stop, stepsize is shown """
    
        try:
            curr_mot_selected=self.get_motor_selection()  #curre_mot_selected of <class 'toydaq.devices.Motor'>
            if curr_mot_selected is None:
                raise ValueError("No motor selected")
        except ValueError as e:
            return

        print(f"{curr_mot_selected.name} is selected.")   # <class 'toydaq.devices.Motor'>.name
        # access the ttk.Entry 
        out_strings=[]
        for column in self.motorpanel.motor_inputTexts:
            print(print('Identify', self.motorpanel.entries[column]))
            # Label : Value
            out_str=f"{self.motorpanel.motor_inputTexts[column].get()}: {self.motorpanel.entriesValues[column].get()}"
            print(out_str)
            out_strings.append(out_str)

            # Both options possible, get only one, I go for the Variables of the ttk.Entry
            #print(f"This is the current Variable for {self.motorpanel.entries[column]}: {self.motorpanel.entriesValues[column].get()}")
            #print("This is the current value via.get on the ttk.Entry", self.motorpanel.entries[column].get())
        showinfo("Current scan settings", f"Motor: {curr_mot_selected.name}, {str(out_strings)[1:-1]}")
        
    def retrieve_scan_settings(self):
        """ Collect scan settings """

        mot_selected=self.get_motor_selection()
        mot_scan_settings=self.motorpanel.entriesValues

        return (mot_selected, mot_scan_settings)


    def line_colors(self, number_of_lines):
        """ Create better line colors """
        start = 0.0
        stop = 1.0
        cm_subsection = np.linspace(start, stop, number_of_lines)
        colors = [cm.jet(x) for x in cm_subsection]
        return colors
        
    def modify_1d_plot(self, mot, diodes):
        """ Modify title and xlabel for 1D scan with diodes """
        self.ax0.set_title('1D Scan')
        self.ax0.set_xlabel(f"{mot.name} [{mot.units}]")
    
    def plot_1d_scan(self, mot_selected, dio_selected, mot_values, dio_values):
        """ Plot 1D scan, one motor, multiple diodes """

        # some graphic modificaton
        self.modify_1d_plot(mot_selected, dio_selected)
        marker = ['o', 'v', '^', '<', '>', 's', '8', 'p']
        colors = ['b', 'g', 'r', 'c', 'm', 'k']
        handles=[]
        labels=[]
        for i in range(len(dio_selected)):
            line, =self.ax0.plot(mot_values, dio_values[i],  marker=marker[i], color=colors[i])
            #keep infos on legend.
            handles.append(line)
            labels.append(dio_selected[i])
        self.ax0.legend(handles,labels, loc="best")
        #this updates the plot (see Matplotlib doc)
        self.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def plot_cam_1d_scan(self, mot_selected, cam_image, camera):
        """ Plot 1D scan with a camera, one motor, one camera """
        cam_im=self.ax0.imshow(cam_image, interpolation="none")
        self.ax0.set_title(f'1D Scan {camera}')
        self.ax0.set_xlabel(f"{camera} X")
        self.ax0.set_ylabel(f"{camera} Y")
        self.canvas.draw_idle()
        self.fig.canvas.flush_events()


    def no_motor_selected(self):
        """ Warning no motor selected """
        showwarning(title='1D scan warning', message="No motor selected for 1D scan.")
        
    
    def no_diode_selected(self):
        """ Warning no diode selected """
        showwarning(title='1D scan warning', message="No diode selected for 1D scan.")
        
    def no_camera_selected(self):
        """ Warning no camera selected """
        showwarning(title='1D scan warning', message="No camera selected for 1D scan.")

class SidePanel():
    """ This class contains the buttons, the combobox, the ouput label for the motor, label frames for diodes """
    def __init__(self, root, guicontrol, model):
        self.guicontrol=guicontrol
        self._model=model
        self._frame2 = tk.Frame(root)
        self._frame2.pack(side="top", fill=tk.BOTH, expand=1)
        self.plotBut = tk.Button(self._frame2, text="Plot 1D Scan")
        self.plotBut.pack(side="top", fill=tk.BOTH)
        self.plotCamBut = tk.Button(self._frame2, text="Plot Cam Scan")
        self.plotCamBut.pack(side="top", fill=tk.BOTH)
        self.clearButton = tk.Button(self._frame2, text="Clear")
        self.clearButton.pack(side="top", fill=tk.BOTH)


        # Create a frame
        self.motor_sel_title=ttk.Label(self._frame2, text='Motor selection').pack()
        motor_name=tk.StringVar() #Motornames are strings
        self.motor_selCombo=ttk.Combobox(self._frame2, textvariable=motor_name)
        self.motor_selCombo['values']=self._model.motor_names()
        self.motor_selCombo['state'] = 'readonly'
        #motor_sel.grid(column=0, row=1)
        self.motor_selCombo.pack(side="top", fill=tk.BOTH)
    

        #Create display for current motor values
        self.curr_motor_val=tk.StringVar()
        self.curr_motor_valLabel=ttk.Label(self._frame2, textvariable=self.curr_motor_val)
        self.curr_motor_valLabel.pack(side="top", fill=tk.BOTH)

         # Create LabelFrame for diodes
        self.frame3=tk.LabelFrame(self._frame2, height=150, text="Diodes")
        self.frame3.pack(side=tk.TOP, fill=tk.X, expand=0, anchor=tk.NW)
        self.frame3.config(highlightcolor='blue', highlightthickness=5, highlightbackground='blue', labelanchor="nw")

        #Create LabelFrame for camera
        self.frame5=tk.LabelFrame(self._frame2, height=150, text="Cameras")
        self.frame5.pack(side=tk.TOP, fill=tk.X, expand=0, anchor=tk.NW)
        self.frame5.config(highlightcolor='blue', highlightthickness=5, highlightbackground='blue', labelanchor="nw")

 
class MotorPanel():
    """ This class contains the show scan bettons and the entries for the motor positon.  #TODO: Boxes for soft limits for motos"""
      
    def __init__(self, root, guicontrol, model):
        self.guicontrol=guicontrol
        self._model=model
        self.frame4=tk.Frame(root)
        self.frame4.pack(side='top',fill=tk.BOTH, expand=1) 
        
        self.entries = {}
        self.entriesValues = {}
        self.motor_input_label=["Start", "Stop", "Stepsize"]  #hard coded, but extendable for software limits
        self.motor_input_titleLabel={}
        self.motor_inputTexts ={}

        # Function to validate entries to the ttk.Entry 
        vcmd = (self.frame4.register(self.onValidate), '%P', '%s', '%S','%W')

        for i, column in enumerate(self.motor_input_label):
            self.motor_inputTexts[column] =tk.StringVar(value=column)
            #self.motor_inputTexts[column].set(f"{column}") #default labels without units
            self.motor_input_titleLabel[column] = ttk.Label(self.frame4, font=('Calibri', 13), textvariable=self.motor_inputTexts[column])
            self.motor_input_titleLabel[column].grid(row=0, column=i, sticky="nswe")
           

            self.entriesValues[column]= tk.DoubleVar()
            self.entries[column] = ttk.Entry(self.frame4, font=('Calibri', 13), textvariable=self.entriesValues[column], justify='left', validate="key", validatecommand=vcmd)
            self.entries[column].grid(row=1, column=i, sticky="nswe")

            
        #lets create a push button
        self.show_scan_settingsButton=ttk.Button(self.frame4,text="Show scan settings")
        self.show_scan_settingsButton.grid(row=2,columnspan=len(self.motor_input_label))

        #lets create a destroy button
        self.terminateButton=ttk.Button(self.frame4, text="Exit GUI", command=lambda: self.guicontrol._master.destroy() )
        self.terminateButton.grid(row=3, columnspan=len(self.motor_input_label))


    def onValidate(self, P, s, S, W):
        """This should validate the input for each ttk.Entry
        %P = value of the entry if the edit is allowed
        %s = value of entry prior to editing
        %S = the text string being inserted or deleted, if any
        %W = the tk name of the widget
        """
        if P.strip() == "":
            # allow blank string
            return True
        elif P.strip() == "-":
            return True
        elif P.strip() == "+":
            return True
        try:
            float(P)
            return True
        except ValueError:
            print(f'float({P}) raised ValueError in {W}.')
            showwarning(title=f'ValueError in {W}', message=f"{P} is not a valid input.")
            return False

        # TODO
        # Create entry limits for software limits
      
        
    