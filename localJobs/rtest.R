## the argument is the number of random numbers we want to generate
numberofnumbers <- 10
 
## create and initalise a result variable
result <- 0
 
## generate array of random numbers
arrayofnumbers<- 100:130 
 
## loop through the array adding each value to the final result
for(i in 1:length(arrayofnumbers)){
 
    print(paste("Adding ",arrayofnumbers[i]))
 
    ## keep a running total
    result = result + arrayofnumbers[i]
 
}
 
## display on screen the total value of all numbers added up
print(result)
