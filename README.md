# cs417-semesterproject
Repository for CS417 semester project (Fall 2022)
Will be coded using Python 3.10.7

## Linear Interpolation and Global Least Squares Approximation
To find linear interpolation and approximated line using global least squares approximation, run the command:
`python ./src/main.py <input file in .txt format>`
This will generated 4 different .txt files (one for each core) containing: 
  * The collection of lines between point (linear interpolation)
  * The "line of best fit" for all of the core's temperatures (global least squares approximation)

## Piecewise Linear Interpolation
To run piecewise linear interpolation, run the command:
`python ./src/linear_interpolation.py <input file in .txt format>`
This will print 4 different .txt files (one for each core) containing the collection of lines between each point

## Global Least Squares Approximation
To run global least squares approximation, run the command:
`python ./src/global_least_squares_approx.py <input file in .txt format>`
This will print out the approximated line for each core's temperatures in the terminal