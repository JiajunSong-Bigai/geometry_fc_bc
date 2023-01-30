## Installation

0. Python version must be <= 3.9. Python 3.10 is not supported.
1. Must have clingo on the path. For example, on ubuntu terminal run `sudo apt install gringo` to install clingo.
2. Launch a virtual environment and install the dependencies by `pip install -r requirements.txt & python setup.py develop`.

## Usage


## Background

Here we are building from scratch a reasoning tool that gives human readable proof process based on given facts and goals, specifically in the case of geometry problem solving.


* knowledge base

Example first-order-logic rules

1. on_same_line(A,B,C) :- pointLiesOnLine(A,line(B,C)).
2. equals(measureOf(angle(A,B,D)),measureOf(angle(B,D,E))) :- parallel(line(A,B),line(D,E))^ not A==D^ not B==D^ line(B, D)^ pointPosition(A,Xa,Ya)^ pointPosition(B,Xb,Yb)^ pointPosition(D,Xd,Yd)^ pointPosition(E,Xe,Ye)^ (Xa-Xb)*(Xe-Xd)<0.



* forward chaining

done by xclingo

*  backward chaining

