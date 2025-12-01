# Predicting Player Bet-Cycle Drop-Off & Optimal Intervention Timing

## Overview & Motivation
A large portion of Sportsbook revenue comes from recurring bettors who engage across many sporting events and over long periods of time. However, engagement can be highly cyclical. Users frequently enter periods where betting slows or stops altogether. If FanDuel can more accurately predict when a player is beginning to disengage, it can proactively deploy personalized messaging or product experiences designed to sustain interest and provide value at the right moment.

The objective of this research project is to identify patterns in player behavior that occur just before a drop-off period, enabling FanDuel to build an early-signal retention model. With strong predictive accuracy, FanDuel can execute well-timed interventions that both increase total engagement and promote responsible betting behavior, ensuring the experience remains fun and within healthy limits.

---

## Hypothesis
Players exhibit detectable shifts in activity before disengagement. Changes in variables such as session frequency, sport diversity, bet type usage, and betting volatility can signal that a player is entering a pre-churn state. By identifying this state early, FanDuel can deliver context-appropriate re-activation nudges that align with user preferences.

---

## Variables of Interest
This project analyzes longitudinal player behavior using rolling windows (e.g., 7-day and 30-day look-backs). Key indicators include:

| Behavioral Indicator | Why It Matters |
|--------------------|----------------|
| **Days since last bet** | Increased inactivity raises churn likelihood |
| **Session frequency** | Steady declines often precede full disengagement |
| **Sport diversity trends** | Narrowing activity may signal reduced interest |
| **Bet type & odds risk profile** | Changes reflect shifts in confidence or excitement |
| **Win/loss volatility** | Streak-based frustration may drive disengagement |
| **Marketing touchpoint interactions** | Ignored promotions can signal disengagement |

These features focus on behavioral momentum rather than raw outcomes.

---

## Methodology

### 1. Feature Engineering
- Construct player activity timelines
- Standardize features for individualized betting styles
- Create rate-of-change and trend metrics
- Include streak-based and recent-event effects

This will create dynamic behavioral signatures for each player.

### 2. Predictive Modeling
Two modeling approaches will be tested:

| Model Type | Purpose |
|------------|---------|
| **Gradient Boosted Trees (e.g., XGBoost)** | Predict likelihood of churn in next N days |
| **Survival Analysis (Cox Hazard / Random Survival Forest)** | Estimate *time until disengagement* |

Feature importance analysis will reveal which behaviors are the strongest signals.

### 3. Intervention Strategy & Experimentation
At-risk users will be included in targeted A/B tests, such as:
- Alerts for relevant upcoming sports events
- Lower-barrier DFS or Fantasy entries
- “Bet & Watch” live-betting experiences
- Reminders of responsible gambling tools

The goal: boost engagement while maintaining safety-first principles.

### 4. Success Measurement
KPIs include:
- Reduced churn vs. control group
- Increased betting days over next 30–60 days
- Incremental GGR attributable to interventions
- Higher usage of healthy play features

---

## Expected Outcomes

| Outcome Type | Impact |
|-------------|--------|
| **Business Value** | Sustainable GGR lift through better retention |
| **Customer Value** | More relevant, enjoyable, timely experiences |
| **Operational Value** | Clear rules for when to communicate with players |
| **Responsible Gaming** | Early detection supports healthier play patterns |

The model shifts the strategy from *reactive* churn response to *proactive* churn prevention.

---

## Conclusion
By leveraging behavioral signals and predictive modeling, FanDuel can significantly enhance its ability to retain players who enjoy betting responsibly. This project supports the business goal of increasing lifetime value while ensuring a player-centric experience.

The result is a smarter Sportsbook that recognizes early when players are drifting away and steps in with the right engagement at the right time.

