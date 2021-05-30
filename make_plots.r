library(ggplot2)
library(emojifont)

OUTPUT_DIR="plots"
LOG_DIR="logs"

generate_error_plot <- function(name, data) {
    ggplot(data, aes(x = iteration, y = error)) + geom_line(aes(color = method), size = 2) +
        scale_colour_manual(name="Metoda ewolucji różnicowej", values=c("#CC6666", "#9999CC"), breaks=c("classic", "dg"), labels=c("Klasyczna", "Diversity Guided")) +
        labs(x = "Iteracja", y = "Odległość od optimum")
        
    ggsave(paste(OUTPUT_DIR, "/optimum_error/", name, ".pdf", sep=""))
}

generate_value_error_plot <- function(name, data) {
    ggplot(data, aes(x = iteration, y = value_error)) + geom_line(aes(color = method), size = 2) +
        scale_colour_manual(name="Metoda ewolucji różnicowej", values=c("#CC6666", "#9999CC"), breaks=c("classic", "dg"), labels=c("Klasyczna", "Diversity Guided")) +
        labs(x = "Iteracja", y = "Odległość od optymalnego wyniku")

    ggsave(paste(OUTPUT_DIR, "/value_error/", name, ".pdf", sep=""))
}

generate_diversity_plot <- function(name, data) {
    ggplot(data, aes(x = iteration, y = diversity)) + geom_line(aes(color = method), size = 2) +
        scale_colour_manual(name="Metoda ewolucja różnicowej", values=c("#CC6666", "#9999CC"), breaks=c("classic", "dg"), labels=c("Klasyczna", "Diversity Guided")) +
        labs(x = "Iteracja", y = "Różnorodność")

    ggsave(paste(OUTPUT_DIR, "/diversity/", name, ".pdf", sep=""))
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
    data_classic = load_file(test)
    data_dg = load_file(paste(test, ".dg", sep=""))

    data_classic$method = "classic"
    data_dg$method = "dg"

    data <- rbind.data.frame(data_classic, data_dg)

    generate_error_plot(test, data)
    generate_value_error_plot(test, data)
    generate_diversity_plot(test, data)
}
