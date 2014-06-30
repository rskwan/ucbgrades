# import data
# enter the absolute path for where the CSV file is stored in csv.path
csv.path <- "~"
dept.avgs <- read.csv(csv.path)
ug <- dept.avgs$Undergraduate.Average
ud <- dept.avgs$Upper.Division.Average
ld <- dept.avgs$Lower.Division.Average
ud <- ud[ud != 0]
ld <- ld[ld != 0]

# whee histograms
hist(ug, main="Department Averages of Undergraduate Courses",
     xlab="Department Average")
hist(ud, main="Department Averages of Upper Division Courses",
     xlab="Department Average")
hist(ld, main="Department Averages of Lower Division Courses",
     xlab="Department Average")

# plot densities
plot(c(2.5, 4.0), c(0.0, 2.0), type="n",
     main="Densities for Department Averages",
     xlab="Department Average", ylab="Density")
lines(density(ug), col="blue")
lines(density(ud), col="green")
lines(density(ld), col="red")
legend(2.6, 1.8, c("Undergrad", "Lower Div", "Upper Div"),
       lty=c(1, 1), lwd=c(1, 1),
       col=c("blue", "red", "green"))