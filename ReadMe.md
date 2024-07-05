# Research Project on Honeypots deployment for real time risk assessment
Welcome to the repository of our research project on threat intelligence and simulation. This repository contains various utilities, scripts, data utilities, and simulations related to our research.

## Repository Structure
BAG_Code: Contains various Python utilities for runing Bayesian inference.

Scripts: Includes different scripts used for building the graphs and draw them.

Threat_intelligence: Contains the different tables to define the average profile of a threat actor.

Personnal_simulation: Includes simulation files and their results.

Main Directory: Contains the playbooks to run the simulation, the baseline and the comparison.

## Getting Started
To get started with the project, clone the repository to your local machine using the following command:
'git clone https://github.com/NathanaeldeLaChesnais/ImperialWork.git'

### Prerequisites
Ensure you have Python installed on your machine. You can download it from python.org.
Additionally, install the necessary Python packages by running:
'pip install -r requirements.txt'

Make sure you also have a distribution of graphviz https://graphviz.org/download/ to draw the graphs.

### Running the Project
To build the graph, place your mulval file in the Personnal_simulation folder and run './Scripts/Build_graph.psi'
Then you can exploit the graph and run all inferences on it through the playbooks

## Acknoledgements


## License
This project is licensed under the GNU General Public License. See the LICENSE file for more details.

