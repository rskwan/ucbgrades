# import data
# enter the absolute path for where the CSV file is stored in csv.path
csv.path <- "FILL ME OUT"
dept.avgs <- read.csv(csv.path)
dept.avgs <- head(dept.avgs, -1) 
ug.avgs <- dept.avgs$Undergraduate.Average
ud.avgs <- dept.avgs$Upper.Division.Average
ld.avgs <- dept.avgs$Lower.Division.Average
ud.avgs <- ud.avgs[ud.avgs != 0]
ld.avgs <- ld.avgs[ld.avgs != 0]
ug.grades <- dept.avgs$Undergraduate.Grades
ud.grades <- dept.avgs$Upper.Division.Grades
ld.grades <- dept.avgs$Lower.Division.Grades
ud.grades <- ud.grades[ud.grades != 0]
ld.grades <- ld.grades[ld.grades != 0]

# whee histograms
hist(ug.avgs, main="Department Averages of Undergraduate Courses",
     xlab="Department Average")
hist(ud.avgs, main="Department Averages of Upper Division Courses",
     xlab="Department Average")
hist(ld.avgs, main="Department Averages of Lower Division Courses",
     xlab="Department Average")

# plot densities
plot(c(2.5, 4.0), c(0.0, 2.0), type="n",
     main="Densities for Department Averages",
     xlab="Department Average", ylab="Density")
lines(density(ug.avgs), col="blue")
lines(density(ud.avgs), col="green")
lines(density(ld.avgs), col="red")
legend(2.6, 1.8, c("Undergrad", "Lower Div", "Upper Div"),
       lty=c(1, 1), lwd=c(1, 1),
       col=c("blue", "red", "green"))