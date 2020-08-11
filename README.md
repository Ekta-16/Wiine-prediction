# Wiine-prediction

## Description
The primary functionality of the system is to develop an algorithm by building a model to determine the quality of wine based on the user reviews by addressing the various issues, being a personal sommelier to the user. The algorithm takes user data and reviews as input and returns the quality of that wine based on the set of optimal wine reviews classified into different review scales. In order to create a dataset, the data has been web scrapped from the available wine enthusiast magazine website which consists of 1,30,000 wine reviews using python. The dataset consists of various length of text reviews. Data cleaning, tokenization, stemming, removal of stop words is all a part of this information retrieval process
		
## Installation
This project to introduce you to Natural Language Processing with data analysis and Machine Learning on Wine Data. This project can also be used as a reference for classification or prediction of any other datasets. 

	Select any of the options for setting up your Machine Learning environment Once you are set with one of the python environment configurations it’s time to start building:
	1.Import the necessary packages. Use the webcrawl.py to web scrape the data and then validate the json file. 
	2. Using convert.py to transform the json file into csv for further data analysis. 
	3. Import required packages, libraries and data for the preprocessing. 
	4. Preprocessing of data includes imputing missing values, removing the unnecessary attributes and performing the NLP like removal of stop words, stemming, tokenization to build a dictionary of wine description of sensible words. 
	5. Train and Test the model using the test.py python file
