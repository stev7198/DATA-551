## Milestone 2 Reflection

### Progress

Our dashboard currently uses a dataset found here: https://www.kaggle.com/datasets/vivekattri/global-ev-charging-stations-dataset/data. This dataset contains information on electric vehicle (EV) charging stations around the world. It includes various details such as location, charger types, and station operator. 

So far, we have linked the data to a world map to show all the locations of the chargers. The user can navigate the world map, and scroll to zoom in to view the charging stations which are represented as red dots. After scrolling over a point, the user will see the station ID, address, charger type, availability, and cost of the charging station in USD/kWh. On the left side of the dashboard, we have a filter option for type of charger. The user can select to filter for all chargers, or only display specific types (e.g. AC level 1, DC fast charger). In addition to this, there is a slide bar to select the year. The user can slide the bar to a desired year to only display the charging station data from that year. 

### Future Improvements

This dashboard is currently intuitive and approachable, in that a user can easily view all charging stations in the dataset and navigate to different parts of the map. This dashboard does well to display a digestible amount of information for the user. However, we are planning to implement a section of the dashboard in the lower left corner that displays summary statistics. It will display a summary of information depending on which stations the user has filtered for with the two filtering options available. Here, we plan to display the number of connectors, the average review score, the average cost, and the average number of spots. This will add information to users without crowding or overloading the dashboard too much. 

One difficulty we have encountered so far is that some stations in specific urban centres appear to have coordinates located just offshore. We will be investigating if there is some error in the data; it is possible that the coordinates are slightly inaccurate for some points which may be the cause of some charging stations being located offshore. 

Overall, our dashboard currently provides valuable information to the user while being easily readable. Manufacturers can use it to gather information on potential market gaps or geographical locations lacking EV access so that they can plan for future charging station development. They can even see changes in development over time using the year filter. The next steps to take that we will take to improve the dashboard are adding the summary statistics section and reviewing some possibly erroneous data points as mentioned earlier. The summary statistics will allow users to have a more holistic view of the data to better identify market gaps and opportunities. 
