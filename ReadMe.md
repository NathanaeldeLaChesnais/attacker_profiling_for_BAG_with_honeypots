# Research Project on Honeypots deployment for real time risk assessment
Welcome to the repository of my research project on Honeypots deployment for real time risk assessment. This repository contains various utilities, scripts, and simulations related to my research. It is the resulting code of my research project at Imperial College.

## Repository Structure
BAG_Code: Contains various Python utilities for runing Bayesian inference.

Scripts: Includes different scripts used for building the graphs and draw them.

Threat_intelligence: Contains the different tables to define the average profile of a threat actor.

Personnal_simulation: Includes simulation files and their results.

Main Directory: Contains the playbooks to run the simulation, the baseline and the comparison.

## Getting Started
To get started with the project, clone the repository to your local machine using the following command:
`git clone https://github.com/NathanaeldeLaChesnais/ImperialWork.git`

### Prerequisites
Ensure you have Python installed on your machine. You can download it from python.org.
Additionally, install the necessary Python packages by running:
`pip install -r requirements.txt`

Make sure you also have a distribution of:
 - graphviz https://graphviz.org/download/ to draw the graphs;
 - windows subsystem for linux https://learn.microsoft.com/en-us/windows/wsl/install;
 - Docker desktop https://www.docker.com/products/docker-desktop/.

Some scripts are designed to be run on the wsl system, but they re easily adaptable to a general version of Linux.

### Running the Project
To build the graph, place your mulval file in the Personnal_simulation folder and run `./Scripts/Build_graph.ps1`
Then you can exploit the graph and run all inferences on it through the playbooks

## Acknowledgements
Professor Emil Lupu

Luca Castiglione

Tao Wang

Institute for Security Science and Technology (ISST) at Imperial College.

## License
This project is licensed under the GNU General Public License. See the LICENSE file for more details.

