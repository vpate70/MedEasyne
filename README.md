To host the website, you'll need to start up the Uvicorn server by running from the project directory:

python ./backend/main.py

And then the frontend is accessible by starting as any React app, first cd'ing to the React app, then running npm start:

cd ./frontend/react/my-app && npm start

For the search to work, you need an appropriate Whoosh index folder. To create the index we use in the paper, which is a subset of the PubMed database, run 

python ./backend/indexmaker.py

This will create an index folder ./backend/index, which is where our code expects it to be. If you wish to use your own database and hence create your own index, refer to the Whoosh documentation regarding that: [Whoosh Indexing Documentation](https://whoosh.readthedocs.io/en/latest/indexing.html)
