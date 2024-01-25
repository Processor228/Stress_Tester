# Stress Tester

This repository contains the backend part of the implementation
of a competitive programming stress testing platform.

What exactly is stress testing in CP? Let me explain...

Suppose you have a solution to some problem A that you are very sure of (a bruteforce, for instance). And you have a solution B for that problem that (maybe more optimal) you are not sure of. So, you 
may wanna run some tests to figure out, whether their output coincide or, more importantly,
differ. This application (with some good UI) may come in handy for such problems. (This will be useful only in case there is just
one correct output for an input)

# Deployment procedure:


# Project structure:
We have monolith here, the logic is separated between two modules: one handles room management 
(just code files user wish to test) and stress-testing logic, where the most important
stuff is. <br>
Each module has:
- schemas.py - for types used in the module
- file with helping procedures (e.g. crud or like testing implementation)
- router - for endpoints
- models - possibly db models

main.py contains the FastApi class instance and there all the modules endpoints are binded to it.<br>
db_connection - connects to db.

Seems to be easy and structured... let's see what I and others will say after a while...

Running instance:
Not yet deployed

