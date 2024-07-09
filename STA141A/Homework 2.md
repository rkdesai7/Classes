---
title: "STA 141A Fundamentals of Statistical Data Science - Homework 2"
params:
  term: Winter 2023
  duedate: '2023-03-08'
  name: Riya Desai
  email: rykdesai@ucdavis.edu
  total_points: XX
  grade: NA
output:
  html_document:
    df_print: paged
  pdf_document: default
editor_options: 
  markdown: 
    wrap: 72
---

```{r as_ordinal, include = TRUE, echo = FALSE}
ord_suffix <-
    function(x) switch(as.character(x), "1"="st", "2"="nd", "3"="rd", "th")
as_ordinal <- function(x) paste0(x, ord_suffix(x))
```

# Exercises

1.After executing the command

```{r eval=FALSE, include=TRUE}
z <- rep(c(rep(x, each = a), rep(y, each = b)), times = t)
```

which element of x or y is contained in the kth element of z?. Suppose
that x and y are vectors in R of lengths m and n, respectively. Write a
function, `rep_tracker(k, m, n, a, b, t)`, which computes the answer for
any positive integers k, m, n, a, b, and t. Your function should return
a list whose first element is named "src_vector" and gives the name of
the vector ("x" or "y") and whose second element is named "src_index"
and gives the integer indicating the original location of the value in
either "x" or "y". For example, if the kth element of z was originally
the 5 element of y, then your function should return
`list(src_vector = "y", src_index = 5)`.

Your may not use the `rep()` function in your solution. Your function
should emulate the way that a human might solve this problem using
integer arithmetic.

# Solution

```{r rep_tracker, echo = TRUE}
rep_tracker <- function(k, m, n, a, b, t) {
  
    #make sure k is in range
    if (k > (t * (m * a + n * b))) warning("First argument is out of range")
    #Get length of one repetition of c(rep(x, each = a), rep(y, each = b))
    t1 = m*a + n*b
    #k mod repetition length to find index value in first repetition
    index <- k %% t1

    #Check if index at end of first repetition: is last element of vector y
    if (k %% t1 == 0){
      v = 'y'
      i = b
    }
    #check if index is in x
    else if (index <= m*a){
      v = 'x'
      i = ceiling(index/a) #find specific index in x
    } else { 
      #index in y
      v = 'y'
      
      #find specific index in y
      index1 = index - m*a
      i = ceiling(index1/b) 
    }
    #print output
    list(src_vector = v, src_index = i)
}
```

2.  Consider the report: [A PHASE 1/2/3, PLACEBO-CONTROLLED, RANDOMIZED,
    OBSERVER-BLIND, DOSE-FINDING STUDY TO EVALUATE THE SAFETY,
    TOLERABILITY, IMMUNOGENICITY, AND EFFICACY OF SARS-COV-2 RNA VACCINE
    CANDIDATES AGAINST COVID-19 IN HEALTHY INDIVIDUALS (pages 99-101)].
    Let $\theta$ be the probability that a subject who fell ill with
    Covid-19 is from the treatment group and $1-\theta$ the probability
    that the subject is from the control group. Assuming that 94
    subjects fell ill to Covid-19 (with a sample efficacy above 90%) and
    at most 8 of those 94 subjects were vaccinated. Write a report
    (Introduction, Methods, Results and Conclusions) assuming:

### Introduction:

We are analyzing probability data from the *A PHASE 1/2/3,
PLACEBO-CONTROLLED, RANDOMIZED, OBSERVER-BLIND, DOSE-FINDING STUDY TO
EVALUATE THE SAFETY, TOLERABILITY, IMMUNOGENICITY, AND EFFICACY OF
SARS-COV-2 RNA VACCINE CANDIDATES AGAINST COVID-19 IN HEALTHY
INDIVIDUALS (pages 99-101)* report. In this study, the control group is
the group without the vaccine, and the treatment group is the one with
the vaccine. Of the 94 subjects that fell ill to COVID-19, at most 8 of
the 94 subjects were vaccinated, and there is a sample efficacy above
90%. We let $\theta$ be the probability that a subject who fell ill with
COVID-19 is from the treatment group, and $1-\theta$ be the probability
that the subject is from the control group. In this report, we examine
the distribution and probabilities of COVID-19 rates within the group,
as well as vaccination rates using various statistical methods.

### Methods:

First, we plot the prior, likelihood, and posterior functions of
$\theta$ using the Beta prior $p(\theta) = Beta(a = 0.5, b = 0.5)$ . For
the posterior function, we take into account the parameters that at most
8 of the 94 subjects were vaccinated, using the new arguments
$a=a_{0}+m_{v}$ and $b=b_{0}+m_{c}$ where $m_{v}=8$ and $m_{c}=94-8$.
This is done using the following code (Pt. A):

```{r echo = T, results = "hide", fig.keep = 'none'}
# priors
a = 0.5
b = 0.5

#prior function
theta = seq(0, 1, len=1000)
plot(theta, dbeta(theta, a, b), type="l", xlab=expression(theta),
     ylab=expression(p(theta)), ylim=c(0,15), lty=1, col=3, main = 'Likelhiood, Prior, and Posterior Distributions')


t = 8  # vaccinated subjects in sample 
n = 94 # subjects -> ill with COVID-19

#likelihood function
lines(theta, dbeta(theta, t+1, n-t+1), type = "l", col = 2, lty = 2)

# posterior function
a = 0.5 + t 
b = 0.5 + n - t
lines(theta, dbeta(theta, a, b), type = "l", col = 4, lty = 2)
legend(0.6, 15, paste(c("Prior: Beta(0.5, 0.5)", "Likelihood",
                        "Posterior: Beta(8.5, 86.5)")),
       lty = c(1, 2, 2), col = c(3, 2, 4), cex = 0.8)
```

We then calculate the posterior probability of having a value of
$\theta>0.4118$ to test Pfizer/Biontech's statement that the posterior
probability of an efficacy below 30% is smaller than 2.5% as an interim
success criterion. So we are testing their proposed beta prior of
$beta(0.700102, 1)$. The following code is used (Pt. B):

```{r echo = T, results = "hide"}
pbeta(0.4118,a,b,lower.tail = FALSE)*100
```

Next, we calculate 95% credible and confidence intervals for $\theta$.
For the credible interval, we depend on the assumed prior for $\theta$.
The following code is used (Pt. C):

```{r echo = T, results = "hide"}
#variables
alpha = 1-0.95
t = 8
n = 94
a = .5 + t
b = .5 + n - t

#confidence interval
L.confidence = qbeta(alpha/2, t+1, n-t+1)
U.confidence = qbeta(1-alpha/2, t+1, n-t+1)

#credible interval
L.credible = qbeta(alpha/2, a, b)
U.credible = qbeta(1-alpha/2, a, b)

```

Finally, we plot the posterior empirical predictive density. As a final
validation metric, we calculate the estimated amount of subjects that
were vaccinated if a new sample of 94 subjects with Covid-19 are taken.
This is done through the following code (Pt. D):

```{r echo = T, results = "hide", fig.keep = 'none', message=FALSE, warning=FALSE}
t = 8 #COVID and vaccinated  
n = 94 #sample size with COVID

a = 0.5 + t #a prior
b = 0.5 + n - t #b prior

#import necessary functions
library(LearnBayes)
library(extraDistr)

m = 94
y_m = rbbinom(10000, m, a, b)
plot(table(y_m)/10000, xlab = '', ylab = 'Posterior Predictive', col = 2, main = 'Posterior Empirical Predictive Density')

mean_predictive = m*a/(a + b)
mean_predictive

```

### Results:

A.  

```{r echo=FALSE}
# priors
a = 0.5
b = 0.5

#prior function
theta = seq(0, 1, len=1000)
plot(theta, dbeta(theta, a, b), type="l", xlab=expression(theta),
     ylab=expression(p(theta)), ylim=c(0,15), lty=1, col=3, main = 'Likelihood, Prior, and Posterior Distributions')


t = 8  # vaccinated subjects in sample 
n = 94 # subjects -> ill with COVID-19

#likelihood function
lines(theta, dbeta(theta, t+1, n-t+1), type = "l", col = 2, lty = 2)

# posterior function
a = 0.5 + t 
b = 0.5 + n - t
lines(theta, dbeta(theta, a, b), type = "l", col = 4, lty = 2)
legend(0.6, 15, paste(c("Prior: Beta(0.5, 0.5)", "Likelihood",
                        "Posterior: Beta(8.5, 86.5)")),
       lty = c(1, 2, 2), col = c(3, 2, 4), cex = 0.8)

```

B. The posterior probability of having a value of $\theta>0.4118$ is
*5.826008e-11*.

```{r, echo = FALSE}
pbeta(0.4118,a,b,lower.tail = FALSE)*100
```

C. The 95% confidence interval is *(0.044, .159)*. The 95% credible
interval is *(0.041, .154)*.

D. The estimated amount of subjects that are vaccinated in a sample of
94 subjects with COVID-19 is 8.410526.

```{r, echo = FALSE, message=FALSE, warning=FALSE}
t = 8  
n = 94 

a = 0.5 + t 
b = 0.5 + n - t

library(LearnBayes)
library(extraDistr)
m = 94
y_m = rbbinom(10000, m, a, b)
plot(table(y_m)/10000, xlab = '', ylab = 'Posterior Predictive', col = 2, main = 'Posterior Empirical Predictive Density')
```

### Conclusion:

As seen in result D, using the prior distribution of $beta(.5, .5)$ is
an adequate model to predict the estimated amount of subjects that are
vaccinated in a sample of 94 subjects as it predicts an amount of 8.41,
which is extremely close to the given amount of having at most 8 of the
subjects vaccinated. Additionally, the posterior function from result A
shows that $E(\theta)$ reduces to approximately .08 when given that at
most 8 out of 94 COVID-19 infected patients are vaccinated. From result
B, we also see that it is unlikely that the probability of being ill
with COVID-19 and being vaccinated is greater than .4118, as the
probability is extremely close to 0. Additionally, result C tells us
that we can be 95% confident that $E(\theta)$ lies between .044 and
.159, meaning the probability of getting COVID-19 while being
vaccinated, $1-E(\theta)$, is fairly low. These results provide evidence
against the proposition that $E(\theta)$ is .4118 considering the
Pfizer/Biontech data that 94 subjects were infected with COVID-19 and at
most 8 of those subjects were vaccinated. It also suggests that the
Pfizer/Biontech vaccine is effective, but further testing is needed.

<!-- -->
