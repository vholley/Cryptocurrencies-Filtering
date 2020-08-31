#!/usr/bin/env python
# coding: utf-8
# Bitcoin and Cryptocurrencies: Full dataset, filtering, and reproducibility


# Import pandas
import pandas as pd

# Import matplotlib and set aesthetics for plotting later.
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Read datasets/coinmarketcap_06122017.csv into pandas
dec6 = pd.read_csv('datasets/coinmarketcap_06122017.csv')

# Select the 'id' and the 'market_cap_usd' columns
market_cap_raw = dec6[['id', 'market_cap_usd']]

# Count the number of values
print(market_cap_raw.count())


# ## Discard the cryptocurrencies without a market capitalization

# Filter out rows without a market capitalization
cap = market_cap_raw.query('market_cap_usd.notnull()')

# Count the number of values again
print(cap.count())


# ## How big is Bitcoin compared with the rest of the cryptocurrencies?

# Declare the title and ylabel for later use in the plots
TOP_CAP_TITLE = 'Top 10 market capitalization'
TOP_CAP_YLABEL = '% of total cap'

# Select the first 10 rows and set the index
cap10 = cap[:10].set_index('id')
print(cap10)

# Calculate market_cap_perc
cap10 = cap10.assign(market_cap_perc=lambda x:
                     (x.market_cap_usd / cap.market_cap_usd.sum() * 100))
print(cap10)

# Plot the barplot with the title defined above
ax = cap10.plot.bar(title=TOP_CAP_TITLE)

# Annotate the y axis with the label defined above
ax.set_ylabel(TOP_CAP_YLABEL)


# ## Make the plot easier to read and more informative

# Colors for the bar plot
COLORS = ['orange', 'green', 'orange', 'cyan', 'cyan', 'blue', 'silver',
          'orange', 'red', 'green']

# Plot market_cap_usd as before but adding the colors and scaling the y-axis
ax = cap10.plot.bar(title=TOP_CAP_TITLE, color=COLORS)
ax.set_yscale('log')

# Annotating the y axis with 'USD'
ax.set_ylabel('USD')

# Removing the xlabel as it is not very informative
ax.set_xlabel('')


# ## Volatility in cryptocurrencies

# Select the id, percent_change_24h and percent_change_7d columns
volatility = dec6[['id', 'percent_change_24h', 'percent_change_7d']]

# Set the index to 'id' and dropping all NaN rows
volatility = volatility.set_index('id').dropna()

# Sort the DataFrame by percent_change_24h in ascending order
volatility = volatility.sort_values(by='percent_change_24h')

# Check the first few rows
print(volatility.head())


# ## Plot the top 10 biggest gainers and top 10 losers in market capitalization

# Define a function with 2 parameters, the series to plot and the title
def top10_subplot(volatility_series, title):

    # Make the subplot and the figure for two side by side plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 6))

    # Plot with pandas the barchart for the top 10 losers
    ax = volatility_series[:10].plot.bar(ax=axes[0], color='darkred')

    # Set the figure's main title to the text passed as parameter
    fig.suptitle(title)

    # Set the ylabel to '% change'
    ax.set_ylabel('% change')
    # ... YOUR CODE FOR TASK 7 ...

    # Same as above, but for the top 10 winners
    ax = volatility_series[-10:].plot.bar(ax=axes[1], color='darkblue')

    # Return fig and ax
    return fig, ax


DTITLE = "24 hours top losers and winners"

# Call the function above with the 24 hours period series and title DTITLE
fig, ax = top10_subplot(volatility.percent_change_24h, DTITLE)


# ## Check the weekly Series

# Sort in ascending order
volatility7d = volatility.sort_values(by='percent_change_7d')

WTITLE = "Weekly top losers and winners"

# Call the top10_subplot function
fig, ax = top10_subplot(volatility7d.percent_change_7d, WTITLE)


# ## Classify the dataset based on Investopedia's capitalization

# Select everything bigger than 10 billion
largecaps = cap.query('market_cap_usd >= 10000000000')

# Print out largecaps
print(largecaps)



# ## Merge categories
# Most cryptocurrencies do not fit within Investopedia's definition

# Define a function for counting different marketcaps from the "cap" Dataframe
def capcount(query_string):
    return cap.query(query_string).count().id

# Labels for the plot
LABELS = ["big", "micro", "nano"]

# Use capcount to count the biggish cryptos
big = capcount('market_cap_usd >= 300000000')

# Same as above for micro
micro = capcount('market_cap_usd >= 50000000 and market_cap_usd < 300000000')

# Same as above for nano
nano = capcount('market_cap_usd < 50000000')

# Make a list with the 3 counts
values = [big, micro, nano]

# Plot them with matplotlib
plt.bar(x=LABELS, height=values)
