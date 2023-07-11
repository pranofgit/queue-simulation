# queue-simulation
implementation of queue simulation 

# Folder Structure
* Code: Contains the main code files.
  * gg1.py: Implementation of the GG1Queue class and related functions.
  * main.py: Example implementation of the queue simulation.
  * main_nb.ipynb: Jupyter Notebook version of the example implementation.

## Currently Supported Probability Density Functions (PDFs)
The GG1Queue class supports the following PDFs for both service and arrival times:

Normal (PDF.NORMAL)
Exponential (PDF.EXPONENTIAL)
Weibull (PDF.WEIBULL)
Uniform (PDF.UNIFORM)
Hawkes (PDF.HAWKES)
Custom (PDF.CUSTOM): Use it to define custom process in inherited child classes

Refer to the code for specifying arguments for these PDFs.
