library(lme4)
library(lmerTest)
library(broom.mixed)
library(dplyr)
library(readr)
library(jsonlite)

set.seed(42)

# ── Load data ──────────────────────────────────────────────────────────────────
cat("Loading data...\n")
df <- read_csv("analysis/sorting_mechanism_master_v2.csv", show_col_types = FALSE)
cat(sprintf("Rows: %d, Cols: %d\n", nrow(df), ncol(df)))

# ── Prep ───────────────────────────────────────────────────────────────────────
df <- df |>
  filter(!is.na(task_z), !is.na(anti_immig_index)) |>
  mutate(
    welfare_regime = factor(welfare_regime,
                            levels = c("Nordic", "Continental", "Liberal", "Southern", "Eastern")),
    non_college    = as.integer(college == 0),
    cntry_wave     = as.character(cntry_wave)
  )

cat(sprintf("Analysis N after listwise: %d\n", nrow(df)))

# ── Controls vector ────────────────────────────────────────────────────────────
ctrls <- "agea + age_sq + female + college + hinctnta + urban"

# ── Random slopes spec (LR test confirmed p<1e-20) ────────────────────────────
re <- "(1 + task_z | cntry_wave)"

# Helper: extract tidy fixed effects + sample size
tidy_model <- function(m, label) {
  t <- tidy(m, effects = "fixed", conf.int = TRUE) |>
    mutate(model = label)
  t$n_obs <- nobs(m)
  t
}

results <- list()

# ── Model 1: RTI baseline ──────────────────────────────────────────────────────
cat("Fitting Model 1...\n")
f1 <- as.formula(paste("anti_immig_index ~ task_z +", ctrls, "+", re))
m1 <- lmer(f1, data = df, REML = TRUE,
           control = lmerControl(optimizer = "bobyqa"))
results[["model1"]] <- tidy_model(m1, "model1")
cat(sprintf("  Model 1 RTI: β=%.3f, SE=%.3f\n",
            fixef(m1)["task_z"], summary(m1)$coefficients["task_z", "Std. Error"]))

# ── Model 2: Welfare regime interaction ───────────────────────────────────────
cat("Fitting Model 2...\n")
df2 <- df |> filter(!is.na(welfare_regime))
f2 <- as.formula(paste(
  "anti_immig_index ~ task_z * welfare_regime +", ctrls, "+", re))
m2 <- lmer(f2, data = df2, REML = TRUE,
           control = lmerControl(optimizer = "bobyqa"))
results[["model2"]] <- tidy_model(m2, "model2")
cat(sprintf("  Model 2 RTI×Liberal: β=%.3f\n",
            fixef(m2)["task_z:welfare_regimeLiberal"]))

# ── Model 3: CWED generosity interaction (key finding) ───────────────────────
cat("Fitting Model 3...\n")
df3 <- df |> filter(!is.na(cwed_generosity_z))
f3 <- as.formula(paste(
  "anti_immig_index ~ task_z * cwed_generosity_z +", ctrls, "+", re))
m3 <- lmer(f3, data = df3, REML = TRUE,
           control = lmerControl(optimizer = "bobyqa"))
results[["model3"]] <- tidy_model(m3, "model3")
cat(sprintf("  Model 3 CWED interaction: β=%.3f, SE=%.3f, p=%.4f\n",
            fixef(m3)["task_z:cwed_generosity_z"],
            summary(m3)$coefficients["task_z:cwed_generosity_z", "Std. Error"],
            summary(m3)$coefficients["task_z:cwed_generosity_z", "Pr(>|t|)"]))

# ── Model 4: Education triple interaction ─────────────────────────────────────
cat("Fitting Model 4...\n")
df4 <- df2 |> mutate(non_college = non_college)
f4 <- as.formula(paste(
  "anti_immig_index ~ task_z * welfare_regime * non_college +",
  "agea + age_sq + female + hinctnta + urban +", re))
m4 <- lmer(f4, data = df4, REML = TRUE,
           control = lmerControl(optimizer = "bobyqa"))
results[["model4"]] <- tidy_model(m4, "model4")
cat("  Model 4 fitted\n")

# ── Model 5: Redistribution DV ───────────────────────────────────────────────
cat("Fitting Model 5...\n")
df5 <- df2 |> filter(!is.na(redist_support))
f5 <- as.formula(paste(
  "redist_support ~ task_z * welfare_regime +", ctrls, "+", re))
m5 <- lmer(f5, data = df5, REML = TRUE,
           control = lmerControl(optimizer = "bobyqa"))
results[["model5"]] <- tidy_model(m5, "model5")
cat("  Model 5 fitted\n")

# ── Model 6: Radical right vote (glmer, binomial) ────────────────────────────
cat("Fitting Model 6 (glmer — may be slow)...\n")
df6 <- df2 |> filter(!is.na(radical_right_vote))
f6 <- as.formula(paste(
  "radical_right_vote ~ task_z * welfare_regime +", ctrls, "+", re))
m6 <- glmer(f6, data = df6, family = binomial,
            control = glmerControl(optimizer = "bobyqa"))
results[["model6"]] <- tidy_model(m6, "model6")
cat(sprintf("  Model 6 RTI: β=%.3f\n", fixef(m6)["task_z"]))

# ── LR test: random slopes vs random intercept only ──────────────────────────
cat("LR test: random slopes vs intercept-only...\n")
m3_ri <- lmer(
  as.formula(paste("anti_immig_index ~ task_z * cwed_generosity_z +", ctrls,
                   "+ (1 | cntry_wave)")),
  data = df3, REML = FALSE,
  control = lmerControl(optimizer = "bobyqa"))
m3_rs <- lmer(
  as.formula(paste("anti_immig_index ~ task_z * cwed_generosity_z +", ctrls,
                   "+", re)),
  data = df3, REML = FALSE,
  control = lmerControl(optimizer = "bobyqa"))
lr <- anova(m3_ri, m3_rs)
cat(sprintf("  LR χ²=%.1f, p=%.2e (random slopes justified)\n",
            lr$Chisq[2], lr$`Pr(>Chisq)`[2]))

# ── Save results ───────────────────────────────────────────────────────────────
all_results <- bind_rows(results)
write_csv(all_results, "outputs/tables/lme4_results.csv")
cat("Saved: outputs/tables/lme4_results.csv\n")

# ── Comparison with Python baseline ──────────────────────────────────────────
py <- fromJSON("analysis/final_results.json")
cat("\n── Coefficient comparison (R random slopes vs Python FE/OLS) ──\n")
cat(sprintf("  Model 1 RTI:             R=%.3f  |  Python=%.3f\n",
            fixef(m1)["task_z"], py$model1$coef_rti))
cat(sprintf("  Model 3 CWED interaction: R=%.3f  |  Python=%.3f\n",
            fixef(m3)["task_z:cwed_generosity_z"], py$model3$coef_interaction))
cat("  (Differences expected: random slopes vs clustered-FE are different estimators)\n")

cat("\nDone. All models fitted successfully.\n")
