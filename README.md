## DSF-2020: Royal Mail Workshop

### Title

*"Going postal: how to craft a cutting-edge route optimisation engine in-house that suits your business needs"*
 
### Abstract

Royal Mail is the UKs national postal service, delivering 15 billion items to 31 million addresses annually.
Despite handling more than 50% of British parcels, Royal Mail is on the look out for efficiency in this extremely dynamic
and competitive market. While protecting operational cost and enhancing customer satisfaction are our main drivers,
designing a new dedicated parcel delivery service from scratch is no small feat…but the Data Science team is here to help!

Route optimisation technology has now become invaluable in the logistics market and is driving high impact in the
Last Mile delivery journey. Based on a long academic history that started with the well known Traveling Salesman Problem,
route optimisation is one of these NP-hard computational problems that requires creative algorithms to extract value
from an extremely challenging combinatorial problem. While it is true that there is a range of very good
software providers in this space, there are also many incentives to develop an in-house capability,
most notably the ability to build a tailored solution for the specific postal constraints.

Building on last year presentation of the general problem, this 3 hours interactive session will allow us to go
through the entire cycle of a PoC project, covering stakeholder requirements, data acquisition, algorithmic modelling
as well as service delivery review. In particular, we will show how heuristics can be crafted manually to match up
with a standard VRP library.

### Target Audience

This workshop is designed for all kind of Data Scientists, from hand-on developers to more managerial roles.

### Prerequisites

- Basic python development environment (pip, python=3.6)
- Standard libraries, such as pandas and numpy
- We will also make use of Google OR-Tools library: https://developers.google.com/optimization/routing/vrp
- Finally, highly beneficial if attendants are familiar with last year’s DSF talk from Royal Mail.
Record can be found here: https://youtu.be/XeccXJ9SI0g

### Schedule (GMT)

-  9:00 - 10:00: Business and science context + data management and exploration
- 10:00 - 10:10: Break + Q&A
- 10:10 - 11:10: Optimisation objective, algorithmic design + MVP development
- 11:10 - 11:15: Break + Q&A
- 11:15 - 12:00: Result exploration + wrap-up

### Installation

#### Setting up Virtual Environment [Linux or Mac]

Clone this repo with:
```bash
git clone https://github.com/fdurier/dsf_2020_royalmail.git
cd dsf_2020_royalmail/
```
Create Virtual **(Linux/Mac)** Environment:
```bash
python -m venv royalmail_env
source royalmail_env/bin/activate
```
Make sure that, from now on, you **run all commands from within your virtual environment**.

#### Setting up Virtual Environment [Windows]
Use the [Github Desktop GUI](https://desktop.github.com/) to clone this repo to your local machine.
Navigate to the `dsf_2020_royalmail` project folder and open a power shell window by pressing **Shift + Right Click**
and selecting `Open PowerShell window here` in the drop-down menu.

Create Virtual **(Windows)** Environment:

```powershell
py -m venv royalmail_env
.\royalmail_env\Scripts\activate
```
Make sure that, from now on, you **run all commands from within your virtual environment**.

#### Install Required Packages [Windows, Mac or Linux]
Install required packages (from within your virtual environment) via:

```bash
pip install -r requirements.txt
```
If this fails, you may have to upgrade your pip version first with `pip install pip --upgrade`.

## Quick Start Guide
We will start exploring and developing the codebase via a notebook:
```bash
jupyter notebook DSF_main.ipynb
```

## Full Pipeline
Once the pipeline will be complete, a simple launch through the command line will run the optimisation engine:

```bash
cd ./src/
python main.py
```


