# ══════════════════════════════════════════════════════════════════════════════
# ESS Loader Utility (R)
# ══════════════════════════════════════════════════════════════════════════════
# Reusable functions for loading, labelling, and merging ESS data in R.
# Mirrors load_ess.py for the R workflow.
#
# Usage:
#   source("scripts/load_ess.R")
#   df <- load_ess_wave(1, sample_only = TRUE)
#   df <- attach_rti_scores(df)
# ══════════════════════════════════════════════════════════════════════════════

library(haven)
library(dplyr)
library(readr)

# ── Path configuration ─────────────────────────────────────────────────────────

ROOT <- normalizePath(file.path(dirname(rstudioapi::getActiveDocumentContext()$path), ".."),
                      mustWork = FALSE)
# Fallback if not in RStudio:
if (!dir.exists(ROOT)) ROOT <- getwd()

ESS_WAVE_PATHS <- list(
  `1` = "data/raw/gugushvili_2025/ESS1e06_7 (1)/ESS1e06_7.dta",
  `2` = "data/raw/gugushvili_2025/ESS2e03_6 (1)/ESS2e03_6.dta",
  `3` = "data/raw/gugushvili_2025/ESS3e03_7 (1)/ESS3e03_7.dta",
  `4` = "data/raw/gugushvili_2025/ESS4e04_6/ESS4e04_6.dta",
  `5` = "data/raw/gugushvili_2025/ESS5e03_5/ESS5e03_5.dta"
)

STRATIFIED_SAMPLE_PATHS <- list(
  `1` = "data/samples/stratified/ESS1e06_7_strat25.csv",
  `2` = "data/samples/stratified/ESS2e03_6_strat25.csv",
  `3` = "data/samples/stratified/ESS3e03_7_strat30.csv",
  `4` = "data/samples/stratified/ESS4e04_6_strat30.csv",
  `5` = "data/samples/stratified/ESS5e03_5_strat30.csv"
)

TASK_FILE       <- "data/raw/aspiration_apprehension/isco08_3d-task3.csv"
CROSSWALK_FILE  <- "data/raw/langenkamp_2022/ess_populist_crosswalk.csv"


# ── Core loading functions ─────────────────────────────────────────────────────

#' Load a single ESS wave
#'
#' @param wave Integer 1–5
#' @param cols Character vector of column names to select (NULL = all)
#' @param countries Character vector of ISO-2 country codes to filter
#' @param sample_only Logical — use stratified sample for development
#' @return data.frame
load_ess_wave <- function(wave, cols = NULL, countries = NULL, sample_only = FALSE) {

  if (sample_only) {
    path <- file.path(ROOT, STRATIFIED_SAMPLE_PATHS[[as.character(wave)]])
    if (!file.exists(path)) {
      stop(sprintf("No stratified sample for wave %d. Run make_stratified_samples.py first.", wave))
    }
    df <- read_csv(path, show_col_types = FALSE)
  } else {
    rel_path <- ESS_WAVE_PATHS[[as.character(wave)]]
    if (is.null(rel_path)) stop(sprintf("Unknown wave: %d", wave))
    path <- file.path(ROOT, rel_path)
    df <- read_dta(path)
    # Convert labelled columns to plain values (keep labels as attributes)
    df <- as_factor(df)
  }

  df$essround <- wave

  if (!is.null(countries)) {
    df <- df %>% filter(cntry %in% countries)
  }

  if (!is.null(cols)) {
    present <- intersect(cols, names(df))
    missing <- setdiff(cols, names(df))
    if (length(missing) > 0) {
      message(sprintf("  ⚠ Columns not in wave %d: %s", wave, paste(missing, collapse = ", ")))
    }
    df <- df %>% select(all_of(present))
  }

  return(df)
}


#' Load and pool multiple ESS waves
#'
#' @param waves Integer vector, default 1:5
#' @param cols Character vector of column names
#' @param countries Character vector of ISO-2 codes
#' @param sample_only Logical
#' @return data.frame
load_pooled_ess <- function(waves = 1:5, cols = NULL, countries = NULL, sample_only = FALSE) {

  frames <- list()
  for (w in waves) {
    tryCatch({
      df_w <- load_ess_wave(w, cols = cols, countries = countries, sample_only = sample_only)
      message(sprintf("  Loaded wave %d: %d rows", w, nrow(df_w)))
      frames[[as.character(w)]] <- df_w
    }, error = function(e) {
      message(sprintf("  ⚠ Wave %d failed: %s", w, e$message))
    })
  }

  if (length(frames) == 0) stop("No waves loaded successfully.")
  bind_rows(frames)
}


# ── RTI task score merger ──────────────────────────────────────────────────────

#' Attach Routine Task Intensity (RTI) scores by ISCO-08 code
#'
#' @param df data.frame with an isco08 column
#' @param isco_col Column name for ISCO-08 codes
#' @return data.frame with task score columns added
attach_rti_scores <- function(df, isco_col = "isco08") {

  task_path <- file.path(ROOT, TASK_FILE)
  if (!file.exists(task_path)) stop(sprintf("Task file not found: %s", task_path))

  tasks <- read_csv(task_path, show_col_types = FALSE)
  message(sprintf("  Task file columns: %s", paste(names(tasks), collapse = ", ")))

  # Find ISCO column in task file
  isco_key <- intersect(c("isco08_3d", "isco3d", "isco08", "isco"), names(tasks))
  if (length(isco_key) == 0) stop("Could not find ISCO column in task file")
  isco_key <- isco_key[1]

  # Create 3-digit ISCO
  if (isco_col %in% names(df)) {
    df <- df %>%
      mutate(isco08_3d = as.integer(as.numeric(.data[[isco_col]]) %/% 10))
    tasks <- tasks %>% rename(isco08_3d = !!isco_key)
    df <- df %>% left_join(tasks, by = "isco08_3d")
    n_matched <- sum(!is.na(df$isco08_3d))
    message(sprintf("  RTI merge: %d/%d rows matched", n_matched, nrow(df)))
  } else {
    message(sprintf("  ⚠ Column '%s' not found. Available: %s",
                    isco_col, paste(names(df)[1:10], collapse = ", ")))
  }

  return(df)
}


# ── Quick inspection helper ────────────────────────────────────────────────────

#' Print quick descriptive info about a dataframe
#'
#' @param df data.frame
#' @param name Label string
quick_info <- function(df, name = "df") {
  cat(sprintf("\n── %s ─────────────────────────────\n", name))
  cat(sprintf("  Shape:    %d rows × %d cols\n", nrow(df), ncol(df)))
  if ("cntry" %in% names(df)) {
    ctries <- sort(unique(na.omit(as.character(df$cntry))))
    cat(sprintf("  Countries (%d): %s\n", length(ctries), paste(ctries, collapse = ", ")))
  }
  if ("essround" %in% names(df)) {
    rnds <- sort(unique(na.omit(df$essround)))
    cat(sprintf("  ESS rounds: %s\n", paste(rnds, collapse = ", ")))
  }
  cat(sprintf("  Columns: %s%s\n",
              paste(names(df)[1:min(8, ncol(df))], collapse = ", "),
              if (ncol(df) > 8) "..." else ""))
}


# ── Demo ───────────────────────────────────────────────────────────────────────

if (FALSE) {  # Set to TRUE to run demo
  # Load stratified samples of waves 1 and 2
  df <- load_pooled_ess(waves = c(1, 2), sample_only = TRUE)
  quick_info(df, "Pooled ESS (waves 1-2, sample)")

  # Attach RTI scores
  if ("isco08" %in% names(df)) {
    df <- attach_rti_scores(df)
  }
}
