# driving-analytics-simulation
This repo is composed of a bunch of little different services to understand event-driven micro-services communication.

You will also have conceptual info about building web applications built on top of python/django, RESTful APIs built on top of node.js/express, websockets servers built on top of node.js/websocket

## Services
- zookeeper (resource management for kafka)
- kafka (service communication, message broker, distributed task queue)
- event_simulator_db (used by event_simulator_web)
- event_simulator_web (create dummy trips to simulate later on) - `Python + Django + Kafka`
- event_simulator_worker (distributed task queue for event simulation) - `Python + Kafka + Multiprocessing`
- event_handler_api (REST API for receving events like location, driver behaviour etc) - `Node.js + Express + Kafka`
- locations_ws_server (a ws server to receive location data from related kafka topic and send them to the connected clients) -  `Node.js + websocket + Kafka`
- driving_analytics_ws_server (same with previous ws server, listens driving_analytics topic for such an events like "hard break", "speed limit" etc.)
- simulation_insights.html (an individual file that contains simple ws client and some google maps code snippets, you can double click this later on once you are ready on launching all services and starting simulation)

## Running docker-compose
- docker-compose build --no-cache
- docker-compose up
### Fixing unexpected issues
Despite the fact that each services are well designed in terms of priority. However, `kafka` server post running scripts somehow might late creating `topics` and other services fail accordingly.  Another issue in first launcing would probably be database tables for `event_simulator_web`. To be able to fix those;
>  iterate running and killing docker-compose up until you have access to localhost:8000 which is the first entry point for the simulation

## Time to create admin account for event_simulator_web and create a few dummy trips
- Find container id of `event_simulator_web` 
     >    docker container ls
- Create a super user, follow the instructions after running below command
     >    docker exec -ti <container_id> python manage.py createsuperuser
 - Now you can add some dummy trips. Go to http://localhost:8000/admin/, login with credentials that you created previously and click `Dummy trips` on the menu
 - Click `Add Dummy Trip` on the top, right
 - Specify a `operator name` and `polyline` (should be google encoded polyline that simulation will be iterating coordinates respectively)

##  Running simulation
- Open `simulation_insights.html` in a ws supported browser.
- Go to http://localhost:8000/admin/trips/dummytrip/ in another tab, choose dummy trips to be simulated, select `Start Simulation` from the dropdown and click `Go`
- Go back to `simulation_insights` page and enjoy the events!
### Some Hints
- Map center point is in Istanbul, you might want to change it
- You should be adding your own google maps api key, replace `<yourapikey>` with your key in .html file 

## Overall Diagram
![ScreenShot](https://raw.github.com/baranbartu/driving-analytics-simulation/master/diagram.png)
