# **Welcome to StarChaser!!!**


StarChaser is an app aimed at helping those individuals seaking to enjoy a nice clear sky for stargazing! In it there are 5 main features.

CORE APP:
1. Map showing campsites overlayed with the light pollution. Also can zoom in, see different campsites at each level/popular campsites even if don't have great stargazing. Click campsite leads to 2day's report. Click somewhere shows you the spots stargazing report. Map should load with a certain zoom level say of USA and have maybe 20-50 best places for stargazing (semi widely spread across the map). Then as you zoom in, we should continue to re-render and show the best spots (maybe 20-50 idk). So first in USA shows places, then in WA, then in Whatcom County for example as you zoom.
    -Incoporate tools from Search into map (auto select today, but can select other dates)

2. Search tool - search for best stargazing sites near you! Exp: I have an hour and want to find the best dark place with a clear sky to see a meteor shower.
    Search will use multiple variables to deduce sky visibility:
    - Weather (clouds)
        - Important parts cloud coverage/hase (smoke, fog, AQI, pollution)
    - Light pollution
    - Moon level
    - Elevation? (does this effect anything? hahaha)
    - User ratings? (good spot regionally, but maybe campgrounds have tall trees?)
    - Distance
    - Datetime (time of day too.)
    - Determined by these other variables - can search based on average level of stargazing (custom algorithm - determines from Horrible, Bad, Meh, Good, Great, Awesome, Spectacular)

3. Sites - Page displaying information about indiviudal stargazing sites. Here you can see:
    - Pictures
    - Location, Distance from you, Directions
    - Average level of stargazing for dates selected
    - Light pollution
    - (Can select dates to see)
        - expected weather
        - moon level
        - expected constellations/planets visible/stellar objects (meteors, spaceships, spacestations, satelites)
    - Links
    - Additional necessary information (permits, passes, walk in available, book a spot)
    - Location rating (how do we determine this, is it users? whats the starting rating? (we could start with google rating))

4. About
    - About Page, Support/Patreon

V2/Amazing to have:

5. News - Here you can find any starchasers most important related news!
    - Northern Lights
    - Full moons
    - Eclipses
    - Meteor showers
    - Cool night news
    - Exciting astronomical news
    - Ability to get notifications based on certain news.
    - Advertisements/sponsors

6. Constellation Viewing Feature
    - Ability to find stars/constellations with phone - traditional thing where you point phone to sky and it tells you what you're seeing

Additional Pages/Ideas:

7. Saved trips
    - Link to results that have been saved

8. Login/Settings
    - Account Info
    - Suggestions
    - Donate
    - Recieve notifications about star events

Levels of Stargazing:
Will be between certain levels of expected light. These will have various factors such as: Level of light polution. Expected weather. Expected moon level. 

- Bad
- Some
- Good
- Great
- Amazing

Data Necessary:
- Light pollution
    - Light Pollution map person recommended: 
        - https://eogdata.mines.edu/products/vnl/
        - https://dataservices.gfz-potsdam.de/contact/showshort.php?id=escidoc:1541893&contactform
- Campsites
    - National Campsite information: https://www.nps.gov/subjects/developer/api-documentation.htm
- Weather/Clouds/Smoke
    - https://www.weatherapi.com/
    - https://openweathermap.org/api
- Navigation
    - Google maps?: https://developers.google.com/maps/documentation/embed/get-started
- Moon level info
    - Calculate it?: https://www.subsystems.us/uploads/9/8/9/4/98948044/moonphase.pdf
- Cool sky news (where's it coming from?)
- Pictures of campsites

Useful links/Similar projects:
- https://www.lightpollutionmap.info/help.html#FAQ29
- https://darksitefinder.com/map/
- https://djlorenz.github.io/astronomy/lp/
- https://github.com/djlorenz/djlorenz.github.io/blob/master/astronomy