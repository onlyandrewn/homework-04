#!/usr/bin/env python
# coding: utf-8

# # WeatherAPI (Weather)
# 
# Answer the following questions using [WeatherAPI](http://www.weatherapi.com/). I've added three cells for most questions but you're free to use more or less! Hold `Shift` and hit `Enter` to run a cell, and use the `+` on the top left to add a new cell to a notebook.
# 
# Be sure to take advantage of both the documentation and the API Explorer!
# 
# ## 0) Import any libraries you might need
# 
# - *Tip: We're going to be downloading things from the internet, so we probably need `requests`.*
# - *Tip: Remember you only need to import requests once!*

# In[1]:


import requests


# ## 1) Make a request to the Weather API for where you were born (or lived, or want to visit!).
# 
# - *Tip: The URL we used in class was for a place near San Francisco. What was the format of the endpoint that made this happen?*
# - *Tip: Save the URL as a separate variable, and be sure to not have `[` and `]` inside.*
# - *Tip: How is north vs. south and east vs. west latitude/longitude represented? Is it the normal North/South/East/West?*
# - *Tip: You know it's JSON, but Python doesn't! Make sure you aren't trying to deal with plain text.* 
# - *Tip: Once you've imported the JSON into a variable, check the timezone's name to make sure it seems like it got the right part of the world!*

# In[2]:


location_visit = "Paris"

url = "http://api.weatherapi.com/v1/current.json?key=370edf33fe024c448d8171449221306&q=Paris"
response = requests.get(url)
data = response.json()
print(data)


# ## 2) What's the current wind speed? How much warmer does it feel than it actually is?
# 
# - *Tip: You can do this by browsing through the dictionaries, but it might be easier to read the documentation*
# - *Tip: For the second half: it **is** one temperature, and it **feels** a different temperature. Calculate the difference.*

# In[3]:


location = data["location"]["name"]
wind_speed = data["current"]["wind_mph"]

temp_c = data["current"]["temp_c"]
feelslike_c = data["current"]["feelslike_c"]
temp_diff = feelslike_c - temp_c

print(f"The current wind speed in {location} is {wind_speed} mph.")

if feelslike_c > temp_c:
    print(f"It is {abs(temp_diff):.1f} degrees warmer than the actual temperature in {location}.")
else:
    print(f"It is {abs(temp_diff):.1f} degrees colder than the actual temperature in {location}.")


# ## 3) What is the API endpoint for moon-related information? For the place you decided on above, how much of the moon will be visible tomorrow?
# 
# - *Tip: Check the documentation!*
# - *Tip: If you aren't sure what something means, ask in Slack*

# In[4]:


url_moon = "http://api.weatherapi.com/v1/astronomy.json?key=370edf33fe024c448d8171449221306&q=Paris&dt=2022-06-17"
response = requests.get(url_moon)
data_moon = response.json()

moon_phase = (data_moon["astronomy"]["astro"]["moon_phase"]).lower()
print(f"There will be a {moon_phase} visible tomorrow.")


# ## 4) What's the difference between the high and low temperatures for today?
# 
# - *Tip: When you requested moon data, you probably overwrote your variables! If so, you'll need to make a new request.*

# In[5]:


import math

url_today = "http://api.weatherapi.com/v1/forecast.json?key=370edf33fe024c448d8171449221306&q=Paris&days=1"
response_today = requests.get(url_today)
data_today = response_today.json()

temp_high_today = data_today["forecast"]["forecastday"][0]["day"]["maxtemp_c"]
temp_low_today = data_today["forecast"]["forecastday"][0]["day"]["mintemp_c"]
temp_diff_today = math.floor(temp_high_today - temp_low_today)

print(f"The difference between the high and low temperatures is roughly {temp_diff_today} degrees.")


# ## 4.5) How can you avoid the "oh no I don't have the data any more because I made another request" problem in the future?
# 
# What variable(s) do you have to rename, and what would you rename them?

# In[6]:


# You may need to rename the variables for url, response and data
# You can append _description to each of the three variables
# i.e. url_variable_name, response_variable_name, data_variable_name


# ## 5) Go through the daily forecasts, printing out the next three days' worth of predictions.
# 
# I'd like to know the **high temperature** for each day, and whether it's **hot, warm, or cold** (based on what temperatures you think are hot, warm or cold).
# 
# - *Tip: You'll need to use an `if` statement to say whether it is hot, warm or cold.*

# In[7]:


url_three_days = "http://api.weatherapi.com/v1/forecast.json?key=370edf33fe024c448d8171449221306&q=Paris&days=3"
response_three_days = requests.get(url_three_days)
data_three_days = response_three_days.json()

high_temps = [temp["day"]["maxtemp_c"] for temp in data_three_days["forecast"]["forecastday"]]

for temp in high_temps:
    if temp >= 24:
        print(temp, "degrees C is hot.")
    elif temp >= 12:
        print(temp, "degrees C is warm.")
    elif temp < 0:
        print(temp, "degrees C is cold.")


# ## 5b) The question above used to be an entire week, but not any more. Try to re-use the code above to print out seven days.
# 
# What happens? Can you figure out why it doesn't work?
# 
# * *Tip: it has to do with the reason you're using an API key - maybe take a look at the "Air Quality Data" introduction for a hint? If you can't figure it out right now, no worries.*

# In[8]:


# It only provides data for three of the seven days requested.

# Free tier allows for 3 day city and town weather. Daily and Hourly.
# Starter tier allows for 7 day city and town weather. Daily and Hourly.

url_seven_days = "http://api.weatherapi.com/v1/forecast.json?key=370edf33fe024c448d8171449221306&q=Paris&days=7"
response_seven_days = requests.get(url_seven_days)
data_seven_days = response_seven_days.json()

high_temps = [temp["day"]["maxtemp_c"] for temp in data_seven_days["forecast"]["forecastday"]]

for temp in high_temps:
    if temp >= 24:
        print(temp, "degrees C is hot.")
    elif temp >= 12:
        print(temp, "degrees C is warm.")
    elif temp < 0:
        print(temp, "degrees C is cold.")


# ## 6) What will be the hottest day in the next three days? What is the high temperature on that day?

# In[9]:


temps = {}

for temp in data_three_days["forecast"]["forecastday"]:
    temps[temp["date"]] = temp["day"]["maxtemp_c"]
    
print(f"The hottest day in the next three days will be {max(temps)}. The temperature will be {max(temps.values()):.0f} degrees C.")
# print(temps, max(temps.values()))


# ## 7) What's the weather looking like for the next 24+ hours in Miami, Florida?
# 
# I'd like to know the temperature for every hour, and if it's going to have cloud cover of more than 50% say "{temperature} and cloudy" instead of just the temperature. 
# 
# - *Tip: You'll only need one day of forecast*

# In[10]:


url_miami = "http://api.weatherapi.com/v1/forecast.json?key=370edf33fe024c448d8171449221306&q=Miami&days=1"
response_miami = requests.get(url_miami)
data_miami = response_miami.json()

for hour in data_miami["forecast"]["forecastday"][0]["hour"]:    
    time = hour["time"]
    temp = hour["temp_c"]
    cloud = hour["cloud"]

    if cloud > 50:
        print(f"The temperature is {temp:.0f} degrees C and cloudy at {time}")
    else:
        print(f"The temperature is {temp:.0f} degrees C at {time}.")


# ## 8) For the next 24-ish hours in Miami, what percent of the time is the temperature above 85 degrees?
# 
# - *Tip: You might want to read up on [looping patterns](http://jonathansoma.com/lede/foundations-2017/classes/data%20structures/looping-patterns/)*

# In[11]:


time_in_hours = 24
hours_above_85 = 0

for hour in data_miami["forecast"]["forecastday"][0]["hour"]:    
    temp = hour["temp_f"]

    if temp > 85:
        hours_above_85 = hours_above_85 + 1
    
pct_time = (hours_above_85 / time_in_hours) * 100
print(f"The temperature is above 85 degrees F roughly {pct_time:.0f}% of the time.")


# ## 9) How much will it cost if you need to use 1,500,000 API calls?
# 
# You are only allowed 1,000,000 API calls each month. If you were really bad at this homework or made some awful loops, WeatherAPI might shut down your free access. 
# 
# * *Tip: this involves looking somewhere that isn't the normal documentation.*

# In[12]:


# https://www.weatherapi.com/pricing.aspx
# It would cost $4 to make 2 million API calls.


# ## 10) You're too poor to spend more money! What else could you do instead of give them money?
# 
# * *Tip: I'm not endorsing being sneaky, but newsrooms and students are both generally poverty-stricken.*

# In[13]:


# - Wait until the following month to make an additional one million calls in the free tier.
# - Make an additional account for the remaining 500,000 API calls.

