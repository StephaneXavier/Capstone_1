# Capstone_1: OC transpo late bus tracker

This project is an attempt to have user generated data that keeps track of OC transpo's delays / no shows. OC transpo in recent years has been an 
unreliable service to Ottawan's. My hope with this project is to add some numbers to the issue. That way people can quantify the problem in concrete terms. The web application has been deployed on heroky, here: https://late-again.herokuapp.com/

Users can:
- create accounts, which allows them to see the data points they have submitted. An accout is not necessary to use any of the application's functionality;
- report when buses are late or when they don't show up;
- look up the next bus arrival times; and
- search the database for data submitted by other users.

The project used the following technologies:
- Flask;
- SQL-Alchemy;
- Jinja;
- WTForms;

The API used for this project was the OC tranpo API, to get the bus and stop numbers.

The technologies were selected based on the fact that I'm a total newb and that's all I know so far. The project is very much a work in progress, as you will be 
to tell from the potato UX. I hope to make it prettier and sleeker as I have the time. Furthermore, I plan to eventually add some sort of geographical verification, 
because as of now anyone from any location in the world can submit data. 

