"""Auditable commercial scenarios. Research does not determine conversion inputs."""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
segments=[
 ('First-time multi-city travellers','Two or three unfamiliar cities; transport and timing decisions compound.',.38,15,'Checking transfers between cities','Free itinerary + maps','A missed connection can undo the rest of my plan.'),
 ('Families with complex itineraries','Multiple stops with meal, rest and accessibility constraints.',.34,18,'Fitting stops around family constraints','Shared document + maps','The route must work at our pace, not just look good on a map.'),
 ('Group-trip organisers','Four or more people with different budgets and preferences.',.26,12,'Reconciling budgets and preferences','Group chat + free planner','The hard part is getting everyone to agree, not finding more places.'),
 ('Simple city-break travellers','One city, a few saved places and flexible days.',.10,7,'Finding a few useful local suggestions','Free Mindtrip or saved maps','For one city, my free tools already do enough.'),
 ('Frequent work travellers','Flights and hotels already managed; limited leisure planning.',.08,10,'Keeping work and personal plans separate','Employer tool or existing organiser','My existing booking tools handle most of the work.')]
people=[]
for g,(name,desc,eligible,mid,benefit,alternative,objection) in enumerate(segments):
 for i in range(200):
  # Evenly spaced latent values: explicit scenario construction, not sampled survey data.
  u=(i+.5)/200
  def maximum(mult):
   e=eligible*mult
   if u>=e:return 0
   q=u/e
   return round(max(0,mid+5*math.log((1-q)/q)),2)
  complex_max=maximum(1)
  basic_max=maximum(.35)*.6
  people.append({'id':f'D{g*200+i+1:04}','segment':name,'label':f'{name} · scenario {i+1:03}',
   'scenario':desc,'max_gbp_per_trip':complex_max,'basic_max_gbp_per_trip':round(basic_max,2),
   'benefit':benefit,'objection':objection,'alternative':alternative,
   'quote':objection+' I would need to see a usable sample for my own trip before switching.',
   'frictions':[], 'provenance':'Deterministic commercial sensitivity scenario, not customer or model evidence.'})
sources=json.loads((ROOT/'travel/market-sources.json').read_text())
data={'id':'travel-showcase-v3-market-scenarios','mode':'illustrative','sample_size':1000,
 'title':'AI trip-readiness assistant','offer':'Proposed trip-readiness pack for a 7–14 day multi-city trip: identify itinerary timing conflicts, check travel between stops, flag budget mismatches and suggest a fallback day. Show source links and checks; traveller verifies and approves bookings. No human concierge, autonomous booking or guaranteed disruption protection.',
 'price_unit':'GBP per trip','segments':[{'name':s[0],'description':s[1]} for s in segments],'respondents':people,'market_sources':sources,
 'scenario_assumptions':[{'segment':s[0],'eligible_fraction':s[2],'midpoint_gbp':s[3],'slope_gbp':5} for s in segments],
 'method':{'data':'1,000 deterministic fictional scenarios, 200 per buying situation; equal allocation is not a market estimate.',
 'decision_rule':'Trip-readiness: scenario eligibility × logistic price response. Basic itinerary: 35% of readiness eligibility and 60% of its price thresholds. Individual thresholds discretise the curve for inspectability.',
 'uncertainty':'Low/high use 0.6× / 1.4× scenario choices, capped at segment count; sensitivity bounds, NOT confidence intervals.',
 'provenance':'Competitor features/pricing are sourced. Eligibility, GBP price midpoints, slope, concept effects and bounds are unvalidated author assumptions. No model calls; no revenue forecasts.',
 'generation_recipe':'scripts/build_showcase_population.py'}}
(ROOT/'travel/showcase-fixture.json').write_text(json.dumps(data,indent=2)+'\n')
print('Built',len(people),'market scenarios')
