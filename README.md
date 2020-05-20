# Web Scraping - Download Multiple Google Images From A Single Command - Using Selenium

## Installation Documentation

    $ sudo apt install git

    $ git clone Web-Scraping-Download-Multiple-Google-Images-From-A-Single-Command-Using-Selenium.git
  
    $ cd Web-Scraping-Download-Multiple-Google-Images-From-A-Single-Command-Using-Selenium

    $ sudo apt-get install virtualenv

    $ virtualenv env

    $ source env/bin/activate
    
    $ sudo apt-get install python3.7
    
    $ sudo apt-get install python3-pip

    $ pip3 install -r requirements.txt
    
    $ cd home/model/
    
    $ wget https://www.dropbox.com/s/nn9975383dee3i6/piano_model.hdf5?dl=0 -O piano_model.hdf5
    
Each time when you want to download images, execute the following command:

	  $ scrapy crawl download -a searchword="<keyword>" -a no_of_images="<number>"
	 
All the images will be downloaded to the images/downloads folder

