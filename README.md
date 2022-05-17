# Fall 2022 Shopify Developer Intern Challenge

Welcome to my submission for Shopify's intern recruitment challenge :D

## Getting Started
[![Run on Repl.it](https://repl.it/badge/github/julia-zhao/for-shopify)](https://repl.it/github/julia-zhao/for-shopify)

Feel free to click that button above to take you to the repl.it link where the app can be ran out of the box!
Once you click `Run`, please allow a few minutes for the repl package manager to install the required packages: 

Frontend:
* flask
* flask_cors

Backend:
* replit
* json

## Additional Details
The app runs on `localhost:5000` by default. To change this setting, modify line 57 in `app.py`.

The `.replit` file should contain the following lines:
```
language = "python3"
run = "python3 backend/app.py"
```

### Controls
Enter an integer to replace the current value, or enter an integer preceeded by a + or - (e.g. +4, -6) to add or subtract from the current value.

## Features
The app fulfills basic CRUD functionality. Furthermore, it is possible to create "shipments" and assign existing inventories to them (which automatically adjusts the inventory as well). 

For example, if we have 20 bananas, we can move 12 of them into shipment A such that there are 8 bananas left in inventory and 12 of them in A.

## Design Decisions
### Libraries, frameworks, tools, etc.
This app uses the `Flask` framework with basic HTML to create a simple frontend, and the inbuilt `Replit Database` with the online IDE to store permanent information. Both of these were chosen for the ease-of-setup that they offer, because the scale of the project is relatively small.

In the case of turning this project into more than just Proof-of-Concept, I would prefer to use a NoSQL database such as `MongoDB` as it contains much more functionality and organization. 

A NoSQL database would be preferred over SQL due to how shipments are irregularly structured - they can contain multiple types of inventories (e.g. bananas, apples); as such, they are best represented in JSON format which NoSQL does best.

Furthermore, I would incorporate a frontend language such as `Vue.js` to make the frontend design more flexible and powerful. 

### Operation
When using the app, you may notice that it is particularly picky about the order of operations. For instance, a user is not able to edit an inventory without creating it first. 

This was a conscious decision - without such checks, users will be extremely prone to human error (i.e. typos) and may accidentally create a new entry when they actually meant to edit an existing one. This would make the database messy and difficult to search as it expands. 

