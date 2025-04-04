## Overview 
- This program is one half of my dissertation, it contains the GUI, data logging and
notebooks required to create the graphs and stats tests. 

## Setting up the codebase the GUI 
- First make sure that you have any version of python after 3.12
- create a virtual environment in python `python -m venv my_venv` 
- activate the virtual environment `source my_venv/bin/activate` for unix based os 
    - `my_venv\Scripts\activate` for windows OS
- install pip (if you haven't got it already) `python -m ensurepip --upgrade`
- install the required packages using pip `pip install -r requirements.txt`

## Running the Code 
- make sure you are in the correct directory (diss_code) and your virtual environment is  active 
- Next run `python -m src.UI.app` This will start the GUI as a python program, it may appear as a rocket on the task bar

## Using the GUI 
- Once the GUI is running, simply input the data to the first page, User iD, age, gender, room temp. The hours of manual labour section is not important, I initially thought that it could be useful but after conducting the user studies it's not needed 
- Once you are on the calibration screen you can use the select monitor section to scan for connected devices. 
- When you can access the 