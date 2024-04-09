import numpy as np
import pandas as pd
import random
import math

def roll_dX(X):
 return random.choice(list(range(X)))+1

def roll_NdX(N,X):
 op=0
 for i in range(N):
  op+=roll_dX(X)
 return op

random.seed("Hail to the Tyrant")

age_q=list(range(1,201))
age_p=[1]

for age in age_q:
 age_p.append(age_p[-1]*(200-age)/200)

age_q = age_q[20:]
age_p = age_p[21:]

def wrinkles_from_age(age):
 w=0
 for i in range(age):
  if roll_dX(100)<i:
   w+=1
 return w

def scars_from_age(age):
 s=0
 for i in range(age):
  if roll_dX(10)==1:
   s+=1
 return s

def shell_segments_from_age(age):
 ss=7
 for i in range(age):
  if roll_dX(ss)==ss:
   ss+=1
 return ss


def color_from_age(age):
 t1 = 22+roll_dX(12)
 t2 = 34+roll_dX(12)
 if age<t1:
  return "green"
 if age<t2:
  return "grayish-green"
 return "greenish-gray"
 

def gen_turt():
 if roll_dX(100)<19:
  age=9999
  wr=0
  sc=roll_dX(6)
  ss=6
  co="green"
  fa="no"
  no="normal"
  ab=0
  we=204
  
  return age, wr, sc, ss, co, fa, no, ab, we
  
 age = random.choices(age_q, age_p)[0]
 wr = wrinkles_from_age(age)
 sc = scars_from_age(age)
 ss = shell_segments_from_age(age)
 co = color_from_age(age)
 fa = random.choice(["yes"]*13+["no"]*87)
 if fa=="yes":
  co="gray"
 no = random.choice(["unusually small"]*5+["normal"]*57+["unusually large"]*8)
 
 
 ab = 0
 if roll_dX(100)>44:
  ab = min(roll_dX(8),roll_dX(10),roll_dX(10),roll_dX(12))
 
 shellweight = 5+2*ss+roll_NdX(ss,4)
 bodyweight = 20+age+roll_NdX(age,6)
 if ab>0:
  bodyweight+=roll_dX(ab*20)
 if fa=="yes":
  we = shellweight
 else:
  we = shellweight+bodyweight
 
 return age, wr, sc, ss, co, fa, no, ab, we

def gen_df(N):
 
 ageList=[]
 wrList=[]
 scList=[]
 ssList=[]
 coList=[]
 faList=[]
 noList=[]
 abList=[]
 weList=[]
 
 for i in range(N):
  age, wr,sc,ss,co,fa,no,ab,we = gen_turt()
  
  ageList.append(age)
  wrList.append(wr)
  scList.append(sc)
  ssList.append(ss)
  coList.append(co)
  faList.append(fa)
  noList.append(no)
  abList.append(ab)
  weList.append(str(we/10)+"lb")
 
 df = pd.DataFrame({"Age":ageList,"Wrinkles":wrList,"Scars":scList,"Shell Segments":ssList,"Color":coList,"Fangs for some reason":faList, "Nostril Size":noList, "Miscellaneous Abnormalities":abList, "Weight":weList})
 
 return df

#df = gen_df(3032)
df = gen_df(30032)

df.to_csv("turt.csv")


random.seed("Precious Beasts")

df = gen_df(10)

df.to_csv("test.csv")
