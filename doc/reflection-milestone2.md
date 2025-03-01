# Reflection Milestone 2

**Name**: Amali Jayatileke, Kiran John, Kelsey Strachan, Jason Suwito

**Published**: February 14, 2025

### Landing page `dashboard-app-landing.py` (Page 1)

An overall landing page will introduce the user to the general theme of the dashboard. It contains an overview of all Canadian provinces and wildfire locations. It will prompt the user to proceed with navigating to the internal dashboard for plots and statistics.

### Dashboard `dashboard-app-main.py` (Page 2)

An interactive map visualization allows users to explore key wildfire data across British Columbia (BC), featuring attributes such as average wildfire size, fire causes, response efforts, occurrence month, and fire density in specific locations. These attributes can be selected via a dropdown menu. For better usability, the data is overlaid on Google Maps. Initially, this was implemented with Altair and Folium; however, performance issues arose when integrated into a Dash app. To address this, the map was transitioned to Plotly’s scatter_mapbox(), significantly improving dashboard performance while preserving interactivity. The map supports zooming and panning, enabling detailed analysis of wildfire causes, responses, size, and density across BC.
Supporting plots were created to showcase both BC-specific and province-wide wildfire data. These include a line plot showing average fire size from 2013-2023, with a dropdown for selecting specific provinces, and a bar graph displaying fire counts per province, where the legend enables users to filter data by year. A pie chart visualizes fire causes in BC with clickable legend to isolate specific causes. Interactivity and connectivity between these plots are still being refined. Originally created with Altair, the plots were rewritten in Plotly for better integration into the dashboard.

### Next Steps

* Combining Page 1 and Page 2 together into one dashboard app. 
* Linking the map visualization with selections made in the pie chart and scatter plots on Page 2.
* Adding a year filter slider, enabling users to adjust the time range and analyze wildfire trends over specific periods. 
* Potentially add animations for better User Experience
