# Automaton Dashboard

This is a graphical and easy to use automation flow designer. This is especially helpful for bot platforms that need to be orchestrated. This is based on a finite state machine approach in which the modules are connected between them and are able to actuate others. It is perfect to use in asynchronous environments where events happen suddenly and there is not a linear path. The main advantage of this approach is that there are no listeners turned on and listening all the time, in this approach all the modules are turned off and are only turned on when they are called and their pre-requisites have been fulfilled.

Example: The following image shows an automated human resources system on Linkedin. It is able to find relevant candidates, add them to contacts and contact them by sending them a message. All the actions happen asynchronously because we don´t know if a candidate will accept us as a contact and we don't know when it can happen.

![alt text](https://docs.google.com/drawings/d/e/2PACX-1vRxmrx764Goir0arSdxHMNMYDGhTm_KT6NGIPNIfaD5UC-ltB4qV61PwcrbYnQRdFHfTWip60QX6bO-/pub?w=1392&h=694 "Screenshot")

## Running User Interface

* Pre-requisites
    * Node.js
    * npm
    * nvm

* Steps
    * Go to ui/ folder in your command line.
    * Run the run.sh file

> cd ui

> ./run.sh

Open your browser and go to the given URL when the platform is up.

## Running Back End

* Pre-requisites
    * Python 2.x or 3.x
    * Selenium
    * PhantomJS
    * MongoDB
    
* Steps
    * Go to /automation folder in your command line.
    * Run the run.sh file

> cd ui

> ./run.sh

## Getting started

* Steps
    * Go to your user interface
    * Click on execute
