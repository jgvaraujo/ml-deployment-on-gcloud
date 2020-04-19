# Machine Learning deployment pipeline on Google Cloud Run

## TL; TR;

I configured a pipeline to deploy Machine Learning models on Google Cloud
 Platform (GCP) that starts with a `git push` in a GitHub repository and ends
 with a [Google Cloud Run](https://cloud.google.com/run) service running my
 application. Basically, the pipeline is as follows:
```
Local Repo > 
  Remote GitHub Repo >
    Google Cloud Build (trigger/image builder) >
      Google Container Registry > 
        Google Cloud Run
```
I followed some best practices to build my application in a way that the
 (re)building process is more efficient, like Dockerfile structure and caching
 images.
 
The technologies used to make the model application was:
```
Python (as language) >
  scikit-learn (dataset & model) > 
    Pickle (model object) >
      Flask (as web framework) >
        Docker (for image/container creation)
```

## Project tree

```
ml-deployment-on-gcloud/
├── README.md
├── cloudbuild.yaml
├── Dockerfile
├── requirements.txt
├── train
│   ├── boston_problem.py
│   ├── example.json
│   └── ml-model.pkl
├── app_files
│   ├── app.py
│   └── ml-model.pkl
├── request_test
│   ├── caller_loop.py
│   ├── caller_single.py
│   └── example.json
├── gcp_commands
│   ├── gcloud_config.sh
│   └── install_gcloud_sdk.sh
├── (+) screenshots
└── LICENSE

5 directories, 23 files
``` 

## Toy problem & the model entity

In this tutorial, I used the scikit-learn [Boston data set](https://scikit-learn.org/stable/datasets/index.html#boston-house-prices-dataset)
 to create my ML model. It is a regression of a continuous target variable,
 namely, price. To make it even simpler, I trained a [Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
 model that also belongs to the scikit-learn package, but I could choose any
 other model (XGBoost, LightGBM, ...).
 
The folder named `train` contains a Python file, `boston_problem.py`, that 
 loads the dataset, saves a JSON file (`example.json`) for test and saves the
 scikit-learn model object into a Pickle file (`ml-model.pkl`). Here is most 
 important codes: 
 ```python
X.sample(1, random_state=0).iloc[0].to_json('example.json')
model = LinearRegression()
model.fit(X, y)
with open('ml-model.pkl', 'wb') as f:
    pickle.dump(model, f)
```
 
This is a very simple example of how to train a model and make it portable 
 throught the Pickle package object serialization. Whatever you go &mdash; 
 for cloud or other computers &mdash;, if you have the same scikit-learn and
 Python version, you will load this Pickle file and get the same object of
 when it was saved.

## Flask application



## Local request

## Docker & Dockerfile

## GitHub Repo

## Google Cloud Build - The trigger

## YAML Ain't a Markup Language - `cloudbuild.yaml`

## Google Container Registry

## Google Cloud Run

## Cloud request

## Conclusion

## References