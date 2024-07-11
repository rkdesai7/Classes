---
title: "STA 141 - Fundamentals of Statistical Data Science - Final project"
params:
  term: Winter 2023
output: 
   html_document: default
   pdf_document: default
editor_options: 
  markdown: 
    wrap: 72
---

# Working with the New York Times COVID-19 Data

As we have seen in class, COVID-19 data collected by the *New York
Times* are available in a repository on Github. In this final project we
will work with these data to reproduce some of the elements of the
*Times*'s reporting on COVID-19.

```{r include = FALSE, echo = TRUE}
diff.eg <- quote(diff(c(1, 3, 6, 10)))
```

# Exercises

1.  The file `us.csv` contains aggregated data for the entire U.S. In
    this file, the `cases` and `deaths` columns represent *cumulative*
    cases and deaths due to covid. The `diff()` function can be used to
    compute the differences between each consecutive element of a
    vector, so it could be used to compute the daily numbers of cases
    and deaths. However, `diff()` returns a vector of length one less
    than the length of the original vector (e.g.,
    `r noquote(deparse(diff.eg))` returns `r eval(diff.eg)`) and this
    can make it somewhat inconvenient to use when transforming columns
    of data frames.

    An alternative is to us the more general `filter()` function with an
    appropriate choice of the `filter` and `sides` arguments. Thus
    function can also be used to computing running averages and similar
    quantities.

    a.  Read the file `us.csv` into R as the data frame `us` and do the
        following:

        -   Transform the `date` column into a column of class `Date`.
        -   Use `filter()` to add a column named `new_cases` containing
            the number of new cases reported on each date. The first
            value in this column will be `NA`.
        -   Use `filter()` to add a column named `new_deaths` containing
            the number of new deaths reported on each date. The first
            value in this column will be `NA`.
        -   Use `filter()` to add a column named `avg_new_cases` where
            each element represents the mean number of new cases for the
            previous 7 days (inclusive of the current day). The first 7
            values in this column will be `NA`.
        -   Use `filter()` to add a column named `avg_new_deaths` where
            each element represents the mean number of new deaths for
            the previous 7 days (inclusive of the current day). The
            first 7 values in this column will be `NA`.

        Note that the `filter()` function used here is `stats::filter()`
        from the `stats` package, which is loaded by default in R. (The
        `dplyr` package has a completely different `filter()` function
        which plays an important role in the "tidyverse". If you have
        problems using `filter()`, you should make sure that you do NOT
        have the `dplyr` package loaded. If you do, then you will need
        to explicitly type out `stats::filter()` to get the `stats`
        version.)

```{r}
#Read in file
us <- read.csv("C:/Users/riyak/OneDrive/Documents/Undergrad/Classes/STA/STA141A/FinalProject/us.csv")

#Transform date column into a column of class date
us$date <- as.Date(us$date)

#Addings new_cases column containing number of new cases reported on each date
new_cases <- filter(us$cases, c(1, -1), sides = 1)
us <- cbind(us, new_cases)

#Adding new_deaths column containing number of new deaths reported on each date
new_deaths <- filter(us$deaths, c(1, -1), sides = 1)
us <- cbind(us, new_deaths)

#Adding avg_new_cases column representing the mean number of new cases for the previous 7 days (inclusive of the current day)
avg_new_cases <- filter(us$new_cases, rep(1/7, 7), sides = 1)
us <- cbind(us, avg_new_cases)

#Adding avg_new_deaths column representing the mean number of new deaths for the previous 7 days
avg_new_deaths <- filter(us$new_deaths, rep(1/7, 7), sides = 1)
us <- cbind(us, avg_new_deaths)
```

    b.  Create a plot of daily cases similar to the one found at the top
        of [this
        page](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html).
        Plot only data beginning from 2020-03-01. (Note that this plot
        and a similar plot for deaths appear again about 1/3 of the way
        down the page.)

        Try to do this using the formula method of the `plot()` function
        with the optional arguments `type = "h"`, `col = "gray"`, and
        `data = us` and using the `subset` argument to plot only the
        data for dates 2020-03-01 and after. (You may also wish to
        experiment with the optional argument `lwd`.)

        Then use the formula interface to the `lines()` function to add
        the curve showing the seven-day running average. (Again, you may
        wish to experiment with the optional argument `lwd`.)

```{r}

#Create new dataframe with data after 2020-3-1
df <- subset(us, date > as.Date("2020-03-01"))
#Set font
par(cex.axis = .52)
#Plot new cases
plot(x = df$date, y = df$new_cases, type = 'h', col = 'gray', xlab = "Year", ylab = "Cases", lwd = 10, yaxp = c(0, 1500000, 5), main = "New COVID Cases in America Starting from March 1, 2020")
#Add 7 day average
lines(x = df$date, y = df$avg_new_cases, type = 'h', col = 'red')
#Add legend
legend(x = "topright", legend = c("Daily New Cases", "7 Day Average"), fill = c("gray", "red"))
```

    c.  Repeat part (b) for deaths.

```{r}

df <- subset(df, df$new_deaths >= 0)

par(cex.axis = .52)
plot(x = df$date, y = df$new_deaths, type = 'h', col = 'gray', xlab = "Year", ylab = "Deaths", lwd = 7, yaxp = c(0, 15000, 5), main = "COVID Deaths in America Starting from March 1, 2020")
lines(x = df$date, y = df$avg_new_deaths, type = 'h', col = 'red')

legend(x = "topleft", legend = c("Daily Deaths", "7 Day Average"), fill = c("gray", "red"))
```

2.  The file `us-states.csv` contains county-level data for the U.S.

    a.  Read `us-states.csv` into R as the data frame `us_states` and
        transform the date column into a column of class `Date`.

```{r}
#read in file
us_states <- read.csv("C:/Users/riyak/OneDrive/Documents/Undergrad/Classes/STA/STA141A/FinalProject/us-states.csv")

#Transform date column into a column of class date
us_states$date <- as.Date(us_states$date)
```

    b.  Use `subset()` to extract the data for the state of California
        and save it as a data frame named `California`. Be sure that the
        rows are correctly ordered by date, and then repeat parts 1b and
        1c of this assignment for California, i.e., plot the number of
        daily new cases and deaths, along with their 7-day running
        averages.
        

```{r}
#Extract and check California specific data
California <- subset(us_states, state == "California")

#New Cases
#Add daily new cases row using filter
new_cases <- filter(California$cases, c(1, -1), sides = 1)
California <- cbind(California, new_cases)
#Add 7 day new case average row using filter
avg_new_cases <- filter(California$new_cases, rep(1/7, 7), sides = 1)
California <- cbind(California, avg_new_cases)

#Plot daily new cases with 7-day running average
#Create new dataframe with data after 2020-3-1
df <- subset(California, date > as.Date("2020-03-01"))
#Set font
par(cex.axis = .52)
#Plot new cases
plot(x = df$date, y = df$new_cases, type = 'h', col = 'gray', xlab = "Year", ylab = "Cases", lwd = 8, yaxp = c(0, 230000, 5), main = "New COVID Cases in California Starting from March 1, 2020")
#Add 7 day average
lines(x = df$date, y = df$avg_new_cases, type = 'h', col = 'red')
#Add legend
legend(x = "topright", legend = c("Daily New Cases", "7 Day Average"), fill = c("gray", "red"))
```

```{r}
#New Deaths
#Adding new_deaths column containing number of new deaths reported on each date
new_deaths <- filter(California$deaths, c(1, -1), sides = 1)
California <- cbind(California, new_deaths)

#Adding avg_new_deaths column representing the mean number of new deaths for the previous 7 days
avg_new_deaths <- filter(California$new_deaths, rep(1/7, 7), sides = 1)
California <- cbind(California, avg_new_deaths)

df <- subset(California, date > as.Date("2020-03-01"))
df <- subset(df, df$new_deaths >= 0)

#plot daily deaths with 7-day running average
par(cex.axis = .52)
plot(x = df$date, y = df$new_deaths, type = 'h', col = 'gray', xlab = "Year", ylab = "Deaths", lwd = 9, yaxp = c(0, 2500, 5), main = "COVID Deaths in California Starting from March 1, 2020")
lines(x = df$date, y = df$avg_new_deaths, type = 'h', col = 'red')

legend(x = "topleft", legend = c("Daily Deaths", "7 Day Average"), fill = c("gray", "red"))
```

3.  The file `us-counties.csv` contains county-level data for the U.S.

    a.  Read `us-counties.csv` into R as the data frame `us_counties`
        and transform the date column into a column of class `Date`.

```{r}
#Read in file
us_counties <- read.csv("C:/Users/riyak/OneDrive/Documents/Undergrad/Classes/STA/STA141A/FinalProject/us-counties.csv")

#Transform date coumn into class Date
us_counties$date <- as.Date(us_counties$date)
```

    b.  Use `subset()` to extract the data for Yolo County, California,
        and save it as a data frame named `Yolo`. Be sure that the rows
        are correctly ordered by date, and then repeat part 1b this
        assignment for Yolo County, i.e., plot the number of daily new
        cases along with their 7-day running average.
        

```{r}
#Subset for Yolo County
Yolo <- subset(us_counties, county == "Yolo")

#Calculate and add daily new case column to Yolo dataframe
new_cases <- filter(Yolo$cases, c(1, -1), sides = 1)
Yolo <- cbind(Yolo, new_cases)

#Calculate and add 7-day running average
avg_new_cases <- filter(Yolo$new_cases, rep(1/7, 7), sides = 1)
Yolo <- cbind(Yolo, avg_new_cases)
```

```{r}
#Plot
#Set font
par(cex.axis = .52)
#Plot new cases
plot(x = Yolo$date, y = Yolo$new_cases, type = 'h', col = 'gray', xlab = "Year", ylab = "Cases", lwd = 8.5, yaxp = c(0, 2000, 5), main = "New COVID Cases in Yolo County")
#Add 7 day average
lines(x = Yolo$date, y = Yolo$avg_new_cases, type = 'h', col = 'red')
#Add legend
legend(x = "topleft", legend = c("Daily New Cases", "7 Day Average"), fill = c("gray", "red"))
```

        Q: What do you notice when comparing the plot of daily new cases
        in Yolo county to the analogous plot for the state of California
        as a whole? What might explain what you are seeing?
        
    When comparing the two plots, it is apparent that Yolo County is lacking data for much of 2022 and the beginning of 2023. 

4.  Bonus
