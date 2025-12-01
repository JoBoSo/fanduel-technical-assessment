# SQL Exercise

### Question 1

Since revenue is driven by betting activity, the campaign should focus on reactivating seasonal bettors and increasing engagement for already active users. Two key target groups are:
- `NFL-Season Bettors (Reactivation)`: Activity falls after the NFL season. Email reminders about NFL markets and new features help bring them back. Promos that require deposits can lock in committment to future betting.
- `Highly Engaged Bettors (Growth)`: Multi-sport bettors who respond well to incentives. Smaller, personalized offers can increase betting volume.

Key variables to segment users:
- State
  - Promotions and messaging must comply with state-level regulations
- NFL Betting Behavior 
  - Whether the user has bet on NFL
  - How much NFL represents their overall betting
- Betting Recency & Frequency
  - Identifies active vs. dormant users overall engagement
- Total Bets / Total Stake / GGR
  - Measures user value and informs appropriate incentive levels
- Account Balance
  - Indicates whether a user is able to place new bets without depositing
  - Engaged users with low balances may be more receptive to promos
  - encourage users with high account balances to place more small bets rather than fewer large bets to increase their engagement and generated an expected GGR across their future bets as per the Law of Large Numbers
- Bet Type Preference
  - Offer parlay insurance to parlay-leaning bettors, or incentives to diversify
- Seasonality Metrics
  - % of bets placed during NFL season vs. offseason.
- Activation Date
  - Informs whether or not other variables are relevant for new users and whether we have enough data on them to segment them

FanDuel can optimize it's return on targetted offers by setting offers at the minimum amount to achieve the campaign's objectives to the highest degree. I recommend that users at the intersction of both segments--highly engaged NFL fans--recieve the lowest offers because they will likely take action with the least amount of provocation, while users in the Primarily NFL Fans segment who showed an average level of betting activity during the last NFL season and who haven't been very active since recieve the largest offers. This temps them to get back in the game by increasing the upside potential on their next bet. A simple formula could be constructed send users offers based on their total GGR in the previous season, such as `promo ($) = max($0.0.5 * total user GGR in last NFL season, $2)`. Seasonal users should be sent offers that require a sportsbook deposit, such as for every dollar depsoited, they get they're average GGR/$ betted from the previous season added as a promo. This encourages committment to future betting this season.

Incentive Strategy:

FanDuel can maximize ROI by scaling offers to user value and motivation. Give small incentives to users who are highly engaged and larger incentives to those have been less active since last season.

- high-value, highly engaged NFL bettors
  - personalized boosts using a formula based on their total GGR in the previous NFL season, e.g. `boost = $0.05 * user's avg(GGR)`
  - early access to new features
- Seasonal NFL bettors
  - deposit-linked rewards to lock-in more betting this NFL season
  - early access to new features
- Low-balance, active NFL bettors
  - three small bet credits to keep their activity high

### Question 2

```sql
with
has_deposited as (
    select distinct playerid
    from deposit
    where payment_status = 'a'
        and extract(year from cartdateid) = 2019
),
has_bet as (
    select distinct playerid
    from activity
    where extract(year from betplaceddate) = 2019
)
select count(distinct u.playerid) as active_playerid_2019
from users as u
inner join has_deposited using (playerid)
inner join has_bet using (playerid)
```

I recommend that the CRM Manager add constraints that limit the set of users to those who will be targeted in his campaign. 
- `sb_flag = 1` excludes users who didn't make a Sportsbook deposit.
- It's mentioned that the CRM Manager will send the email to existing users. I recommend that he limit it to users who were active during the previous NFL season and bet on football. I assume we're now in the 2020 off-season, which began December 30, 2019.
  - `activity.sportname = 'Football'`
- The key segmentation variables outlined in (1.) can be incorporated into other queries for tests relating to the segment-specific offers. for tests run within segments, then the CRM Manager should consider the counts within each.

### Question 3 
    i.  playerid 
    ii.  alias 
    iii.  email 
    iv.  total stake generated in 2019 
    v.  margin in 2019 (i.e. gross revenue/stake) 
    vi.  last bet placed date 
    vii.  total amount deposited on Sportsbook (approved deposit only) 
How would you create this list in SQL?

```sql
with
u as (
    select playerid, alias, email
    from users
),
a as (
    select playerid,
        sum(stake) as total_stake_2019,
        sum(ggr) / nullif(sum(stake), 0) as margin_2019,
        max(betplaceddate) as last_bet_placed_date
    from activity
    where extract(year from betplaceddate) = 2019
        and sportname = 'Football'
    group by playerid
),
d as (
    select playerid,
        sum(payment_amount) as total_approved_sportsbook_deposits_2019
    from deposit
    where sb_flag = 1
        and payment_status = 'a'
        and extract(year from cartdateid) = 2019
    group by playerid
)
select u.playerid, u.alias, u.email,
    a.total_stake_2019,
    a.margin_2019,
    a.last_bet_placed_date,
    d.total_approved_sportsbook_deposits_2019
from u
inner join a using (playerid)
inner join d using (playerid)
;
```

### Question 4

```sql
with
activity_ltd as (
    select distinct betid, bettype,
        min(extract(month from betplaceddate)) as month
    from activity
    where betplaceddate between '2019-01-01' and '2019-04-30'
    group by betid, bettype --since parlay bets can span more than one month
),
total_bets as (
    select month,
        count(betid) as total_bets
    from activity_ltd
    group by month
),
total_parlay as (
    select month,
        count(betid) as total_parlay
    from activity_ltd
    where bettype = 'Parlay'
    group by month
)
select month, 
    100 * total_parlay / total_bets as parlay_pct
from total_bets
left join total_parlay using (month)
order by month asc
```

### Question 5

```sql
select extract(month from activation_date) month,
    count(activation_date) / count(registration_date) reg_to_act
from users
where activation_date between '2019-01-01' and '2019-04-30'
group by extract(month from activation_date)
order by month asc
```

We consider users who activated between January and April since activation isn't always immediate, it could occur in a later month. This helps ensure we have a complete dataset to determine the ratio from. It avoids the situation where we're running this in the first week of May, for example, and users who registered at the end of April but activated just a week or two later are excluded.