library(ggplot2)

OUTPUT_DIR="plots"
LOG_DIR="logs"

generate_error_plot <- function(name, data) {
    ggplot(data, aes(x = iteration)) + geom_line(aes(y = error), color = "darkred") + geom_line(aes(y = error_dg), color = "steelblue") +
        scale_colour_discrete(name = "Metoda ewolucji", breaks = c("error", "error_dg"), labels = c("Klasyczna ewolucja róznicowa", "Różnicowa z Heurystyką Diversity Guided"))
    ggsave(paste(OUTPUT_DIR, "/optimum_error/", name, ".pdf", sep=""))
}

generate_value_error_plot <- function(name, data) {
    ggplot(data, aes(x = iteration)) + geom_line(aes(y = value_error), color = "darkred") + geom_line(aes(y = value_error_dg), color = "steelblue") +
        scale_colour_discrete(name = "Metoda ewolucji", breaks = c("value_error", "value_error_dg"), labels = c("Klasyczna ewolucja róznicowa", "Różnicowa z Heurystyką Diversity Guided"))
    ggsave(paste(OUTPUT_DIR, "/value_error/", name, ".pdf", sep=""))
}

load_file <- function(name) {
    data_set = read.csv(paste(LOG_DIR, "/", name, ".csv", sep=""))
}

tests = c(
    "one.parabola",
    "one.transposed_parabola",
    "two_local.single_dimension",
    "two_local.moutains",
    "two_global",
    "multiple_local",
    "multiple_global"
)

for (test in tests) {
    data_std = load_file(test)
    data_dg = load_file(paste(test, ".dg", sep=""))

    data = data.frame(iteration = data_std$iteration,
                      error = data_std$error,
                      error_dg = data_dg$error,
                      value_error = data_std$value_error,
                      value_error_dg = data_dg$value_error
    )

    generate_error_plot(test, data)
    generate_value_error_plot(test, data)
}
