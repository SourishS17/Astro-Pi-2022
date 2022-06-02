f=open("results.csv","r").readlines()
ff=open("entropy.csv","w")

g=""

cc,dd,ee=[],[],[]
m,mm=[],[]

for i in f:
  if i[0]=="l":continue
  a,b,c,d,e=[float(r) for r in i.split(",")]
  cc,dd,ee=cc+[c],dd+[d],ee+[e]
  m,mm=m+[a],mm+[b]
  #c,d,e=c+1,d+1,e+1
  #v=d/(c+e)
  
  #g+=str(v)+"\n"
  
  
#print(cc)
z,x=min(cc),max(cc)
#print(z,x)
l=abs(x-z)
#print(l)
l=1/l
print(l)

#print(cc)
zz,xx=min(dd),max(dd)
#print(z,x)
ll=abs(xx-zz)
#print(l)
ll=1/ll
print(ll)

#print(cc)
zzz,xxx=min(ee),max(ee)
#print(z,x)
lll=abs(xxx-zzz)
#print(l)
lll=1/lll
print(lll)
k=[]
p=0
for i in f:
  p+=1
  if i[0]=="l":continue
  a,b,c,d,e=[float(r) for r in i.split(",")]
  #cc,dd,ee=cc+[c],dd+[d],ee+[e]
  #c,d,e=c+1,d+1,e+1
  
  c=abs(c-z)*l
  d=abs(d-zz)*ll
  e=abs(e-zzz)*lll
  #print(c,d,e,p)
  
  try:v=d/(c+e)
  except:v=1.0
  #g+=str(v)+"\n"
  k.append(v)
  
z,x=min(k),max(k)
#print(z,x)
l=abs(x-z)
#print(l)
l=1/l
print(l)
p=0

j=[]

for i in k:
  
  v=abs(i-z)*l
  
  
  j.append((m[p],mm[p],v,p+1))
  #g+=str(m[p])+","+str(mm[p])+","+str(v)+"\n"
  p+=1

j=sorted(j,key=lambda b:b[2])
g="ent,lat,lon,pic\n"

for i in j:
  g+=str(i[2])+","+str(i[0])+","+str(i[1])+","+str(i[-1])+"\n"
  
g=g[:-1]
ff.write(g)
ff.close()
