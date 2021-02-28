# PROXCITY📍
Be sure to visit [PROXCITY](https://proxcity-app.herokuapp.com/) to “Find, Help, and Save” a local business in your city close to your proximity!


 ## Table of Contents
 * [About this Project](#about-this-project)
 * [Functions to Highlight](#functions-to-highlight)
 * [Deployment](#deployment)
 * [Demo](#demo)
 * [More Info](#more-info)
 
## About this Project
PROXCITY is a simple and easy way to find local businesses 
<br><br>
During the covid pandemic, small/medium local businesses suffered greatly. So we thought, why don't we make it easier for them to get noticed? This project is aimed at helping local businesses market their name by making it easier for users <b>"Find, Help, and Save"</b> them. 

## Functions to highlight
* Use of FourSquare API
* CRUD of favorite places
* Authetication


## Deployment
In a terminal window, navigate to your newly created folder and clone:
```bash
git clone git@github.com:git@github.com:Kou-kun42/proxcity.git
```
Next, go to GitHub.com and create a new repository for your project. <b>IMPORTANT</b>: Make sure the box for “Initialize with a README” is NOT checked. Then, run the following commands to push your starter code to GitHub:

```bash
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin master
```

Deploy virtual environment.
```
python3 -m venv auth
source auth/bin/activate
```

Run the following commands from your virtual environment to install the needed packages
```bash 
pip3 install -r requirements.txt
```

On a development server
```bash 
# run
python3 app.py
```

## Demo
![alt text](2_28_gif.gif "Demo Giphy")

# More Info
For more information visit websites:
> [FourSquare API Documentation](https://developer.foursquare.com/docs/places-api/)
> [Ziptastic Documentation](http://ziptasticapi.com/)
