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
'git clone https://github.com/NathanaeldeLaChesnais/ImperialWork.git'

### Prerequisites
Ensure you have Python installed on your machine. You can download it from python.org.
Additionally, install the necessary Python packages by running:
`pip install -r requirements.txt`

Make sure you also have a distribution of graphviz https://graphviz.org/download/ to draw the graphs.

### Running the Project
To build the graph, place your mulval file in the Personnal_simulation folder and run `./Scripts/Build_graph.ps1`
Then you can exploit the graph and run all inferences on it through the playbooks

## Acknoledgements
I am deeply grateful to Professor Emil Lupu, who accompanied me throughout the project as my supervisor. He introduced me to attack graph, the base of the development of my project and oriented my research all along. He kept me in the right direction without restraining me from exploring new tracks.

Special thanks to Luca Castiglione for his explanations more in depth for the use of tools to produce Bayesian inference, as well as for the discussion we had on how to use attack graphs and how to extend them for new use cases.

I would also like to thank Tao Wang for his help with the python libraries for Bayesian inference and his opening on Markov random field.

At last, I would like to thank the Institute for Security Science and Technology (ISST) for hosting me during these four months at Imperial College.

## License
This project is licensed under the GNU General Public License. See the LICENSE file for more details.

