# Machine Learning deployment pipeline on Google Cloud Run

This project is a simple example on how to deploy your Machine Learning algorithm on Google Cloud in a Continuous Integration and Deployment (CI/CD) context. For this, I understand that you'll need to have this skills:

- Python: <span style='color:darkorange'>`Intermediate`</span>
- Flask: <span style='color:green'>`Basic`</span>
- Terminal: <span style='color:darkorange'>`Intermediate`</span>
- Docker: <span style='color:green'>`Basic`</span>
- Cloud: <span style='color:green'>`Basic`</span>

## TL; TR;

I configured a pipeline to deploy Machine Learning models on Google Cloud Platform (GCP) that starts with a `git push` in a GitHub repository and ends with a [Google Cloud Run](https://cloud.google.com/run) service running my application. Basically, the pipeline is as follows:

```
Local Repo > 
  Remote GitHub Repo >
    Google Cloud Build (trigger/image builder) >
      Google Container Registry > 
        Google Cloud Run
```
I followed some best practices to build my application in a way that the (re)building process is more efficient, like Dockerfile structure and caching images.

The technologies used to make the model application was:

- Python: `as language` 
- scikit-learn: `dataset & model`
- Pickle: `model object`
- Flask: `as web framework`
- Docker: `for image/container creation`

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
│   ├── loop_get.py
│   ├── loop_post.py
│   └── example.json
├── gcp_commands
│   ├── gcloud_config.sh
│   └── install_gcloud_sdk.sh
├── (+) screenshots
└── LICENSE

5 directories, 23 files
```

## Toy problem & the model entity

In this tutorial, I used the scikit-learn [Boston data set](https://scikit-learn.org/stable/datasets/index.html#boston-house-prices-dataset) to create my ML model. It is a regression of a continuous target variable, namely, price. To make it even simpler, I trained a [Linear Regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) model that also belongs to the scikit-learn package, but I could choose any other model (XGBoost, LightGBM, ...).

The folder named `train` contains a Python file, `boston_problem.py`, that loads the dataset, saves a JSON file (`example.json`) for test and saves the scikit-learn model object into a Pickle file (`ml-model.pkl`). Here is most important part of the code: 

 ```python
X.sample(1, random_state=0).iloc[0].to_json('example.json')
model = LinearRegression()
model.fit(X, y)
with open('ml-model.pkl', 'wb') as f:
    pickle.dump(model, f)
 ```

This is a very simple example of how to train a model and make it portable through the Pickle package object serialization. Whatever you go &mdash; for cloud or other computers &mdash;, if you have the same scikit-learn and Python version, you will load this Pickle file and get the same object of when it was saved.

Notice that in the `boston_problem.py` I put a command that prints the columns of my dataset. It's important because the order of columns matter in almost every algorithm of ML. I used the output of this command in my Flask application to eliminate possible mistakes.

## Flask application

Flask is a micro web framework written in Python. This API helped me to create an application that execute my model prediction function in a web address in the *localhost*. It's very simple, you only need to know three commands to expose your functions.

If you don't know anything about Flask, I recommend you to read the Todd Birchard articles [[1]](#L1).

The `app_files` folder contains two files: `ml-model.pkl`, the object that contains my exact created and trained model; and`app.py`, the application itself.

In `app.py`, to read the `.pkl`, I just used Pickle package:

```python
with open('ml-model.pkl', 'rb') as f:
    MODEL = pickle.load(f)
```

After that, I created a variable that I named `app` and it's a Flask object. This object has a [decorator](https://www.datacamp.com/community/tutorials/decorators-python) called `route` that exposes my functions to the web framework in a given URL pattern, e.g., _myapp.com**/**_ and _myapp.com**/predict**_ has `"/"` and `"/predict"` as routes, respectively. This decorator gives the option to choose the request method of this route. There are two main methods that can be simply described as follows:

- GET: to retrieve an information (message);
- POST: to receive an information and return a task result (another information/message);

I created one function for each method. The first is a message to know that the application is alive:

```python
@app.route('/', methods=['GET'])
def server_check():
    return "I'M ALIVE!"
```

And the second is my model prediction function:

```python
@app.route('/predict', methods=['POST'])
def predictor():
    content = request.json
    # <...>
```

Remember that I said that for almost every algorithm the column order is important? I made a `try`/`except` to guarantee that:

```python
    try:
        features = pd.DataFrame([content])
        features = features[FEATURES_MASK]
    except:
        logging.exception("The JSON file was broke.")
        return jsonify(status='error', predict=-1)
```

The last two command lines runs the application into the IP `0.0.0.0` (localhost) on the port `8080`, if the system has no environment variable named `PORT`. This environment variable is important to deploy on Google Cloud.

```python
if __name__=='__main__':
    app.run( debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)) )
```

The conditional statement is because I just want to run my application if I am executing `app.py`. 

## Request Tests

In folder `request_test` I have two Python files to each request method that makes infinity loops. I used this programs to test my local and cloud Flask applications. To change between local and cloud application, we just have to change the URL address, e.g., http://localhost:8080/predict > http://myapp.com:8080/predict.

## Docker & Dockerfile

Docker is an excellent container image manager and did the system isolation work for me. I just made a simple Dockerfile, but I have two tips for you:

- If your application don't need a whole operating system, you can get small base image to you application. Instead of `ubuntu:18.04` you can choose `python:3.6`; instead of `python:3.6` you can choose `python:3.6-slim-buster`; and so on.
- A container image is built of layers. Every command is a layer. If something change in the command (the content of a file, the command itself, ...) the layer changes. The tip here is to use cache images, i.e., to use a pre-built image and it's layers in the process of building a new image. For this, put the commands and layers more prone to change in the end of the file. The classical layer to put in the first lines is the one to install dependencies.

This is my Dockerfile:

```dockerfile
# a small operating system
FROM python:3.6-slim-buster
# layers to install dependencies (less prone to changes)
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
# layers to copy my files (more prone to changes)
COPY . /app
WORKDIR /app/app_files
# starts my application
CMD ["python", "app.py"]
```

NOTE: I lost sometime to understand the difference between commands RUN, CMD and ENTRYPOINT. If you wanna know this too, I recommend you to read Yury Pitsishin's article [[2]](#L2).

## GitHub Repo

HERE!

## Google Cloud Build - The trigger

## YAML Ain't a Markup Language - `cloudbuild.yaml`

## Google Container Registry

## Google Cloud Run

## Cloud request

## Conclusion

## References

<a name="L1">[1]</a> Todd Birchard ["Building a Python App in Flask"](https://hackersandslackers.com/your-first-flask-application/). July, 2008. _(visited April 20, 2020)_
<a name="L2">[2]</a> Yury Pitsishin ["Docker RUN vs CMD vs ENTRYPOINT"](https://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/). April 2, 2016. _(visited April 20, 2020)_