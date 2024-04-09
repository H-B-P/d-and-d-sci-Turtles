import numpy as np
import pandas as pd
import random
import math

#Ye olde functions:

def roll_dX(X):
 op = {}
 for i in range(X):
  op[i+1] = 1.0/X
 return op

def app(dyct,key,val):
 if key in dyct:
  dyct[key]+=val
 else:
  dyct[key]=val
 return dyct

def p_add(a,b):
 op = {}
 for akey in a:
  for bkey in b:
   op = app(op, akey+bkey, a[akey]*b[bkey])
 return op

#And introducing, the new friends . . .

def normalize(dyct):
    tot = sum(dyct.values())
    return {k: v / tot for k, v in dyct.items()}

def update(pDist, explDists, value):
 newPDist={}
 for outcome in pDist:
  if outcome in explDists:
   if value in explDists[outcome]:
    newPDist[outcome] = pDist[outcome]*explDists[outcome][value]
 return normalize(newPDist)

#Our starting age dist

def get_startingageDist():
 
 age_q=list(range(1,201))
 age_p=[1]
 
 for age in age_q:
  age_p.append(age_p[-1]*(200-age)/200)
 
 age_q = age_q[20:]
 age_p = age_p[21:]
 
 sad = {}
 for i in range(len(age_q)):
  sad[age_q[i]] = age_p[i]
 
 sad = normalize(sad)
 
 return sad

startingageDist = get_startingageDist()


#Distributions of explanatories given ages

def get_wrinklesDists(maxAge):
 wrinklesDists = {0:{0:1}}
 for i in range(maxAge):
  oldWrinklesDist = wrinklesDists[i]
  if i<100:
   newWrinklesDist = p_add(oldWrinklesDist,{0:(100-(i))/100, 1:(i)/100})
  else:
   newWrinklesDist = p_add(oldWrinklesDist,{1:1})
  wrinklesDists[i+1] = newWrinklesDist
 return wrinklesDists

def get_scarsDists(maxAge):
 scarsDists = {0:{0:1}}
 for i in range(maxAge):
  oldScarsDist = scarsDists[i]
  newScarsDist = p_add(oldScarsDist,{0:0.9,1:0.1})
  scarsDists[i+1] = newScarsDist
 return scarsDists

def get_ssDists(maxAge):
 ssDists = {0:{7:1}}
 for i in range(maxAge):
  oldSSDist = ssDists[i]
  newSSDist = {}
  for key in oldSSDist:
   newSSDist = app(newSSDist,key,oldSSDist[key]*(key-1)/key)
   newSSDist = app(newSSDist,key+1,oldSSDist[key]/key)
  ssDists[i+1] = newSSDist
 return ssDists

def get_colorDists(maxAge):
 colorDists = {}
 for i in range(maxAge+1):
  if i<23:
   colorDists[i] = {"green":1}
  if i>=23 and i<35:
   colorDists[i] = {"green":1-(i-22)/12, "grayish-green": (i-22)/12}
  if i>=35 and i<47:
   colorDists[i] = {"grayish-green":1-(i-34)/12, "greenish-gray": (i-22)/12}
  if i>=47:
   colorDists[i] = {"greenish-gray":1}
 return colorDists

wrinklesDists=get_wrinklesDists(200)
scarsDists=get_scarsDists(200)
ssDists=get_ssDists(200)
colorDists=get_colorDists(200)

#Update age given explanatories

def apply_the_updates(ageDist, wrinkles, scars, ss, color):
 ageDist = update(ageDist, wrinklesDists, wrinkles)
 ageDist = update(ageDist, scarsDists, scars)
 ageDist = update(ageDist, ssDists, ss)
 ageDist = update(ageDist, colorDists, color)
 return ageDist
 

#Distributions of weight components given relevant inputs

def get_bodyweightDists(maxAge):
 bwDists = {0:{20:1}}
 for i in range(maxAge):
  oldBWDist = bwDists[i]
  newBWDist = p_add(oldBWDist,{1:1})
  newBWDist = p_add(newBWDist,roll_dX(6))
  bwDists[i+1] = newBWDist
 return bwDists

def get_shellweightDists(maxSS):
 swDists = {0:{5:1}}
 for i in range(maxSS):
  oldSWDist=swDists[i]
  newSWDist=p_add(oldSWDist,{2:1})
  newSWDist=p_add(newSWDist,roll_dX(4))
  swDists[i+1]=newSWDist
 return swDists

def get_magiweightDists(maxAnom):
 mwDists={0:{0:1}}
 for i in range(1,maxAnom):
  mwDists[i] = p_add(mwDists[0],roll_dX(20*i))
 return mwDists

bodyweightDists = get_bodyweightDists(200)
shellweightDists = get_shellweightDists(200)
magiweightDists = get_magiweightDists(10)

#Given we have an agedist, what bwdist should we get?

def ageDist_to_bwDist(ageDist):
 bwDist = {}
 for age in ageDist:
  relevantbwDist = bodyweightDists[age]
  addon = {k: v * ageDist[age] for k, v in relevantbwDist.items()}
  for ao in addon:
   bwDist = app(bwDist, ao, addon[ao])
 return bwDist

#For each turtle type, what is good outcome?

def get_cloneWeightDist(ageDist, ss, ab):
 return {204:1}

def get_vampWeightDist(ageDist, ss, ab):
 return shellweightDists[ss]

def get_normWeightDist(ageDist, ss, ab):
 weightComponent = ageDist_to_bwDist(ageDist)
 shellComponent = shellweightDists[ss]
 magiComponent = magiweightDists[ab]
 return p_add(weightComponent, p_add(shellComponent, magiComponent))

#

def weights_to_mean_payout(weightDist, prediction):
 payout = 0
 for weight in weightDist:
  if weight<=prediction:
   payout+= weightDist[weight]*(200-(prediction-weight))
  else:
   payout+= weightDist[weight]*(200-(weight-prediction)*8)
 return payout


def best_prediction(weightDist):
 bestPred=0
 bestPayout=0
 for prediction in range(2000):
  payout = weights_to_mean_payout(weightDist, prediction)
  if payout>bestPayout:
   bestPred = prediction
   bestPayout = payout
 return bestPred, bestPayout

####################

def gimme(w, s, ss, c, ab, v=False):
	ad = apply_the_updates(get_startingageDist(), w,s,ss, c)
	#print("ad:", ad)
	#print(sum(ad.values()))

	if v:
	 wd = get_vampWeightDist(ad, ss, ab)
	else:
	 wd = get_normWeightDist(ad, ss, ab)
	#print("wd:", wd)
	#print(sum(wd.values()))

	meanweight=0
	for w in wd:
	 meanweight+=w*wd[w]
	print("meanweight:",meanweight)

	bestpred, bestpay = best_prediction(wd)
	print("bps:", bestpred, bestpay)

	print("THE GAP:", bestpred-meanweight)
	print("")

gimme(2,7,10,"green",2)
gimme(1,3,8,"green",1)
gimme(5,5,8,"grayish-green",3)
gimme(1,0,12,"green",1)
gimme(1,0,9,"green",0)
gimme(4,2,14,"gray",5, True)
gimme(5,6,11,"green",6)
print("FREE SPACE")
gimme(4,3,12,"grayish-green",0)
gimme(2,1,12,"green",0)

