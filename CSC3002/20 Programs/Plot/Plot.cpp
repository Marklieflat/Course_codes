/*
 * File: Plot.cpp
 * --------------
 * This program illustrates the use of functions as arguments by plotting
 * mathematical function on the graphics window.
 */

#include <iostream>
#include <cmath>
#include "gmath.h"
#include "gwindow.h"

/* Function prototypes */

void plot(GWindow & gw, double (*fn)(double),
                        double minX, double maxX,
                        double minY, double maxY);

/* Main program */

int main() {
   GWindow gw(600, 400);
   plot(gw, cos, -2 * PI, 2 * PI, -1, 1);
}

/*
 * Function: plot
 * Usage: plot(gw, fn, minX, maxX, minY, maxY);
 * --------------------------------------------
 * Plots the specified function (which must map one double to another
 * double) on the screen.  The remaining arguments indicate the range
 * of values in the x and y directions, respectively.
 */

void plot(GWindow & gw, double (*fn)(double),
                        double minX, double maxX,
                        double minY, double maxY) {
   double width = gw.getWidth();
   double height = gw.getHeight();
   double nSteps = int(width);
   double dx = (maxX - minX) / nSteps;
   double sx0 = 0;
   double sy0 = height - (fn(minX) - minY) / (maxY - minY) * height;
   for (int i = 1; i < nSteps; i++) {
      double x = minX + i * dx;
      double y = fn(x);
      double sx1 = (x - minX) / (maxX - minX) * width;
      double sy1 = height - (y - minY) / (maxY - minY) * height;
      gw.drawLine(sx0, sy0, sx1, sy1);
      sx0 = sx1;
      sy0 = sy1;
   }
}
