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

ALIASES={"mass":"m","velocity":"v","speed":"v","time":"t","dist":"d",
"distance":"d","height":"h","f":"F","force":"F","netforce":"Fnet",
"normal":"N","friction":"ffric","fric":"ffric","work":"W","theta":"theta",
"angle":"theta","fnet":"Fnet","wnc":"Wnc","winc":"Wnc","ki":"Ki",
"ui":"Ui","uf":"Uf","kf":"Kf","ug":"Ug","us":"Us","tspring":"Tspring",
"tpend":"Tpend","period":"T","omega":"omega","radius":"r","length":"L",
"muk":"mu","mukinetic":"mu","coefficient":"mu"}

def nk(k):
 r=k.replace("_","").replace(" ","").strip()
 if r in ("M","I","L","K","J","W","P","T"):return r
 lo=r.lower()
 return ALIASES.get(lo,r)

def add_knowns(ks,s):
 s=s.replace(";",",")
 for p in s.split(","):
  p=p.strip()
  if "=" in p:
   a,b=p.split("=",1)
   set_known(ks,a.strip(),b.strip())

def set_known(ks,k,v):
 if v=="":return
 if v.lower() in ("null","none","blank","?"):return
 try:ks[nk(k)]=float(eval(fixexpr(v),NAMES))
 except:ks[nk(k)]=fixexpr(v)

def req(ks,rs):
 for r in rs:
  if nk(r) not in ks:return False
 return True

def val(ks,k):return ks[nk(k)]

def put(ks,out,v,ans,why):
 if v!=v or v==float("inf") or v==-float("inf"):return
 out=nk(out)
 if out not in ks:
  ks[out]=v;ans.append((out,v,why))

def isnum(x):return type(x)==float or type(x)==int

def smart_eqs():
 return [
 ("a",("Fnet","m"),lambda k:val(k,"Fnet")/val(k,"m"),"a=Fnet/m"),
 ("Fnet",("m","a"),lambda k:val(k,"m")*val(k,"a"),"Fnet=m*a"),
 ("Fnet",("m","v","r"),lambda k:val(k,"m")*val(k,"v")**2/val(k,"r"),"centripetal net force"),
 ("v",("v0","a","t"),lambda k:val(k,"v0")+val(k,"a")*val(k,"t"),"v=v0+a*t"),
 ("x",("x0","v0","a","t"),lambda k:val(k,"x0")+val(k,"v0")*val(k,"t")+.5*val(k,"a")*val(k,"t")**2,"x=x0+v0*t+.5*a*t^2"),
 ("a",("x","x0","v0","t"),lambda k:2*(val(k,"x")-val(k,"x0")-val(k,"v0")*val(k,"t"))/val(k,"t")**2,"a=2*(x-x0-v0*t)/t^2"),
 ("v",("x","x0","v0","t"),lambda k:2*(val(k,"x")-val(k,"x0"))/val(k,"t")-val(k,"v0"),"v=2*(x-x0)/t-v0"),
 ("a",("v","v0","t"),lambda k:(val(k,"v")-val(k,"v0"))/val(k,"t"),"a=(v-v0)/t"),
 ("K",("m","v"),lambda k:.5*val(k,"m")*val(k,"v")**2,"K=.5*m*v^2"),
 ("v",("K","m"),lambda k:sqrt(2*val(k,"K")/val(k,"m")),"speed=sqrt(2K/m)"),
 ("p",("m","v"),lambda k:val(k,"m")*val(k,"v"),"p=m*v"),
 ("J",("Favg","dt"),lambda k:val(k,"Favg")*val(k,"dt"),"J=Favg*dt"),
 ("Favg",("J","dt"),lambda k:val(k,"J")/val(k,"dt"),"Favg=J/dt"),
 ("vf",("v0","J","m"),lambda k:val(k,"v0")+val(k,"J")/val(k,"m"),"vf=v0+J/m"),
 ("W",("F","d","theta"),lambda k:val(k,"F")*val(k,"d")*cos(val(k,"theta")),"W=F*d*cos(theta)"),
 ("F",("W","d","theta"),lambda k:val(k,"W")/(val(k,"d")*cos(val(k,"theta"))),"F=W/(d*cos(theta))"),
 ("P",("W","t"),lambda k:val(k,"W")/val(k,"t"),"P=W/t"),
 ("Ug",("m","y"),lambda k:val(k,"m")*g*val(k,"y"),"Ug=m*g*y"),
 ("Us",("k","x"),lambda k:.5*val(k,"k")*val(k,"x")**2,"Us=.5*k*x^2"),
 ("F",("k","x"),lambda k:-val(k,"k")*val(k,"x"),"spring force F=-kx"),
 ("ffric",("mu","N"),lambda k:val(k,"mu")*val(k,"N"),"friction force f=mu*N"),
 ("x",("Us","k"),lambda k:sqrt(2*val(k,"Us")/val(k,"k")),"spring x=sqrt(2Us/k)"),
 ("v",("m","k","x"),lambda k:val(k,"x")*sqrt(val(k,"k")/val(k,"m")),"spring speed from .5kx^2=.5mv^2"),
 ("d",("h","mu"),lambda k:val(k,"h")/val(k,"mu"),"stopping distance from mgh=mu*mg*d"),
 ("Kf",("Ki","Ui","Wnc","Uf"),lambda k:val(k,"Ki")+val(k,"Ui")+val(k,"Wnc")-val(k,"Uf"),"Kf=Ki+Ui+Wnc-Uf"),
 ("v",("Kf","m"),lambda k:sqrt(2*val(k,"Kf")/val(k,"m")),"speed from final K"),
 ("Tspring",("m","k"),lambda k:2*pi*sqrt(val(k,"m")/val(k,"k")),"T=2pi*sqrt(m/k)"),
 ("Tpend",("L",),lambda k:2*pi*sqrt(val(k,"L")/g),"T=2pi*sqrt(L/g)"),
 ("omega",("k","m"),lambda k:sqrt(val(k,"k")/val(k,"m")),"omega=sqrt(k/m)"),
 ("ac",("v","r"),lambda k:val(k,"v")**2/val(k,"r"),"a_c=v^2/r"),
 ("v",("omega","r"),lambda k:val(k,"omega")*val(k,"r"),"v=omega*r"),
 ("Krot",("I","omega"),lambda k:.5*val(k,"I")*val(k,"omega")**2,"Krot=.5*I*omega^2"),
 ("Lrot",("I","omega"),lambda k:val(k,"I")*val(k,"omega"),"L=I*omega"),
 ("vorb",("M","r"),lambda k:sqrt(GC*val(k,"M")/val(k,"r")),"v_orbit=sqrt(GM/r)"),
 ("vesc",("M","r"),lambda k:sqrt(2*GC*val(k,"M")/val(k,"r")),"v_esc=sqrt(2GM/r)"),
 ("vroll",("m","h","r","I"),lambda k:sqrt(2*g*val(k,"h")/(1+val(k,"I")/(val(k,"m")*val(k,"r")**2))),"rolling speed from height")]

def sym_eqs():
 return [
 ("a",("Fnet","m"),"Fnet/m","Newton 2nd law"),
 ("Fnet",("m","a"),"m*a","Newton 2nd law"),
 ("Fnet",("m","v","r"),"m*v^2/r","centripetal net force"),
 ("v",("v0","a","t"),"v0+a*t","constant acceleration"),
 ("x",("x0","v0","a","t"),"x0+v0*t+.5*a*t^2","constant acceleration"),
 ("a",("x","x0","v0","t"),"2*(x-x0-v0*t)/t^2","constant acceleration solved for acceleration"),
 ("v",("x","x0","v0","t"),"2*(x-x0)/t-v0","constant acceleration average velocity"),
 ("a",("v","v0","t"),"(v-v0)/t","constant acceleration solved for acceleration"),
 ("K",("m","v"),".5*m*v^2","kinetic energy"),
 ("v",("K","m"),"sqrt(2*K/m)","solve kinetic energy for speed"),
 ("p",("m","v"),"m*v","momentum"),
 ("J",("Favg","dt"),"Favg*dt","constant average force impulse"),
 ("Favg",("J","dt"),"J/dt","average force from impulse"),
 ("vf",("v0","J","m"),"v0+J/m","impulse-momentum"),
 ("W",("F","d","theta"),"F*d*cos(theta)","work by constant force"),
 ("F",("W","d","theta"),"W/(d*cos(theta))","force from work"),
 ("Ug",("m","y"),"m*g*y","gravitational potential"),
 ("Us",("k","x"),".5*k*x^2","spring potential"),
 ("F",("k","x"),"-k*x","spring force"),
 ("ffric",("mu","N"),"mu*N","friction force"),
 ("x",("Us","k"),"sqrt(2*Us/k)","solve spring energy for x"),
 ("v",("m","k","x"),"x*sqrt(k/m)","spring energy converted to kinetic energy"),
 ("d",("h","mu"),"h/mu","height energy lost to friction"),
 ("Kf",("Ki","Ui","Wnc","Uf"),"Ki+Ui+Wnc-Uf","energy conservation"),
 ("v",("Kf","m"),"sqrt(2*Kf/m)","speed from final kinetic energy"),
 ("Tspring",("m","k"),"2*pi*sqrt(m/k)","spring period"),
 ("Tpend",("L",),"2*pi*sqrt(L/g)","pendulum period"),
 ("omega",("k","m"),"sqrt(k/m)","spring angular frequency"),
 ("ac",("v","r"),"v^2/r","centripetal acceleration"),
 ("Krot",("I","omega"),".5*I*omega^2","rotational kinetic energy"),
 ("Lrot",("I","omega"),"I*omega","angular momentum"),
 ("vroll",("m","h","r","I"),"sqrt(2*g*h/(1+I/(m*r^2)))","rolling energy")]

VN={"m":"mass","M":"big mass","v":"speed/velocity","v0":"initial velocity",
"vf":"final velocity","a":"acceleration","t":"time","x":"position/stretch",
"x0":"initial position","d":"distance","h":"height","mu":"friction coeff",
"F":"force","Fnet":"net force","Favg":"average force","ffric":"friction force",
"N":"normal force","dt":"time interval",
"theta":"angle rad","W":"work","K":"kinetic energy","Ki":"initial K","Kf":"final K",
"Ui":"initial U","Uf":"final U","Wnc":"nonconservative work","Ug":"grav U",
"Us":"spring U","k":"spring constant","p":"momentum","J":"impulse",
"I":"rot inertia","omega":"angular speed","r":"radius","L":"length"}

VG=[("motion",("m","v0","v","a","t","x0","x","Fnet")),
("energy",("m","v","K","Ki","Ui","Wnc","Uf","h","mu","d","k","x","Us")),
("momentum",("m","v","v0","vf","p","J","Favg","dt")),
("rotation",("I","omega","r","m","h")),
("osc/grav",("m","k","L","M","r"))]

def sym_solve(ks):
 out=[]
 have={}
 for k in ks:have[k]=1
 for _ in range(5):
  n=len(out)
  for v,rs,f,why in sym_eqs():
   vv=nk(v)
   if vv not in have and req(have,rs):
    have[vv]=1;out.append((vv,f,why))
  if len(out)==n:break
 return out

def solve_knowns(ks):
 ans=[]
 for _ in range(6):
  n=len(ans)
  for out,rs,fn,why in smart_eqs():
   if nk(out) not in ks and req(ks,rs):
    try:put(ks,out,fn(ks),ans,why)
    except:pass
  if len(ans)==n:break
 if ans:
  print("Can calculate:")
  for a,b,w in ans:print(a+" = "+str(b)+"  from "+w)
 else:
  print("No new numeric values.")
 sym=sym_solve(ks)
 if sym:
  print("Formula paths:")
  for a,f,w in sym:print(a+" = "+f+"  from "+w)
 print("Known now:")
 for k in sorted(ks):print(k+" = "+str(ks[k]))

def smart_quick():
 print("Enter knowns like m=5,v0=0,a=2")
 print("Symbols are ok too: mass=m,k=k,x=x")
 print("Use Wnc for nonconservative work.")
 ks={}
 while True:
  try:s=input("knowns blank=solve: ").strip()
  except EOFError:break
  if s=="":break
  add_knowns(ks,s)
 solve_knowns(ks)

def smart_guided():
 c=menu("Which variables?",[
  ("motion",0),("energy",1),("momentum",2),
  ("rotation",3),("osc/grav",4),("all common",5),
  ("Back",99)])
 if c==99:return
 if c==5:
  vs=[]
  for _,g in VG:
   for v in g:
    if v not in vs:vs.append(v)
 else:vs=list(VG[c][1])
 print("Enter a number, a symbol like m, or blank if unknown.")
 ks={}
 for v in vs:
  try:s=input(v+" "+VN.get(v,"")+": ").strip()
  except EOFError:break
  if s!="":set_known(ks,v,s)
 solve_knowns(ks)

def smart_num():
 while True:
  c=menu("Knowns solver",[
   ("guided variable list",1),("quick knowns line",2),
   ("Back",0)])
  if c==0:return
  if c==1:smart_guided()
  elif c==2:smart_quick()

def same_rs(a,b):
 if len(a)!=len(b):return False
 for i in range(len(a)):
  if nk(a[i])!=nk(b[i]):return False
 return True

def compute_eq(out,rs,ks):
 for o,r,fn,_ in smart_eqs():
  if nk(o)==nk(out) and same_rs(r,rs):
   for x in r:
    if not isnum(val(ks,x)):return None
   try:return fn(ks)
   except:return None
 return None

def target_match(target,out):
 target=nk(target);out=nk(out)
 if target==out:return True
 if target=="F" and out in ("Fnet","Favg","ffric"):return True
 if target=="T" and out in ("Tspring","Tpend"):return True
 return False

def need_text(rs):
 s=[]
 for r in rs:s.append(nk(r))
 return ",".join(s)

def choose_target_eq(v):
 opts=[]
 for e in sym_eqs():
  if target_match(v,e[0]):
   opts.append((e[3]+": "+e[0]+"="+e[2]+"  need "+need_text(e[1]),e))
 if not opts:return None
 opts.append(("Back",0))
 return menu("Path for "+v,opts)

def ask_given(ks,v):
 s=input(v+" "+VN.get(v,"")+" blank=solve: ").strip()
 if s!="":
  if "=" in s:add_knowns(ks,s)
  else:set_known(ks,v,s)
  return True
 return False

def solve_target_var(v,ks,depth):
 v=nk(v)
 if v in ks:return True
 if depth>4:print("too deep");return False
 e=choose_target_eq(v)
 if e==0 or e==None:
  print("No path for "+v);return False
 out,rs,form,why=e
 for r in rs:
  rr=nk(r)
  if rr not in ks:
   if not ask_given(ks,rr):
    print("Trying to find "+rr+" first...")
    if not solve_target_var(rr,ks,depth+1):return False
 num=compute_eq(out,rs,ks)
 print("")
 print("Use "+why)
 print(out+" = "+form)
 oo=nk(out)
 if num!=None:
  ks[oo]=num;print(out+" = "+str(num))
 else:
  ks[oo]=form;print(out+" = "+form)
 if oo!=v:ks[v]=ks[oo]
 return True

def smart_target():
 ks={}
 print("Examples: v, a, x, F/force, W, K, p, T/period")
 target=nk(input("What variable do you want? ").strip())
 if target=="":return
 print("If a needed value is unknown, press Enter.")
 if solve_target_var(target,ks,0):
  print("")
  print("Result:")
  print(target+" = "+str(ks.get(target,"?")))
  print("Knowns used:")
  for k in sorted(ks):print(k+" = "+str(ks[k]))

def has_any(s,ws):
 for w in ws:
  if w in s:return True
 return False

def print_path(title,lines):
 print("")
 print(title)
 for l in lines:print(l)

def clean(s):
 s=s.lower().replace(" ","").replace("*","")
 s=s.replace("sqrt","r").replace("omega","w")
 return s

def has_all(s,ws):
 for w in ws:
  if w not in s:return False
 return True

def smart_back():
 print("Paste the answer you were given.")
 print("Then describe the situation in a few words.")
 ans=clean(input("answer formula: "))
 giv=input("problem type optional: ").lower()
 s=ans+" "+giv
 hits=0
 if "h/mu" in ans or "h/muk" in ans:
  hits+=1;print_path("How to show: d = h/mu",[
  "This is a height-to-friction stopping problem.",
  "Start with energy: gravitational energy becomes work done by friction.",
  "Write: m*g*h = mu_k*m*g*d",
  "Cancel m and g on both sides.",
  "You get h = mu_k*d, so d = h/mu_k."])
 if has_all(ans,("x","r(k/m)")) or has_all(ans,("x","r(k","m)")):
  hits+=1;print_path("How to show: v = x*sqrt(k/m)",[
  "This is spring potential energy becoming kinetic energy.",
  "Start with conservation of energy: spring energy = kinetic energy.",
  "Write: .5*k*x^2 = .5*m*v^2",
  "Cancel .5, divide by m, then square root.",
  "You get v = x*sqrt(k/m)."])
 if has_all(ans,("r(2","k","m")) or has_all(ans,("r(2k","m")):
  hits+=1;print_path("How to show: v = sqrt(2K/m)",[
  "Start with kinetic energy.",
  "Write: K = .5*m*v^2",
  "Multiply both sides by 2: 2K = m*v^2",
  "Divide by m and square root.",
  "Use a sign only if the problem asks for velocity direction."])
 if "2pi" in ans and "r(m/k)" in ans:
  hits+=1;print_path("How to show: T = 2*pi*sqrt(m/k)",[
  "This is a mass-spring period result.",
  "Use omega = sqrt(k/m).",
  "Period and angular frequency are related by T = 2*pi/omega.",
  "Substitute omega and simplify.",
  "You get T = 2*pi*sqrt(m/k)."])
 if "2pi" in ans and "r(l/g)" in ans:
  hits+=1;print_path("How to show: T = 2*pi*sqrt(L/g)",[
  "This is a small-angle pendulum period result.",
  "Use omega = sqrt(g/L).",
  "Period and angular frequency are related by T = 2*pi/omega.",
  "Substitute omega and simplify.",
  "You get T = 2*pi*sqrt(L/g)."])
 if has_all(ans,("r(2gh","1+i")) or "vroll" in giv:
  hits+=1;print_path("How to show: rolling speed from height",[
  "This is energy with both translation and rotation.",
  "Start with mgh = .5*m*v^2 + .5*I*w^2",
  "For rolling without slipping, w = v/R.",
  "Substitute to get mgh = .5*(m+I/R^2)*v^2",
  "Solve for v: sqrt(2gh/(1+I/(mR^2)))."])
 if "fmax" in ans or ("j" in ans and "cos" in ans):
  hits+=1;print_path("How to show: force pulse maximum",[
  "This is an impulse problem.",
  "Impulse equals area under the force-time graph: J = int F(t)dt.",
  "If F = Fmax*sin(A*t), integrate from 0 to T.",
  "J = Fmax*(1-cos(A*T))/A",
  "Solve for Fmax: A*J/(1-cos(A*T))."])
 if "vf" in ans and ("/" in ans or "m1" in ans):
  hits+=1;print_path("How to show: stuck-together collision speed",[
  "This is conservation of momentum.",
  "Before collision: total momentum is m1*v1i + m2*v2i.",
  "After they stick: total mass is (m1+m2) moving at vf.",
  "Write m1*v1i + m2*v2i = (m1+m2)*vf.",
  "Divide by (m1+m2)."])
 if hits==0:
  smart_deriv()

def smart_deriv():
 giv=input("givens/keywords: ").lower()
 goal=input("goal: ").lower()
 s=giv+" "+goal
 hits=0
 if has_any(s,("collision","momentum","impulse","force time","change momentum","vf")):
  hits+=1;print_path("Momentum/Impulse",[
  "Choose + direction.",
  "If external impulse is zero: sum p_i=sum p_f.",
  "For impulse: J=int F(t)dt=m*(vf-vi).",
  "If objects stick: m1v1i+m2v2i=(m1+m2)vf."])
 if has_any(s,("energy","spring","speed","height","friction","work","kinetic")):
  hits+=1;print_path("Energy",[
  "Start: Ki+Ui+W_nc=Kf+Uf.",
  "Use Ug=mgy and Us=.5kx^2.",
  "Friction work usually W_f=-mu_k*N*d.",
  "Solve .5*m*v^2=remaining energy."])
 if has_any(s,("graph","experiment","slope","linear","linearize","mu","gravity")):
  hits+=1;print_path("Experiment/Graph",[
  "Rearrange into y=slope*x+b.",
  "For drop to speed: v^2=(2g)h, slope=2g.",
  "For rough stopping: h=mu_k*d, slope=mu_k.",
  "Use repeated trials and average."])
 if has_any(s,("roll","rolling","disk","sphere","hoop","torque","static")):
  hits+=1;print_path("Rolling",[
  "No slip: v=R*omega and a=R*alpha.",
  "Energy: mgh=.5mv^2+.5Iomega^2.",
  "Or use sumF=ma and sumtau=Ialpha.",
  "Larger I/(mR^2) means less translational speed."])
 if has_any(s,("period","pendulum","oscillation","shm","frequency")):
  hits+=1;print_path("Oscillation",[
  "Spring: T=2pi*sqrt(m/k).",
  "Pendulum: T=2pi*sqrt(L/g).",
  "Use proportional reasoning for MCQ changes.",
  "Mass affects spring period, not simple pendulum period."])
 if hits==0:
  print("Try keywords like energy, momentum, graph, rolling, period.")

def smart():
 while True:
  c=menu("Smart solver",[
   ("all from givens",1),("solve one target",2),
   ("derivation",3),("backward proof",4),
   ("Back",0)])
  if c==0:return
  if c==1:smart_num()
  elif c==2:smart_target()
  elif c==3:smart_deriv()
  elif c==4:smart_back()

def deriv_mom():
 while True:
  c=menu("Momentum deriv",[
   ("collision setup",1),("stick together vf",2),
   ("impulse from F(t)",3),("sin pulse Fmax",4),
   ("Back",0)])
  if c==0:return
  if c==1:
   print("Choose + direction first.")
   print("p_before=sum(m_i*v_i)")
   print("p_after=sum(m_i*v_fi)")
   print("If external impulse=0:")
   print("p_before=p_after")
   print("Keep signs on velocities.")
  elif c==2:
   print("For a perfectly inelastic collision:")
   print("m1*v1i + m2*v2i = (m1+m2)*vf")
   print("vf=(m1*v1i+m2*v2i)/(m1+m2)")
  elif c==3:
   print("Impulse is area under F-t graph.")
   print("J=int F(t)dt = dp")
   print("For one object: J=m*(vf-vi)")
   print("For a system, internal forces cancel.")
  elif c==4:
   print("If F(t)=Fmax*sin(A*t), 0 to T:")
   print("J=Fmax*(1-cos(A*T))/A")
   print("Fmax=A*J/(1-cos(A*T))")
   print("Use J=needed change in momentum.")

def deriv_energy():
 while True:
  c=menu("Energy deriv",[
   ("conservation setup",1),("many springs",2),
   ("solve speed symbolically",3),("friction graphs",4),
   ("Back",0)])
  if c==0:return
  if c==1:
   print("Write all energy terms:")
   print("Ki+Ug_i+Us_i+W_nc = Kf+Ug_f+Us_f")
   print("Ug=m*g*y")
   print("Us=.5*k*x^2")
   print("W_nc is + added, - removed.")
  elif c==2:
   print("Add spring energies.")
   print("Us_total=sum(.5*k_i*x_i^2)")
   print("If same displacement x:")
   print("Us_total=.5*(sum k_i)*x^2")
   print("This acts like k_eff=sum k_i.")
  elif c==3:
   print("After moving terms:")
   print("Kf=Ki+Ui+W_nc-Uf")
   print(".5*m*v^2=Kf")
   print("v=+/-sqrt(2*Kf/m)")
   print("Sign comes from direction.")
  elif c==4:
   print("Friction removes mechanical energy:")
   print("W_f=-mu_k*N*d")
   print("K graph peaks shrink over time.")
   print("Turning points have K=0.")
   print("Bigger m -> bigger fk if N=m*g.")

def deriv_exp():
 while True:
  c=menu("Experiment deriv",[
   ("linearize steps",1),("find g graph",2),
   ("find mu graph",3),("line fit",4),
   ("Back",0)])
  if c==0:return
  if c==1:
   print("1 choose independent variable x")
   print("2 choose measured dependent y")
   print("3 rearrange to y=slope*x+b")
   print("4 constant wanted is in slope")
   print("5 repeat trials and average")
  elif c==2:
   print("Energy drop to kinetic:")
   print("m*g*h=.5*m*v^2")
   print("v^2 = (2g)*h")
   print("Graph y=v^2 vs x=h.")
   print("slope=2g, so g=slope/2.")
  elif c==3:
   print("Energy lost to rough surface:")
   print("m*g*h = mu_k*m*g*d")
   print("h = mu_k*d")
   print("Graph y=h vs x=d.")
   print("slope=mu_k.")
  elif c==4:fit_xy()

def deriv_roll():
 while True:
  c=menu("Rolling deriv",[
   ("rolling energy",1),("incline equations",2),
   ("compare shapes",3),("static vs kinetic f",4),
   ("Back",0)])
  if c==0:return
  if c==1:
   print("No slip: v=R*w")
   print("Ktotal=.5*m*v^2+.5*I*w^2")
   print("Ktotal=.5*(m+I/R^2)*v^2")
   print("Use with mgh or spring energy.")
  elif c==2:
   print("Use signs along incline.")
   print("sumF_parallel = m*a")
   print("sumtau_cm = I*alpha")
   print("no slip: a=R*alpha")
   print("Solve these three together.")
  elif c==3:
   print("Larger I/(mR^2):")
   print("- smaller translational speed")
   print("- smaller acceleration down ramp")
   print("- more energy in rotation")
   print("Ring > disk > solid sphere in I factor.")
  elif c==4:
   print("Static friction adjusts; f_s <= mu_s*N.")
   print("It can be up or down ramp.")
   print("Kinetic slipping: f_k=mu_k*N.")
   print("For same m, theta, surface: same f_k.")

def deriv_mcq():
 while True:
  c=menu("MCQ deriv checks",[
   ("units",1),("limits",2),("signs",3),
   ("proportions",4),("Back",0)])
  if c==0:return
  if c==1:
   print("Check dimensions before calculating.")
   print("Energy: kg*m^2/s^2")
   print("Momentum: kg*m/s")
   print("Torque: N*m")
  elif c==2:
   print("Try simple limits:")
   print("m->0, k->0, mu->0, I->0")
   print("Bad formulas often fail limits.")
  elif c==3:
   print("Choose positive direction.")
   print("Velocity, momentum, force can be signed.")
   print("Speed, mass, energy magnitudes are nonnegative.")
  elif c==4:
   print("Use proportional reasoning:")
   print("K~v^2, Us~x^2, Ug~h")
   print("T_spring~sqrt(m/k)")
   print("T_pend~sqrt(L/g)")

def deriv():
 while True:
  c=menu("Derivation helpers",[
   ("momentum/impulse",1),("energy/springs",2),
   ("experiments/graphs",3),("rolling/friction",4),
   ("MCQ checks",5),
   ("Back",0)])
  if c==0:return
  if c==1:deriv_mom()
  elif c==2:deriv_energy()
  elif c==3:deriv_exp()
  elif c==4:deriv_roll()
  elif c==5:deriv_mcq()

def fullmenus():
 while True:
  print("")
  c=menu("Full equation menus",[
   ("Kinematics",1),("Forces",2),
   ("Energy/Work/Power",3),("Momentum",4),
   ("Rotation",5),("Oscillations",6),
   ("Gravitation",7),("Calculus tools",8),
   ("Derivation helpers",9),
   ("Back",0)])
  if c==0:return
  if c==1:kin()
  elif c==2:force()
  elif c==3:energy()
  elif c==4:mom()
  elif c==5:rot()
  elif c==6:osc()
  elif c==7:grav()
  elif c==8:calc()
  elif c==9:deriv()

def main():
 while True:
  print("")
  print("AP PHYS C MECH v3")
  print("SI units, radians")
  c=menu("Choose mode",[
   ("Smart solver",1),("Full equation menus",2),
   ("Quit",0)])
  if c==0:print("Done.");return
  if c==1:smart()
  elif c==2:fullmenus()

main()
