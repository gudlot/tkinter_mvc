from toydaq import scan_iter


#from threading import Thread
from tqdm import tqdm
import numpy as np

from model import Model
from view import View


# I use tkinter for creating the GUI and follow the MVC design patter to follow a serparate of concerns.
# Model: all hardware components inside and a future place for scan methods
# View: the GUI, visualises output, hardware. Talks to the user and the controller. Performs basic tasks like plotting and checks if parameter are selected
# Controller: Performs the workflows to bring motors and diodes, camera together. Sends events to functions


class Controller():
    """" Controller part of the MVC model """
   
    def __init__(self, model, view):
        
        self.model = model
        self.view=view
          
        # Establish connection between buttons in View and controller
        self.view.on_create_scanplot(self.create_scan_plot)
        self.view.on_create_camplot(self.create_cam_plot)
        self.view.on_clear(self.clear)

        self.view.on_combobox_selection(self.motor_selection)

        self.view.on_show_scan_settings(self.show_scan_settings)

            
 
    def clear(self, event):
        """" Clears canvas on event action"""
        self.view.ax0.clear()
        self.view.canvas.draw()


    def create_cam_plot(self, event):
        """ 1D scan with a camera on event action """

        # get scan configuration
        scan_dict=self.prepare_1d_scan_settings()

        # get camera selected, dict
        cam_sel_dict=self.view.get_camera_selection()
        # get the keys
        cam_selected=[k for k,v in  cam_sel_dict.items()]
        num_dio_sel=len(cam_selected)
        print(f"Selected cameras for scan are {cam_selected}.")
        print(scan_dict, cam_sel_dict)

        #clear graph
        self.view.ax0.clear()
        self.view.canvas.draw()

        x_values=[]
        for pos in scan_iter(scan_dict["mot_sel"], scan_dict["Start"], scan_dict["Stop"], scan_dict["Stepsize"], cb=None, show_progress=True):
            
            #save motor positions
            x_values.append(pos)
            for i in cam_selected:
                img = self.model.cameras[i].get()
            self.view.plot_cam_1d_scan(mot_selected=scan_dict["mot_sel"], cam_image=img, camera=cam_selected)


    
    def prepare_1d_scan_settings(self):
        """ Retrieves relevant information for scan and prepapres scan dict for output (1D scan)"""

        mot_selected, scan_values=self.view.retrieve_scan_settings()

        #["Start", "Stop", "Stepsize"]
        start= scan_values["Start"].get()
        stop= scan_values["Stop"].get()
        stepsize= scan_values["Stepsize"].get()
       
        #check
        try:
            if stepsize > np.absolute(stop - start):
                raise ValueError("Stepszie larger than total scan range.")
            
        except ValueError as e:
            showwarning(title='Stepsize too large.', message="Stepszie larger than total scan range.")
            return

        try:
            if start > stop:
                raise ValueError("Start>Stop")
        except ValueError as e:
            showwarning(title="Start>Stop", message="Please select start < stop.")

        try:
            if stepsize < 0:
                raise ValueError("Stepsize negative.")

        except ValueError as e:
            showwarning(title="Stepsize negative." , message="Choose positive Stepsize.") 
        
        try:
            if stepsize==0:
                raise ValueError(f"Stepsize is {stepsize}")
        except ValueError as e:
            showwarning(title=f"Stepsize {stepsize}." , message="Choose different Stepsize.") 
        
        
        scan_dict={}
        scan_dict["mot_sel"]=mot_selected
        scan_dict["Start"]=start
        scan_dict["Stop"]=stop
        scan_dict["Stepsize"]=stepsize
        return scan_dict

    def create_scan_plot(self, event):
        """ Procedure for the 1D scan plot with diodes """       
        #get the diodes
        dio_selected_dict=self.view.get_diode_selection()

        # get the keys
        dio_selected=[k for k,v in  dio_selected_dict.items()]
        num_dio_sel=len(dio_selected)
        print(f"Selected diodes for scan are {dio_selected}.")
       
        # get scan configuration
        scan_dict=self.prepare_1d_scan_settings()

        #clear graph
        self.view.ax0.clear()
        self.view.canvas.draw()


        # prepare for plot
        #self.view.modify_1d_plot(self.model.motors[mot_selected], dio_selected)
        #self.view.modify_1d_plot(mot_selected, dio_selected)
                  
        x_values=[]
        diode_values = [[] for i in range(0, num_dio_sel)]

        # Pseudo exectuition of motor
        #for pos in scan_iter(self.model.motors[mot_selected], start, stop, stepsize, cb=None, show_progress=False):
        for pos in scan_iter(scan_dict["mot_sel"], scan_dict["Start"], scan_dict["Stop"], scan_dict["Stepsize"], cb=None, show_progress=True):
            
            #save motor positions
            x_values.append(pos)
            # read out and save diode positions
            for i in range(num_dio_sel):
                diode_values[i].append(self.model.diodes[dio_selected[i]].get())
                #print(dio_selected[i])
                #print(self.model.diodes[dio_selected[i]])

            # this is the function that sends data for plotting to view
            self.view.plot_1d_scan(mot_selected=scan_dict["mot_sel"],dio_selected=dio_selected, mot_values=x_values, dio_values=diode_values)
            
            #nope this does not work?
            #update motor position on GUI:
            #self.view.update_current_motor_pos(scan_dict["mot_sel"])
            # I think this is where you need threading

        #TODO: 
        # move motore per step and read out at every step
        # if I had better access to the scan function, this whole function would be nicer 


    def motor_selection(self, event):
        """ Selects motors on event action """
        # this method is directly bound to the function, so we can make use of this option
        mot_selected = event.widget.get()
        #show the current motor value after selection in the GUI
        self.view.on_motor_selection(mot_selected)


    def show_scan_settings(self, event):
        """ Show scan settings on event action"""
        self.view.show_scan_settings()


def main():
    """ Setting the stage for the GUI action """
    # create model and add diodes, motors, camera
    # TODO: hide adding of motors in Model?
    model = Model()
    motors = {"MY-LARGE-MOTOR": "m", "MY-TINY-MOTOR": "nm", "MY-NORMAL-MOTOR": "mm"}
    for motor_name, units in motors.items():
        model.add_motor(motor_name, units)
   
    diodes = {"INTENSITY": None, "COUNTER": None, "SIGNAL": None, "XRF": None} 
    for diode_name in diodes.keys():
        model.add_diode(diode_name) 

    cameras = {"MY-CAMERA": None}
    for camera_name in cameras.keys():
        model.add_camera(camera_name)

    # prepare GUI
    view = View(model)
   

    # inject into Controller
    c = Controller(model, view)
   
    # start the GUI
    view.run()


if __name__ == '__main__':
    main()