predicting whether a user is going to use the product within 12 months (validating vc decision to invest in a company) 
(no llm involved in the weighting process, thus deterministic - but we can add automation to grab data from the web, or somewhere since we're probably not going to have it all info of all companies in a database)

  
input - 
- selection of category (to narrow scope, saves tokens and memory)
- text of an extensive proposal of idea
	- guideline provided depending on the weights of the algorithm

algorithm - 
- currently 8 features
- **price_fit** (below are hard coded values) (not evidence based for the numbers, estimations)
    - ratio = price/WTP (willingness to pay)
        - if ratio <= 0.6, price fit = 1
        - 0.6 <= ratio <= 1, price fit = 1 - 0.45 * (ratio - 0.6)/0.4 (essentially max becomes 0.55)
        - 1.0 <= ratio <= 2, price fit = 0.55 * (2 - ratio) (drops to 0)
        - ratio >2, price_fit = 0.02
- **Calculate S** = weight * score of feature (price_fit is one of the 8 features here)
- **Turn S (sigmoid) into probability of adopting it** P(A)
- **Incorporate analogs** (similar products' performance)
    - if real similar products performing well, then pull up the probability
- **Price multiplier**: P = blended × (0.30 + 0.70 × price_fit)
    - price_fit 1 gives ×1.00. price_fit 0 gives ×0.30.
    - A bad price cuts P by at most 70%.
- **icp fit**: if icp_fit < 0.12, P is reduced to 1/4 (p * 0.25)
    - right target audience matters a lot; so if icp is lower than a certain value, it's sure to drop the p down by a lot.
- **Limit** 0.8% <= P <= 40%: if p is lower or higher than respective values, they get set to 0.8% or 40%
    - reason for 0.8: chance of adoption is never zero, no matter how low
    - reason for 40: almost no new product is near-certain to be adopted within a year and analogs aren't too strong of a proxy anyways.

output - 
- display of which weight is the constraint
- suggestion of how to navigate thru that (list of actions to take)
	- could be something recommended