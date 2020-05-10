# Boundary Layer Sphere
**points_generator.py** 
1. Generates datapoints around the Sphere in the XY plane, stored in the file *data.csv*. Radius and Frequency of Angles are parameters.
2. Load the datafile generated onto TecPlot as *Text Spreadsheet Loader*.
3. Interpolate *X*, *Y*, *u*, *v*, onto the newly created zone and *Wrtie Data as Formatted Text* in the same order. 
4. Save the file as *tcdata.csv*

**calculate.py**
1. Calculates the Velocity Profile, Boundary Layer Thickness, Displacement Thickness and Momentum Thickness for flow past sphere. Radius and Frequency of Angles are parameters.
2. Stores the Boundary Layer in *bl.csv*, Displacement Thickness in *dis.csv*, and Momentum Thickness in *momen.csv*. These files can be loaded onto the TecPlot figure. 

![Velocity Profile](/../media/vel_pro.png)
![Boundary Layer Characteristics](/../media/boundary_layer_chars.png)

**plotter.py**
1. Plots Boundary Layer Characteristics. _Under Testing_

