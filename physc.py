from math import pi,sin,cos,tan,asin,acos,atan,sqrt,exp

g=9.8
GC=6.674e-11
NAMES={"__builtins__":{},"sin":sin,"cos":cos,"tan":tan,"asin":asin,"acos":acos,
"atan":atan,"sqrt":sqrt,"exp":exp,"pi":pi,"g":g}
FUNS=("sin","cos","tan","asin","acos","atan","sqrt","exp")

def tok(e):
 e=e.replace(" ","")
 ts=[];i=0
 while i<len(e):
  c=e[i]
  if c.isdigit() or c==".":
   j=i+1
   while j<len(e) and (e[j].isdigit() or e[j]=="."):j+=1
   if j<len(e) and (e[j]=="e" or e[j]=="E"):
    j+=1
    if j<len(e) and (e[j]=="+" or e[j]=="-"):j+=1
    while j<len(e) and e[j].isdigit():j+=1
   ts.append(e[i:j]);i=j
  elif c.isalpha():
   j=i+1
   while j<len(e) and e[j].isalpha():j+=1
   ts.append(e[i:j]);i=j
  else:
   ts.append(c);i+=1
 return ts

def endfac(t):return t==")" or t[0].isdigit() or t[0]=="." or t[0].isalpha()
def startfac(t):return t=="(" or t[0].isdigit() or t[0]=="." or t[0].isalpha()

def fixexpr(e):
 ts=tok(e);out=[]
 for i,t in enumerate(ts):
  if i:
   p=ts[i-1]
   if endfac(p) and startfac(t) and not (p in FUNS and t=="("):
    out.append("*")
  out.append(t)
 return "".join(out)

def gn(p):
 while True:
  try:return float(eval(fixexpr(input(p+": ")),NAMES))
  except:print("?")

def gi(p):
 while True:
  try:return int(input(p+": "))
  except:print("?")

def ge(p):return fixexpr(input(p+" (use u): "))

def mkf(e):
 def f(u):
  ns=NAMES.copy();ns["u"]=u
  return eval(e,ns)
 return f

def menu(t,opts):
 while True:
  print("")
  print(t)
  for i,(lbl,_) in enumerate(opts,1):
   print(str(i)+"."+lbl)
  try:
   c=int(input("> "))
   if 1<=c<=len(opts):return opts[c-1][1]
  except EOFError:return opts[-1][1]
  except:pass

def yes(p):return input(p+" 1=y: ").strip()=="1"
def sgn():return -1 if input("sgn 1=+,-1=-: ").strip()=="-1" else 1

def nint(f,a,b,n=120):
 if n%2:n+=1
 h=(b-a)/n
 s=f(a)+f(b)
 for i in range(1,n):
  s+=(4 if i%2 else 2)*f(a+i*h)
 return s*h/3

def dfx(f,x,h=1e-4):return (f(x+h)-f(x-h))/(2*h)
def d2fx(f,x,h=1e-3):return (f(x+h)-2*f(x)+f(x-h))/(h*h)

def quad_roots(a,b,c):
 d=b*b-4*a*c
 if d<0:return []
 s=sqrt(d)
 return [(-b+s)/(2*a),(-b-s)/(2*a)]

def show(label,val):print(label+" = "+str(val))

def get_a():
 c=menu("Find a from",[
  ("Fnet=m*a",1),("incline",2),("a_c=v^2/r",3),
  ("a_c=w^2*r",4),("a_t=r*alpha",5),("from a(t)",6),
  ("given",7)])
 if c==1:
  F=gn("Fnet");m=gn("m");a=F/m
  show("a=Fnet/m",a);return a
 if c==2:
  th=gn("theta rad");mu=gn("mu")
  a=g*(sin(th)-mu*cos(th));show("a",a);return a
 if c==3:
  v=gn("v");r=gn("r");a=v*v/r;show("a_c",a);return a
 if c==4:
  w=gn("omega");r=gn("r");a=w*w*r;show("a_c",a);return a
 if c==5:
  r=gn("r");al=gn("alpha");a=r*al;show("a_t",a);return a
 if c==6:
  e=ge("a(u)");t=gn("t");a=mkf(e)(t);show("a(t)",a);return a
 return gn("a")

def get_I():
 c=menu("I shape",[
  ("point m*r^2",1),("hoop M*R^2",2),("disk .5MR^2",3),
  ("sld sphere .4MR^2",4),("hol sphere (2/3)MR^2",5),
  ("rod center 1/12 ML^2",6),("rod end 1/3 ML^2",7),
  ("parallel axis",8),("given",9)])
 if c==1:m=gn("m");r=gn("r");I=m*r*r
 elif c==2:M=gn("M");R=gn("R");I=M*R*R
 elif c==3:M=gn("M");R=gn("R");I=.5*M*R*R
 elif c==4:M=gn("M");R=gn("R");I=.4*M*R*R
 elif c==5:M=gn("M");R=gn("R");I=(2/3)*M*R*R
 elif c==6:M=gn("M");L=gn("L");I=M*L*L/12
 elif c==7:M=gn("M");L=gn("L");I=M*L*L/3
 elif c==8:Ic=gn("Icm");M=gn("M");d=gn("d");I=Ic+M*d*d
 else:I=gn("I")
 show("I",I);return I

def kin():
 while True:
  c=menu("Kinematics",[
   ("v final",1),("x final",2),("a accel",3),
   ("t time",4),("projectile",5),("rolling v(h)",6),
   ("Back",0)])
  if c==0:return
  if c==1:kv()
  elif c==2:kx()
  elif c==3:ka()
  elif c==4:kt()
  elif c==5:proj()
  elif c==6:rolling()

def kv():
 c=menu("Find v",[
  ("v=v0+a*t",1),("v^2=v0^2+2adx",2),
  ("from energy",3),("from impulse",4),
  ("from int a(t)dt",5),("Back",0)])
 if c==0:return
 if c==1:
  v0=gn("v0");a=get_a();t=gn("t")
  show("v=v0+a*t",v0+a*t)
 elif c==2:
  v0=gn("v0");x0=gn("x0");x=gn("x");a=get_a()
  s=sgn();dx=x-x0
  disc=v0*v0+2*a*dx
  if disc<0:print("no real v");return
  show("dx",dx);show("v",s*sqrt(disc))
 elif c==3:
  m=gn("m");Ki=gn("Ki");Ui=gn("Ui")
  Wnc=gn("W_nc");Uf=gn("Uf");s=sgn()
  E=Ki+Ui+Wnc-Uf
  if E<0:print("imag");return
  show("v",s*sqrt(2*E/m))
 elif c==4:
  m=gn("m");v0=gn("v0")
  if yes("Know J?"):
   J=gn("J")
  else:
   F=gn("Favg");dt=gn("dt");J=F*dt;show("J=F*dt",J)
  show("vf=v0+J/m",v0+J/m)
 elif c==5:
  m=gn("m");v0=gn("v0");e=ge("a(u)")
  t1=gn("t1");t2=gn("t2")
  dv=nint(mkf(e),t1,t2)
  show("dv",dv);show("vf",v0+dv)

def kx():
 c=menu("Find x",[
  ("x=x0+v0t+.5at^2",1),("x=x0+((v+v0)/2)t",2),
  ("x=x0+int v(t)dt",3),("Back",0)])
 if c==0:return
 if c==1:
  x0=gn("x0");v0=gn("v0");t=gn("t");a=get_a()
  show("x",x0+v0*t+.5*a*t*t)
 elif c==2:
  x0=gn("x0");v0=gn("v0");v=gn("v");t=gn("t")
  show("x",x0+(v+v0)/2*t)
 elif c==3:
  x0=gn("x0");e=ge("v(u)");t1=gn("t1");t2=gn("t2")
  dx=nint(mkf(e),t1,t2);show("dx",dx);show("x",x0+dx)

def ka():
 c=menu("Find a",[
  ("a=(v-v0)/t",1),("a=(v^2-v0^2)/2dx",2),
  ("a=Fnet/m",3),("incline",4),
  ("a_c=v^2/r",5),("a_c=w^2*r",6),
  ("a_t=r*alpha",7),("from dv/dt",8),
  ("from d2x/dt2",9),("Back",0)])
 if c==0:return
 if c==1:
  v=gn("v");v0=gn("v0");t=gn("t");show("a",(v-v0)/t)
 elif c==2:
  v=gn("v");v0=gn("v0");x0=gn("x0");x=gn("x")
  show("a",(v*v-v0*v0)/(2*(x-x0)))
 elif c==3:
  F=gn("Fnet");m=gn("m");show("a",F/m)
 elif c==4:
  th=gn("theta rad");mu=gn("mu")
  show("a",g*(sin(th)-mu*cos(th)))
 elif c==5:
  v=gn("v");r=gn("r");show("a_c",v*v/r)
 elif c==6:
  w=gn("omega");r=gn("r");show("a_c",w*w*r)
 elif c==7:
  r=gn("r");al=gn("alpha");show("a_t",r*al)
 elif c==8:
  e=ge("v(u)");t=gn("t");show("a=dv/dt",dfx(mkf(e),t))
 elif c==9:
  e=ge("x(u)");t=gn("t");show("a=d2x/dt2",d2fx(mkf(e),t))

def kt():
 c=menu("Find t",[
  ("t=(v-v0)/a",1),("quadratic in x eq",2),
  ("T circular 2pi r/v",3),("T spring",4),
  ("T pendulum",5),("Back",0)])
 if c==0:return
 if c==1:
  v=gn("v");v0=gn("v0");a=get_a()
  show("t",(v-v0)/a)
 elif c==2:
  x0=gn("x0");x=gn("x");v0=gn("v0");a=get_a()
  rs=quad_roots(.5*a,v0,x0-x)
  print("Solutions:")
  for r in rs:print(" t =",r)
 elif c==3:
  r=gn("r");v=gn("v");show("T",2*pi*r/v)
 elif c==4:
  m=gn("m");k=gn("k");show("T",2*pi*sqrt(m/k))
 elif c==5:
  L=gn("L");show("T",2*pi*sqrt(L/g))

def proj():
 c=menu("Projectile",[
  ("range level",1),("max height",2),
  ("time of flight level",3),("components v0",4),
  ("y(t)",5),("x(t)",6),
  ("y(x) trajectory",7),("hit from h",8),
  ("Back",0)])
 if c==0:return
 if c==1:
  v0=gn("v0");th=gn("theta rad")
  show("R",v0*v0*sin(2*th)/g)
 elif c==2:
  v0=gn("v0");th=gn("theta rad")
  show("H",(v0*sin(th))**2/(2*g))
 elif c==3:
  v0=gn("v0");th=gn("theta rad")
  show("T",2*v0*sin(th)/g)
 elif c==4:
  v=gn("v");th=gn("theta rad")
  show("vx",v*cos(th));show("vy",v*sin(th))
 elif c==5:
  v0=gn("v0");th=gn("theta rad");y0=gn("y0");t=gn("t")
  show("y(t)",y0+v0*sin(th)*t-.5*g*t*t)
 elif c==6:
  v0=gn("v0");th=gn("theta rad");x0=gn("x0");t=gn("t")
  show("x(t)",x0+v0*cos(th)*t)
 elif c==7:
  v0=gn("v0");th=gn("theta rad");x=gn("x")
  show("y",x*tan(th)-g*x*x/(2*(v0*cos(th))**2))
 elif c==8:
  v0=gn("v0");th=gn("theta rad");h=gn("h start")
  rs=quad_roots(-.5*g,v0*sin(th),h)
  print("Times to ground:")
  for r in rs:
   if r>=0:print(" t =",r)

def rolling():
 print("Rolling v from height drop")
 print("mgh = .5mv^2 + .5Iw^2, v=rw")
 m=gn("m");h=gn("h drop");r=gn("r rolling")
 if yes("Know I?"):
  I=gn("I")
 else:
  I=get_I()
 v=sqrt(2*g*h/(1+I/(m*r*r)))
 show("v",v)

def force():
 while True:
  c=menu("Forces",[
   ("Fnet",1),("normal",2),("friction",3),
   ("incline a",4),("spring F=-kx",5),
   ("Atwood",6),("banking",7),
   ("loop top/bot",8),("drag",9),
   ("Back",0)])
  if c==0:return
  if c==1:ff()
  elif c==2:fn()
  elif c==3:ffr()
  elif c==4:fi()
  elif c==5:
   k=gn("k");x=gn("x");show("F=-kx",-k*x)
  elif c==6:fatw()
  elif c==7:fbk()
  elif c==8:flp()
  elif c==9:fdr()

def ff():
 c=menu("Fnet from",[
  ("m*a",1),("centripetal mv^2/r",2),
  ("sum components",3),("dp/dt of p(t)",4),
  ("Back",0)])
 if c==0:return
 if c==1:
  m=gn("m");a=gn("a");show("F=m*a",m*a)
 elif c==2:
  m=gn("m");v=gn("v");r=gn("r");show("Fc",m*v*v/r)
 elif c==3:
  n=gi("how many forces")
  s=0
  for i in range(n):
   f=gn("F"+str(i+1)+" signed");s+=f
  show("Fnet",s)
 elif c==4:
  e=ge("p(u)");t=gn("t");show("F=dp/dt",dfx(mkf(e),t))

def fn():
 c=menu("Normal force",[
  ("flat N=mg",1),("incline mg*cos",2),
  ("vertical accel m(g+a)",3),
  ("loop bottom",4),("loop top",5),
  ("Back",0)])
 if c==0:return
 if c==1:m=gn("m");show("N",m*g)
 elif c==2:
  m=gn("m");th=gn("theta rad");show("N",m*g*cos(th))
 elif c==3:
  m=gn("m");a=gn("a vert");show("N",m*(g+a))
 elif c==4:
  m=gn("m");v=gn("v");r=gn("r");show("N",m*g+m*v*v/r)
 elif c==5:
  m=gn("m");v=gn("v");r=gn("r");show("N",m*v*v/r-m*g)

def ffr():
 c=menu("Friction",[
  ("kinetic mu_k*N",1),("max static mu_s*N",2),
  ("Back",0)])
 if c==0:return
 mu=gn("mu");N=gn("N");show("f",mu*N)

def fi():
 print("Down-slope accel")
 th=gn("theta rad");mu=gn("mu (0 if none)")
 show("a",g*(sin(th)-mu*cos(th)))

def fatw():
 c=menu("Atwood",[
  ("simple 2 hanging",1),("one on table",2),
  ("one on incline",3),("Back",0)])
 if c==0:return
 if c==1:
  m1=gn("m1 heavy");m2=gn("m2 light")
  a=(m1-m2)*g/(m1+m2);T=2*m1*m2*g/(m1+m2)
  show("a",a);show("T",T)
 elif c==2:
  m1=gn("m1 hang");m2=gn("m2 table");mu=gn("mu_k")
  a=(m1-mu*m2)*g/(m1+m2);T=m1*(g-a)
  show("a",a);show("T",T)
 elif c==3:
  m1=gn("m1 hang");m2=gn("m2 incl")
  th=gn("theta rad");mu=gn("mu_k")
  a=(m1-m2*(sin(th)+mu*cos(th)))*g/(m1+m2)
  T=m1*(g-a)
  show("a",a);show("T",T)

def fbk():
 c=menu("Banking",[
  ("frictionless angle",1),("max v friction",2),
  ("min v friction",3),("Back",0)])
 if c==0:return
 if c==1:
  v=gn("v");r=gn("r");show("theta",atan(v*v/(r*g)))
 elif c==2:
  r=gn("r");th=gn("theta rad");mu=gn("mu")
  num=sin(th)+mu*cos(th);den=cos(th)-mu*sin(th)
  if den<=0:print("no real vmax");return
  show("vmax",sqrt(r*g*num/den))
 elif c==3:
  r=gn("r");th=gn("theta rad");mu=gn("mu")
  num=sin(th)-mu*cos(th);den=cos(th)+mu*sin(th)
  v2=r*g*num/den
  if v2<=0:print("any low v ok");return
  show("vmin",sqrt(v2))

def flp():
 c=menu("Vertical loop",[
  ("min top v=sqrt(gr)",1),("N bottom",2),
  ("N top",3),("Back",0)])
 if c==0:return
 if c==1:r=gn("r");show("v_min_top",sqrt(g*r))
 elif c==2:
  m=gn("m");v=gn("v bot");r=gn("r")
  show("N_bot",m*g+m*v*v/r)
 elif c==3:
  m=gn("m");v=gn("v top");r=gn("r")
  show("N_top",m*v*v/r-m*g)

def fdr():
 c=menu("Drag",[
  ("linear bv terminal",1),("quadratic cv^2 term",2),
  ("v(t) linear drag",3),("Back",0)])
 if c==0:return
 if c==1:m=gn("m");b=gn("b");show("v_term",m*g/b)
 elif c==2:m=gn("m");c2=gn("c");show("v_term",sqrt(m*g/c2))
 elif c==3:
  m=gn("m");b=gn("b");t=gn("t")
  show("v",(m*g/b)*(1-exp(-b*t/m)))

def energy():
 while True:
  c=menu("Energy",[
   ("W=F*d*cos",1),("K=.5mv^2 / solve v",2),
   ("Ug=mgy",3),("Us=.5kx^2",4),
   ("power",5),("Wnet=dK",6),
   ("energy conserv->v",7),("rolling K_total",8),
   ("x from spring U",9),("W from F(x)",10),
   ("Back",0)])
  if c==0:return
  if c==1:
   F=gn("F");d=gn("d");th=gn("theta rad")
   show("W",F*d*cos(th))
  elif c==2:
   if yes("Have K? else compute"):
    K=gn("K");m=gn("m");s=sgn()
    show("v",s*sqrt(2*K/m))
   else:
    m=gn("m");v=gn("v");show("K",.5*m*v*v)
  elif c==3:m=gn("m");y=gn("y");show("Ug",m*g*y)
  elif c==4:k=gn("k");x=gn("x");show("Us",.5*k*x*x)
  elif c==5:enp()
  elif c==6:
   Ki=gn("Ki");Kf=gn("Kf");show("Wnet=dK",Kf-Ki)
  elif c==7:
   m=gn("m");Ki=gn("Ki");Ui=gn("Ui")
   Wnc=gn("W_nc");Uf=gn("Uf");s=sgn()
   E=Ki+Ui+Wnc-Uf
   if E<0:print("imag");continue
   show("v",s*sqrt(2*E/m))
  elif c==8:
   m=gn("m");v=gn("v");r=gn("r rolling")
   if yes("Know I?"):I=gn("I")
   else:I=get_I()
   w=v/r;show("K_total",.5*m*v*v+.5*I*w*w)
  elif c==9:
   U=gn("U_spring");k=gn("k")
   if U<0:print("imag");continue
   show("x",sqrt(2*U/k))
  elif c==10:
   e=ge("F(u)");x1=gn("x1");x2=gn("x2")
   show("W",nint(mkf(e),x1,x2))

def enp():
 c=menu("Power",[
  ("P=W/t avg",1),("P=F*v*cos inst",2),
  ("P=dW/dt of W(t)",3),("Back",0)])
 if c==0:return
 if c==1:W=gn("W");t=gn("t");show("P",W/t)
 elif c==2:
  F=gn("F");v=gn("v");th=gn("theta rad")
  show("P",F*v*cos(th))
 elif c==3:
  e=ge("W(u)");t=gn("t");show("P",dfx(mkf(e),t))

def mom():
 while True:
  c=menu("Momentum",[
   ("p=m*v",1),("impulse J",2),
   ("vf from impulse",3),("center of mass",4),
   ("v_cm of system",5),("1D elastic",6),
   ("1D inelastic",7),("coef restit",8),
   ("F=dp/dt",9),("Back",0)])
  if c==0:return
  if c==1:m=gn("m");v=gn("v");show("p",m*v)
  elif c==2:mj()
  elif c==3:mv()
  elif c==4:mcm()
  elif c==5:
   m1=gn("m1");v1=gn("v1");m2=gn("m2");v2=gn("v2")
   show("v_cm",(m1*v1+m2*v2)/(m1+m2))
  elif c==6:
   m1=gn("m1");v1=gn("v1i");m2=gn("m2");v2=gn("v2i")
   v1f=((m1-m2)/(m1+m2))*v1+(2*m2/(m1+m2))*v2
   v2f=(2*m1/(m1+m2))*v1+((m2-m1)/(m1+m2))*v2
   show("v1f",v1f);show("v2f",v2f)
  elif c==7:
   m1=gn("m1");v1=gn("v1i");m2=gn("m2");v2=gn("v2i")
   show("vf",(m1*v1+m2*v2)/(m1+m2))
  elif c==8:
   v1=gn("v1i");v2=gn("v2i")
   p1=gn("v1f");p2=gn("v2f")
   show("e",(p2-p1)/(v1-v2))
  elif c==9:
   e=ge("p(u)");t=gn("t");show("F=dp/dt",dfx(mkf(e),t))

def mj():
 c=menu("Impulse",[
  ("J=Favg*dt",1),("J=pf-pi",2),
  ("J=int F(t)dt",3),("Back",0)])
 if c==0:return
 if c==1:F=gn("Favg");dt=gn("dt");show("J",F*dt)
 elif c==2:pf=gn("pf");pi2=gn("pi");show("J",pf-pi2)
 elif c==3:
  e=ge("F(u)");t1=gn("t1");t2=gn("t2")
  show("J",nint(mkf(e),t1,t2))

def mv():
 m=gn("m");v0=gn("v0")
 if yes("Know J?"):
  J=gn("J")
 else:
  c=menu("J source",[
   ("J=Favg*dt",1),("J=int F(t)dt",2)])
  if c==1:F=gn("Favg");dt=gn("dt");J=F*dt
  else:
   e=ge("F(u)");t1=gn("t1");t2=gn("t2")
   J=nint(mkf(e),t1,t2)
  show("J",J)
 show("vf=v0+J/m",v0+J/m)

def mcm():
 n=gi("n particles (2-4)")
 sm=0;sx=0
 for i in range(n):
  mi=gn("m"+str(i+1));xi=gn("x"+str(i+1))
  sm+=mi;sx+=mi*xi
 show("xcm",sx/sm)

def rot():
 while True:
  c=menu("Rotation",[
   ("I (find)",1),("torque tau",2),
   ("angular accel alpha",3),("angular kinematics",4),
   ("circular motion",5),("K_rot",6),
   ("angular momentum L",7),("conserve L",8),
   ("Back",0)])
  if c==0:return
  if c==1:get_I()
  elif c==2:rtau()
  elif c==3:ral()
  elif c==4:rk()
  elif c==5:rcir()
  elif c==6:ren()
  elif c==7:rl()
  elif c==8:
   Ii=gn("Ii");wi=gn("wi");If=gn("If")
   show("wf",Ii*wi/If)

def rtau():
 c=menu("Torque",[
  ("tau=rFsin",1),("tau=I*alpha",2),
  ("tau=dL/dt",3),("Back",0)])
 if c==0:return
 if c==1:
  r=gn("r");F=gn("F");th=gn("theta rad")
  show("tau",r*F*sin(th))
 elif c==2:
  if yes("Know I?"):I=gn("I")
  else:I=get_I()
  al=gn("alpha");show("tau",I*al)
 elif c==3:
  e=ge("L(u)");t=gn("t");show("tau",dfx(mkf(e),t))

def ral():
 c=menu("Find alpha",[
  ("alpha=tau/I",1),("alpha=(w-w0)/t",2),
  ("alpha from dw/dt",3),("Back",0)])
 if c==0:return
 if c==1:
  tau=gn("tau")
  if yes("Know I?"):I=gn("I")
  else:I=get_I()
  show("alpha",tau/I)
 elif c==2:
  w=gn("omega");w0=gn("omega0");t=gn("t")
  show("alpha",(w-w0)/t)
 elif c==3:
  e=ge("w(u)");t=gn("t");show("alpha",dfx(mkf(e),t))

def rk():
 c=menu("Angular kin",[
  ("w=w0+alpha*t",1),("th=th0+w0t+.5at^2",2),
  ("w^2=w0^2+2a*dth",3),("dth=.5(w+w0)t",4),
  ("Back",0)])
 if c==0:return
 if c==1:
  w0=gn("w0");al=gn("alpha");t=gn("t")
  show("w",w0+al*t)
 elif c==2:
  th0=gn("th0");w0=gn("w0");al=gn("alpha");t=gn("t")
  show("theta",th0+w0*t+.5*al*t*t)
 elif c==3:
  w0=gn("w0");al=gn("alpha")
  th0=gn("th0");th=gn("theta");s=sgn()
  disc=w0*w0+2*al*(th-th0)
  if disc<0:print("no real");return
  show("w",s*sqrt(disc))
 elif c==4:
  w=gn("w");w0=gn("w0");t=gn("t")
  show("dtheta",.5*(w+w0)*t)

def rcir():
 c=menu("Circular",[
  ("v=r*w",1),("a_t=r*alpha",2),
  ("a_c=v^2/r",3),("a_c=w^2*r",4),
  ("F_c=mv^2/r",5),("T=2pi/w",6),
  ("Back",0)])
 if c==0:return
 if c==1:r=gn("r");w=gn("w");show("v",r*w)
 elif c==2:r=gn("r");al=gn("alpha");show("a_t",r*al)
 elif c==3:v=gn("v");r=gn("r");show("a_c",v*v/r)
 elif c==4:w=gn("w");r=gn("r");show("a_c",w*w*r)
 elif c==5:m=gn("m");v=gn("v");r=gn("r");show("Fc",m*v*v/r)
 elif c==6:w=gn("w");show("T",2*pi/w)

def ren():
 if yes("Know I?"):I=gn("I")
 else:I=get_I()
 w=gn("omega");show("K_rot",.5*I*w*w)

def rl():
 c=menu("Angular momentum L",[
  ("L=I*omega",1),("L=mvr (point)",2),
  ("L=mvr*sin",3),("Back",0)])
 if c==0:return
 if c==1:
  if yes("Know I?"):I=gn("I")
  else:I=get_I()
  w=gn("omega");show("L",I*w)
 elif c==2:
  m=gn("m");v=gn("v");r=gn("r");show("L",m*v*r)
 elif c==3:
  m=gn("m");v=gn("v");r=gn("r");th=gn("theta rad")
  show("L",m*v*r*sin(th))

def osc():
 while True:
  c=menu("SHM",[
   ("T spring",1),("T pendulum",2),
   ("physical pendulum",3),("w from k,m",4),
   ("w from T or f",5),("x(t)",6),
   ("v(t) and a(t)",7),("vmax amax",8),
   ("total SHM energy",9),("Back",0)])
  if c==0:return
  if c==1:m=gn("m");k=gn("k");show("T",2*pi*sqrt(m/k))
  elif c==2:L=gn("L");show("T",2*pi*sqrt(L/g))
  elif c==3:
   I=gn("I about pivot");m=gn("m");d=gn("d to cm")
   show("T",2*pi*sqrt(I/(m*g*d)))
  elif c==4:k=gn("k");m=gn("m");show("w",sqrt(k/m))
  elif c==5:
   if yes("Have T? (else f)"):
    T=gn("T");show("w",2*pi/T)
   else:
    f=gn("f");show("w",2*pi*f)
  elif c==6:
   A=gn("A");w=gn("w");t=gn("t");ph=gn("phi")
   show("x",A*cos(w*t+ph))
  elif c==7:
   A=gn("A");w=gn("w");t=gn("t");ph=gn("phi")
   show("v",-A*w*sin(w*t+ph))
   show("a",-A*w*w*cos(w*t+ph))
  elif c==8:
   A=gn("A");w=gn("w")
   show("vmax",A*w);show("amax",A*w*w)
  elif c==9:
   k=gn("k");A=gn("A");show("E",.5*k*A*A)

def grav():
 while True:
  c=menu("Gravitation",[
   ("F=GmM/r^2",1),("g=GM/r^2",2),
   ("U=-GMm/r",3),("v_orbit",4),
   ("T orbit Kepler",5),("v_escape",6),
   ("total orbit E",7),("Back",0)])
  if c==0:return
  if c==1:
   m1=gn("m1");m2=gn("m2");r=gn("r")
   show("F",GC*m1*m2/(r*r))
  elif c==2:
   M=gn("M");r=gn("r");show("g",GC*M/(r*r))
  elif c==3:
   m=gn("m");M=gn("M");r=gn("r")
   show("U",-GC*M*m/r)
  elif c==4:
   M=gn("M");r=gn("r");show("v_orb",sqrt(GC*M/r))
  elif c==5:
   M=gn("M");r=gn("r")
   show("T",2*pi*sqrt(r*r*r/(GC*M)))
  elif c==6:
   M=gn("M");r=gn("r");show("v_esc",sqrt(2*GC*M/r))
  elif c==7:
   m=gn("m");M=gn("M");r=gn("r")
   show("E",-GC*M*m/(2*r))

def calc():
 while True:
  c=menu("Calculus",[
   ("int F(t)dt = J",1),("int F(t) -> vf",2),
   ("int F(x)dx = W",3),("int F(t)v(t)dt",4),
   ("int a(t)dt = dv",5),("int v(t)dt = dx",6),
   ("d/du f(u) at t",7),("d2/du2 f(u) at t",8),
   ("U from F(x)",9),("F from U(x)",10),
   ("Back",0)])
  if c==0:return
  if c==1:
   e=ge("F(u)");t1=gn("t1");t2=gn("t2")
   show("J",nint(mkf(e),t1,t2))
  elif c==2:
   m=gn("m");v0=gn("v0")
   e=ge("F(u)");t1=gn("t1");t2=gn("t2")
   J=nint(mkf(e),t1,t2)
   show("J",J);show("vf",v0+J/m)
  elif c==3:
   e=ge("F(u)");x1=gn("x1");x2=gn("x2")
   show("W",nint(mkf(e),x1,x2))
  elif c==4:
   ef=ge("F(u)");ev=ge("v(u)")
   t1=gn("t1");t2=gn("t2")
   F=mkf(ef);V=mkf(ev)
   W=nint(lambda u:F(u)*V(u),t1,t2)
   show("W",W);show("Pavg",W/(t2-t1))
  elif c==5:
   v0=gn("v0");e=ge("a(u)")
   t1=gn("t1");t2=gn("t2")
   dv=nint(mkf(e),t1,t2)
   show("dv",dv);show("vf",v0+dv)
  elif c==6:
   x0=gn("x0");e=ge("v(u)")
   t1=gn("t1");t2=gn("t2")
   dx=nint(mkf(e),t1,t2)
   show("dx",dx);show("xf",x0+dx)
  elif c==7:
   e=ge("f(u)");t=gn("t");show("df/du",dfx(mkf(e),t))
  elif c==8:
   e=ge("f(u)");t=gn("t");show("d2f/du2",d2fx(mkf(e),t))
  elif c==9:
   e=ge("F(u)");x0=gn("x_ref");x=gn("x")
   show("U",-nint(mkf(e),x0,x))
  elif c==10:
   e=ge("U(u)");t=gn("x");show("F",-dfx(mkf(e),t))

def fit_xy():
 n=gi("n data pts")
 sx=sy=sxx=sxy=0
 for i in range(n):
  x=gn("x"+str(i+1));y=gn("y"+str(i+1))
  sx+=x;sy+=y;sxx+=x*x;sxy+=x*y
 den=n*sxx-sx*sx
 if den==0:print("bad data");return
 a=(n*sxy-sx*sy)/den
 b=(sy-a*sx)/n
 show("slope",a);show("intercept",b)

def frq25_q1():
 while True:
  c=menu("2025 Q1 collision",[
   ("momentum arrows",1),("Fmax formula",2),
   ("v1 formula",3),("Back",0)])
  if c==0:return
  if c==1:
   print("p1 before = +2*m*v0")
   print("p2 before = -6*m*v0")
   print("system before = -4*m*v0")
   print("after stuck: vf=-4*v0/7")
   print("system after = -4*m*v0")
  elif c==2:
   print("Use J=dp=int F(t)dt")
   print("dp block2 = 18*m*v0/7")
   print("int_0^tc Fmax*sin(A*t)dt")
   print("=Fmax*(1-cos(A*tc))/A")
   print("Fmax=18*m*v0*A/(7*(1-cos(A*tc)))")
  elif c==3:
   print("Conserve momentum:")
   print("m*v1-6*m*v0=7*m*vf")
   print("final speed v0 must be +x")
   print("v1=13*v0")

def frq25_q2():
 while True:
  c=menu("2025 Q2 springs",[
   ("energy bars",1),("v at x1/2",2),
   ("K graph friction",3),("larger mass graph",4),
   ("Back",0)])
  if c==0:return
  if c==1:
   print("At x=x1:")
   print("UA=.5*k*x1^2")
   print("UB=.5*(2k)*x1^2=k*x1^2")
   print("Kblock=0")
   print("bar ratio UA:UB:K = 1:2:0")
  elif c==2:
   print("Energy conserved.")
   print("Utotal=.5*k*x^2 + .5*(2k)*x^2")
   print("Utotal=(3/2)*k*x^2")
   print("K at x1/2 = (9/8)*k*x1^2")
   print("v=(3*abs(x1)/2)*sqrt(k/m)")
  elif c==3:
   print("K starts at 0, rises to max near x=0,")
   print("then returns to 0 at turning points.")
   print("With friction, each peak is smaller.")
   print("Same period T; graph dies to K=0.")
  elif c==4:
   print("Larger mass: spring period increases.")
   print("K peaks occur farther apart in time.")
   print("Friction force mu*m*g is larger,")
   print("so energy can be lost faster.")

def frq25_q3_mu():
 print("Use x_max vs h.")
 print("m*g*h = mu*m*g*x_max")
 print("x_max = h/mu, so slope=1/mu")
 if yes("Use AP table?"):
  hs=[.30,.45,.60,.75,.90]
  xs=[.76,1.10,1.40,1.90,2.30]
 else:
  n=gi("n data pts");hs=[];xs=[]
  for i in range(n):
   hs.append(gn("h"+str(i+1)))
   xs.append(gn("xmax"+str(i+1)))
 shx=sh2=0
 for i in range(len(hs)):
  shx+=hs[i]*xs[i];sh2+=hs[i]*hs[i]
 if sh2==0:print("bad data");return
 slope=shx/sh2
 show("slope x/h",slope)
 show("mu",1/slope)
 print("Equiv: graph h vs x, slope=mu.")

def frq25_q3():
 while True:
  c=menu("2025 Q3 experiment",[
   ("g linear graph",1),("rough graph vars",2),
   ("mu from data",3),("generic line fit",4),
   ("Back",0)])
  if c==0:return
  if c==1:
   print("Vary release height h.")
   print("Measure launch speed v with sensor.")
   print("Repeat/average each h.")
   print("Energy: m*g*h=.5*m*v^2")
   print("Graph y=v^2 vs x=h.")
   print("slope=2*g, so g=slope/2")
  elif c==2:
   print("Rough surface:")
   print("m*g*h = mu*m*g*x_max")
   print("Graph y=x_max vs x=h.")
   print("slope=1/mu, so mu=1/slope")
   print("Or graph y=h vs x=x_max; slope=mu.")
  elif c==3:frq25_q3_mu()
  elif c==4:fit_xy()

def frq25_q4():
 while True:
  c=menu("2025 Q4 rolling",[
   ("static f compare",1),("static f formula",2),
   ("kinetic f compare",3),("Back",0)])
  if c==0:return
  if c==1:
   print("fD < fR")
   print("Ring has larger I, so it needs")
   print("more torque to reduce rotation.")
  elif c==2:
   print("Use sumF=M*a, sumtau=I*alpha, a=R*alpha")
   print("For rolling up ramp, static f is up ramp.")
   print("f = M*g*sin(theta)*I/(I+M*R^2)")
  elif c==3:
   print("fD = fR")
   print("While slipping, fk=mu_k*N.")
   print("Same material, M, and theta -> same N")
   print("so same kinetic friction.")

def frq25():
 while True:
  c=menu("AP 2025 FRQ helpers",[
   ("Q1 collision",1),("Q2 springs",2),
   ("Q3 experiment",3),("Q4 rolling",4),
   ("Back",0)])
  if c==0:return
  if c==1:frq25_q1()
  elif c==2:frq25_q2()
  elif c==3:frq25_q3()
  elif c==4:frq25_q4()

def main():
 while True:
  print("")
  print("AP PHYS C MECH v2")
  print("SI units, radians")
  c=menu("Choose area",[
   ("Kinematics",1),("Forces",2),
   ("Energy/Work/Power",3),("Momentum",4),
   ("Rotation",5),("Oscillations",6),
   ("Gravitation",7),("Calculus tools",8),
   ("AP 2025 FRQ helpers",9),
   ("Quit",0)])
  if c==0:print("Done.");return
  if c==1:kin()
  elif c==2:force()
  elif c==3:energy()
  elif c==4:mom()
  elif c==5:rot()
  elif c==6:osc()
  elif c==7:grav()
  elif c==8:calc()
  elif c==9:frq25()

main()
