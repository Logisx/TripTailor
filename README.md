# UNDER CONSTRUCTION

# TripTailor

## How to Start the Application

### Prerequisites
The app is using **Python 3.12.0** 

Create `.env` file and add the relevant API keys and your Redis server url. Use `env_example.txt` as a template for your env file.

### Option 1: Using Poetry (Preferred)
1. Install Poetry if not already installed:
   ```bash
   pip install poetry
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Start the application:
   ```bash
   poetry run python -m triptailor.main
   ```

---

### Option 2: Using `requirements.txt`
If Poetry is not available, use `pip` to install dependencies.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the application:
   ```bash
   python -m triptailor.main
   ```


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks for initial experiments
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         triptailor and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
├── Procfile           <- File defining how to start the app for Heroku
│
└── triptailor   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes triptailor a Python module
    │
    ├── etc/defaults.cfg        <- Store useful variables and configuration
    │
    ├── logger.py               <- Initialized logger
    │
    ├── main.py                 <- Starts up the application
    |
    ├── routes.py               <- Defines API routes
    |
    ├── templates/              <- HTML templates for Flask to render  
    |
    ├── modeling                
    │   ├── __init__.py 
    │   ├── agent.py            <- Class defining the pipeline of LLM calls         
    │   ├── data_schemas.py     <- Contains desired output format for the LLM calls          
    │   ├── inference.py        <- Class running a pipeline to generate itinerary          
    │   ├── prompts.py          <- Contains prompt templates used to form an LLM request          
    │   └── itinerary_example.json <- Sample itinerary used when debugging
    │
    └── static/                 <- CSS and JS files for the frontend
```

--------

