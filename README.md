# DSA Search_Engine

This web development  project is on building a Search Engine dedicated for finding Data Structure and Algorithm problems.
* [ My Deployed app](https://dsa-search-engine-ss.herokuapp.com/)


## Description
This project is on a [search engine](https://dsa-search-engine-ss.herokuapp.com/) which takes an input from a user in the search box and returns top 10 matches of DSA Problem from the database.
Database for this project consists of around 1500 questions.
We build this project and then deployed it using heroku.

## Getting Started

### Dependencies
To work with this project you need:-
* OS :-  any (I worked on Windows10)
* [Pycharm](https://www.jetbrains.com/help/pycharm/installation-guide.html#toolbox):- 
  * used pycharm for pycthon codes.
* [VS](https://code.visualstudio.com/download) :- 
   * for help in VScode_setup [visit here](https://github.com/john-smilga/VS-CODE-SETUP)
   * used vs_code to write javascript, ejs and css codes.
* [Git](https://git-scm.com/downloads)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

### Installing

* Downloading this  project on your PC:-
  * [visit here]( https://github.com/Shruti192/DSA_SE)
  * select code (in green colour)
  * select HTTPS
  * click on Download zip
* After downloading visit to downloads and extract the usable folder from the zip folder.

### File Description:-
Open the extracted file in VS code: you should see following files-
* **[Web_scraping.py](https://github.com/Shruti192/DSA_SE/blob/main/web_scraping.py)**: This file contains code written in python to scrape data from the website we want data, to prepare a DataBase.
* **[BM25_requirements.py](https://github.com/Shruti192/DSA_SE/blob/main/BM25_requirements.py)**: This file contains code written in python ho prepare some of the files and folders that we will need while calculating similarity score using [BM25](http://ipl.cs.aueb.gr/stougiannis/bm25.html) Algorithm.
* **[app.js](https://github.com/Shruti192/DSA_SE/blob/main/app.js)**:  This file contains javascript code and is backbone of the project this is from where the project will start running. It contains the info about on which port our app will be running and handles the fired request. This also contains BM25 smilarity algoritm  which gets executed whien /search is fired which gets fired when we click on "Ask Me" button near search box.
* **[Procfile](https://github.com/Shruti192/DSA_SE/blob/main/Procfile)**: This is a text file.
  Heroku apps include a Procfile that specifies the commands that are executed by the app on startup. Read more in detail about it [here](https://devcenter.heroku.com/articles/procfile).
* **gitignore**: This is a text file that specifies intentionally untracked files that Git should ignore. Read more about it [here](https://git-scm.com/docs/gitignore).
* **[Package.json](https://github.com/Shruti192/DSA_SE/blob/main/package.json)**: This file contains different project-related metadata. This file is used to provide information to npm so that it can identify the project and handle its dependencies. It may also include other metadata like as a project description, the version of the project in a certain distribution, licence information, and even configuration data, all of which are important to both npm and the package's end users. Read more about it [here](https://nodejs.org/en/knowledge/getting-started/npm/what-is-the-file-package-json/).
* **[README.md](https://github.com/Shruti192/DSA_SE/blob/main/README.md)**: This file contains details about project, it's directories and how to get started with this project and how to use it.
* Folder **[public](https://github.com/Shruti192/DSA_SE/tree/main/public)** which contains following files:- 
  * **styles.css**
  * images: used in styles.css
* Folder **views** which contains following files:- 
  * **index.ejs**
  * **detail.ejs**
  * **error.ejs**
  * **partials_folde**r: which further contains:- 
    * **header.ejs**
    * **footer.ejs**
    * **nav.ejs**



### Executing program
* Open the extracted file in VS code:-
* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
