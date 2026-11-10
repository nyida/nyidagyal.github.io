"""Build exact, downloadable scientific SVG plates from plate-data.json.
Run extraction first: node --import tsx public/research/figures/extract-data.ts
Then: python public/research/figures/generate.py
No benchmark values are hand-entered. Schematic values are declared below.
"""
from pathlib import Path
import json, math, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap, Normalize, to_rgb

ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'plate-data.json').read_text())
INK='#182733'; MUTED='#5e6b75'; GRID='#dce2e6'; BODY='#397331'; HEAD='#214d27'; GOLD='#c79235'; RED='#c63832'; WALL='#d1d7dc'; PURPLE='#755e9e'
HEAT=LinearSegmentedColormap.from_list('expansion',['#f5faf0','#d1e9bc','#90c66b','#558b3a','#254d27'])
DIV=LinearSegmentedColormap.from_list('signed',['#3c7631','#e6f0de','#ffffff','#f7e5e1','#bd3c35'])
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':INK,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED,'axes.edgecolor':'#7e8b95','axes.linewidth':.7,'svg.fonttype':'path','figure.facecolor':'white','savefig.facecolor':'white','mathtext.fontset':'dejavuserif','axes.spines.top':False,'axes.spines.right':False})
PREVIEW=Path(os.environ['SNAKEGUIDE_FIGURE_PREVIEWS']).expanduser() if os.environ.get('SNAKEGUIDE_FIGURE_PREVIEWS') else None
if PREVIEW is not None: PREVIEW.mkdir(parents=True, exist_ok=True)

def label_color(background):
 # Use the rendered cell color, not a numeric threshold, to preserve text contrast.
 def luminance(color):
  rgb=to_rgb(color)
  return sum(w*(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4) for c,w in zip(rgb,[.2126,.7152,.0722]))
 lum=luminance(background)
 if 1.05/(lum+.05)>=4.5:return 'white'
 return INK if (lum+.05)/(luminance(INK)+.05)>=4.5 else '#000000'

def header(fig,title,sub):
 fig.text(.045,.958,title,fontsize=18,fontfamily='DejaVu Serif',weight='normal',va='top')
 fig.text(.045,.904,sub,fontsize=9.6,color=MUTED,va='top')

def panel(ax,letter,title,sub=None):
 ax.set_title(f'({letter})  {title}',loc='left',fontsize=11.3,fontweight='bold',pad=16,color=INK)
 if sub: ax.text(0,1.035,sub,transform=ax.transAxes,fontsize=8.6,color=MUTED,va='bottom')

def save(fig,name,title,desc):
 fig.savefig(ROOT/f'{name}.svg',format='svg',metadata={'Title':title,'Description':desc,'Creator':'SnakeGuide scientific figure generator'})
 svg=ROOT/f'{name}.svg'
 svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
 if PREVIEW is not None: fig.savefig(PREVIEW/f'{name}.png',dpi=115)
 plt.close(fig)

def xy(p): return p['x'],p['y']
def board(ax,w,h,walls=(),values=None,cmap=HEAT,vmin=0,vmax=1,labels=False):
 ws=set(walls);ax.set_xlim(-.5,w-.5);ax.set_ylim(h-.5,-.5);ax.set_aspect('equal')
 for y in range(h):
  for x in range(w):
   k=f'{x},{y}';fill='#fafbfc'
   if k in ws:fill=WALL
   elif values is not None and k in values:fill=cmap((values[k]-vmin)/(vmax-vmin or 1))
   ax.add_patch(Rectangle((x-.5,y-.5),1,1,facecolor=fill,edgecolor='white',linewidth=1,zorder=0))
   if k in ws:ax.plot([x-.18,x+.18],[y-.18,y+.18],color='#a7b1b9',lw=.7)
   if labels and values is not None and k in values:ax.text(x,y,str(values[k]),ha='center',va='center',fontsize=7,color=INK)
 ax.set_xticks(range(w));ax.set_yticks(range(h));ax.tick_params(length=0,labelsize=8,pad=5)
 for s in ax.spines.values():s.set_visible(False)
 ax.set_xlabel('column x',fontsize=9,labelpad=8);ax.set_ylabel('row y',fontsize=9,labelpad=5)

def body(ax,b,order=True):
 pts=np.array([xy(p) for p in b]);ax.plot(pts[:,0],pts[:,1],color=BODY,lw=15,solid_capstyle='round',solid_joinstyle='round',zorder=3)
 for i,(x,y) in enumerate(pts):
  ax.add_patch(Circle((x,y),.24,fc=HEAD if i==0 else BODY,ec='white',lw=.8,zorder=4))
  if order:ax.text(x,y,str(i),ha='center',va='center',fontsize=9,color='white',weight='bold',zorder=5)

def marker(ax,p,label,color):
 x,y=xy(p);ax.add_patch(Circle((x,y),.28,fc=color,ec='white',lw=1,zorder=8));ax.text(x,y,label,ha='center',va='center',fontsize=9,color='white',weight='bold',zorder=9)

def footer(fig,text):fig.text(.045,.045,text,fontsize=9.1,color=MUTED,va='bottom',linespacing=1.5)

# 1. Real transition outputs. The three panels share the same initial ordered body.
def state_plate():
 fig=plt.figure(figsize=(12,5.65));header(fig,'State is an ordered chain, not an occupancy mask','Exact engine transitions · immediate growth · body index 0 is the head')
 gs=fig.add_gridspec(1,3,left=.055,right=.975,bottom=.25,top=.79,wspace=.24)
 states=[D['state']['before'],D['state']['tailEntry'],D['state']['growth']]
 titles=['Before the move','Enter the vacating tail','Eat and retain the tail']
 for i,(st,title) in enumerate(zip(states,titles)):
  ax=fig.add_subplot(gs[0,i]);board(ax,8,6);body(ax,st['body']);panel(ax,chr(97+i),title)
  if i==0:
   ax.add_patch(Rectangle((3-.44,2-.44),.88,.88,fill=False,ec=GOLD,lw=2,zorder=7))
   ax.annotate('tail: index 3',xy=(3,2),xytext=(4.15,.85),fontsize=8.5,color='#916a24',arrowprops={'arrowstyle':'-','color':GOLD,'lw':1.1},zorder=10)
   ax.annotate('',xy=(3,2.4),xytext=(3,2.7),arrowprops={'arrowstyle':'-|>','color':HEAD,'lw':2},zorder=10)
  if i==1:
   ax.annotate('old tail → new head',xy=(3,2),xytext=(4.05,.85),fontsize=8.5,color=HEAD,arrowprops={'arrowstyle':'-','color':HEAD,'lw':1.1},zorder=10)
  if i==2:
   ax.annotate('food consumed',xy=(4,3),xytext=(4.3,1.15),fontsize=8.5,color=HEAD,arrowprops={'arrowstyle':'-','color':HEAD,'lw':1.1},zorder=10)
  ax.text(.5,-.25,['length = 4','length = 4  ·  tail released','length = 5  ·  tail retained'][i],transform=ax.transAxes,ha='center',fontsize=10.2,fontweight='bold',color=HEAD if i else INK)
 footer(fig,'The occupied cells can remain unchanged while body order changes. On a growing move, the old tail remains occupied.\nThe two successors use different inputs: upward without food (b), rightward into food (c).')
 save(fig,'state-order','Ordered body and exact transitions','Three exact engine states: before, legal tail entry, and immediate growth. No performance experiment.')

# 2. Actual trace search, seed 2031, common expansion-order scale.
def search_plate():
 q=D['search'];fig=plt.figure(figsize=(12,6.1));header(fig,'Same board. Different objective and search effort.','Computed search traces · seed 2031 · 10 × 8 grid · terrain entry cost 5, other moves cost 1')
 gs=fig.add_gridspec(1,3,left=.055,right=.965,bottom=.28,top=.785,wspace=.23)
 maxrank=max(len(t['frames']) for t in q['traces'].values());axes=[]
 for i,(alg,tr) in enumerate(q['traces'].items()):
  ax=fig.add_subplot(gs[0,i]);axes.append(ax)
  vals={f"{f['current']['x']},{f['current']['y']}":j+1 for j,f in enumerate(tr['frames'])}
  board(ax,10,8,q['walls'],vals,vmin=1,vmax=maxrank);panel(ax,chr(97+i),alg)
  for k in q['terrain']:
   x,y=map(int,k.split(','));ax.plot(x+.28,y-.28,marker='^',ms=3.8,color=GOLD,zorder=6)
  pts=np.array([xy(p) for p in tr['path']]);ax.plot(pts[:,0],pts[:,1],color='white',lw=4.3,zorder=4);ax.plot(pts[:,0],pts[:,1],color=RED,lw=2,zorder=5)
  marker(ax,q['start'],'S',HEAD);marker(ax,q['goal'],'G',RED)
  ax.text(.5,-.25,f"{tr['steps']} moves    cost {tr['cost']}    {len(tr['frames'])} expanded",transform=ax.transAxes,ha='center',fontsize=9.6,fontweight='bold')
 cax=fig.add_axes([.32,.173,.35,.023]);cb=fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(1,maxrank),cmap=HEAT),cax=cax,orientation='horizontal');cb.set_label('Expansion order (shared scale)',fontsize=9,labelpad=2);cb.ax.tick_params(labelsize=8,length=2);cb.outline.set_visible(False)
 fig.text(.057,.185,'▲  terrain cost 5',fontsize=9,color='#916a24');fig.text(.75,.185,'red line = returned route',fontsize=9,color=RED)
 footer(fig,'BFS minimizes moves; Dijkstra and A* minimize weighted cost. A* uses Manhattan distance.\nThese are static graph traces, not claims about Snake survival. White cells were not expanded before the goal was reached.')
 save(fig,'search-landscape','Search cost and expansion landscapes','Exact BFS, Dijkstra and A* traces on benchmark seed 2031. All panel values come from the current engine.')

# 3. Cycle construction and occupancy over exact engine transitions.
def cycle_plate():
 c=D['cycle'];fig=plt.figure(figsize=(12,6));header(fig,'A spatial route becomes a temporal invariant','Exact cycle construction and engine replay · 60 vertices · body length 10 · no growth in the shown interval')
 ax=fig.add_axes([.055,.30,.43,.47]);idx={f"{p['x']},{p['y']}":i for i,p in enumerate(c['path'])};board(ax,10,6,values=idx,vmin=0,vmax=59,cmap=HEAT)
 panel(ax,'a','One cyclic ordering of the grid');pts=np.array([xy(p) for p in c['path']+[c['path'][0]]]);ax.plot(pts[:,0],pts[:,1],color='#6c8f50',lw=1.05,zorder=2)
 body(ax,c['states'][0]['body'],order=False)
 marker(ax,c['path'][15],'H',HEAD);marker(ax,c['path'][6],'T',BODY)
 for j in [0,9,16,23,32,41,50,59]:
  x,y=xy(c['path'][j]);ax.text(x,y,str(j),ha='center',va='center',fontsize=7.7,color=label_color(BODY if 6<=j<=15 else HEAT(j/59)),zorder=6)
 ax.text(.5,-.23,'tail index 6  →  head index 15  →  next index 16',transform=ax.transAxes,ha='center',fontsize=9.3)
 ax2=fig.add_axes([.57,.36,.38,.40]);occ=np.zeros((9,24));
 for t,st in enumerate(c['states']):
  for p in st['body']:
   j=idx[f"{p['x']},{p['y']}"]
   if j<24:occ[t,j]=1
 ax2.imshow(occ,origin='upper',aspect='auto',cmap=LinearSegmentedColormap.from_list('body',['#f5f8ef','#5c923e']),vmin=0,vmax=1,extent=(-.5,23.5,8.5,-.5))
 ax2.set_xticks([0,6,10,15,20,23]);ax2.set_yticks(range(9));ax2.set_xlabel('cycle index (first 24 of 60 vertices)',fontsize=9);ax2.set_ylabel('time step t',fontsize=9);panel(ax2,'b','The occupied interval moves forward')
 ax2.plot(np.arange(9)+15,np.arange(9),color=HEAD,marker='o',ms=4,lw=1.4,label='head');ax2.plot(np.arange(9)+6,np.arange(9),color=BODY,marker='s',ms=3.6,lw=1.2,label='tail');ax2.legend(frameon=False,loc='upper left',bbox_to_anchor=(0,-.2),ncol=2,fontsize=9)
 fig.text(.58,.20,'next(i) = (i + 1) mod 60',fontsize=14,fontfamily='DejaVu Serif',color=HEAD)
 footer(fig,'Following the cycle preserves a contiguous body interval until the board fills. The spatial and temporal panels show the same states.\nThis certificate assumes a compatible initial body, fixed obstacles, and the specified growth rules; it does not cover arbitrary wall insertion.')
 save(fig,'cycle-invariant','Hamiltonian cyclic-order invariant','Engine-generated 60-cell cycle and a time-by-cycle-index occupancy map from eight legal nongrowing moves.')

# 4. Connected components computed from exact fixed terrain.
def connectivity_plate():
 q=D['connection'];fig=plt.figure(figsize=(12,5.9));header(fig,'A one-cell cut changes the reachable region','Exact flood-fill on a frozen terrain graph · start S = (2, 3) · removed passage = (5, 3)')
 gs=fig.add_gridspec(1,3,left=.055,right=.965,bottom=.30,top=.79,wspace=.28,width_ratios=[1,1,.85])
 for i,k in enumerate(['open','closed']):
  ax=fig.add_subplot(gs[0,i]);vals={f"{p['x']},{p['y']}":1 for p in q[k]['reachable']};board(ax,10,7,q[k]['walls'],vals,cmap=LinearSegmentedColormap.from_list('reach',['white','#c1dfa4']),vmax=1)
  if k=='closed':
   for p in q[k]['right']:
    x,y=xy(p);ax.add_patch(Rectangle((x-.5,y-.5),1,1,fc='#e5e3ee',ec='white',lw=1,zorder=1))
  marker(ax,q['start'],'S',HEAD);ax.add_patch(Rectangle((4.56,2.56),.88,.88,fill=False,ec=RED if i else GOLD,lw=2,zorder=5));panel(ax,chr(97+i),['Passage open','Passage removed'][i]);ax.text(.5,-.24,['1 component · 64 reachable','2 components · 35 reachable'][i],transform=ax.transAxes,ha='center',fontsize=9.5,fontweight='bold')
 ax=fig.add_subplot(gs[0,2]);counts=[len(q['open']['reachable']),len(q['closed']['reachable'])];ax.bar([0,1],counts,width=.52,color=[HEAD,BODY],alpha=.87,zorder=3);ax.set_xticks([0,1],['Open','Removed']);ax.set_ylim(0,75);ax.set_yticks([0,20,40,60]);ax.set_ylabel('Cells reachable from S');ax.grid(axis='y',color=GRID,lw=.6,zorder=0);panel(ax,'c','Reachability loss')
 for x,n in enumerate(counts):ax.text(x,n+1.5,str(n),ha='center',fontsize=12,fontweight='bold')
 ax.annotate('−29 cells',xy=(1,49),xytext=(.5,66),ha='center',fontsize=10,color=RED,arrowprops={'arrowstyle':'->','color':RED,'lw':1.2})
 fig.text(.08,.19,'Reachable from S',color=HEAD,fontsize=9.5);fig.text(.3,.19,'Other component',color=PURPLE,fontsize=9.5);fig.text(.51,.19,'Walls / removed passage',color=MUTED,fontsize=9.5)
 footer(fig,'The removed vertex is an articulation point: deleting it separates the free-space graph. The lost reachable set includes the deleted cell.\nThis is a connectivity statement about a fixed snapshot. Moving-body release times require a richer model.')
 save(fig,'connectivity-cut','Articulation vertex and reachable components','Exact open and closed passage graphs and reachable counts 64 and 35, calculated by flood-fill.')

# 5. A declared finite analytical example, not a measured learning trajectory.
def reward_plate():
 gamma=.9;phi=np.array([-6.,-5.,-4.,-3.,-2.,0.]);n=5;terms=np.zeros((n,n+1))
 for t in range(n):terms[t,t]=-gamma**t*phi[t];terms[t,t+1]=gamma**(t+1)*phi[t+1]
 total=terms.sum(0);assert np.allclose(total,[6,0,0,0,0,0]);local=gamma*phi[1:]-phi[:-1]
 fig=plt.figure(figsize=(12,6));header(fig,'Potential shaping: local rewards, one boundary term','Analytical example · γ = 0.90 · Φ = [−6, −5, −4, −3, −2, 0] · terminal potential is zero')
 ax=fig.add_axes([.075,.32,.33,.44]);ax.plot(range(6),phi,color=BODY,marker='o',ms=5,lw=1.7);ax.axhline(0,color=GRID,lw=.8);ax.set_xticks(range(6),[f's{i}' for i in range(6)]);ax.set_ylim(-6.8,.8);ax.set_yticks([-6,-4,-2,0]);ax.set_ylabel('Potential Φ(s)');ax.set_xlabel('State along the constructed sequence');ax.grid(axis='y',color=GRID,lw=.5);panel(ax,'a','A declared sequence of potentials')
 for i,p in enumerate(phi):ax.annotate(f'{p:.0f}',(i,p),xytext=(0,10),textcoords='offset points',ha='center',fontsize=9)
 ax.annotate('terminal Φ = 0',xy=(5,0),xytext=(2.6,-1.2),fontsize=9,color=HEAD,arrowprops={'arrowstyle':'->','color':HEAD,'lw':1})
 ax=fig.add_axes([.53,.32,.40,.44]);im=ax.imshow(terms,cmap=DIV,vmin=-6,vmax=6,aspect='auto');ax.set_xticks(range(6),[f'Φ(s{i})' for i in range(6)]);ax.set_yticks(range(5),[f't = {i}' for i in range(5)]);ax.set_xlabel('');panel(ax,'b','Interior contributions cancel exactly')
 for y in range(n):
  for x in range(n+1):
   if abs(terms[y,x])>1e-8:ax.text(x,y,f'{terms[y,x]:+.2f}',ha='center',va='center',fontsize=9,color=label_color(DIV((terms[y,x]+6)/12)))
 ax.set_xticks(np.arange(-.5,6,1),minor=True);ax.set_yticks(np.arange(-.5,5,1),minor=True);ax.grid(which='minor',color='white',lw=1);ax.tick_params(which='minor',bottom=False,left=False)
 for j,v in enumerate(total):ax.text(j,5.45,f'{v:+.0f}',ha='center',fontsize=11,fontweight='bold',color=HEAD if j==0 else MUTED,clip_on=False)
 ax.text(-.85,5.45,'Σ',fontsize=11,clip_on=False)
 fig.text(.08,.20,r'$F_t = \gamma\Phi(s_{t+1})-\Phi(s_t)$',fontsize=15,fontfamily='DejaVu Serif');fig.text(.52,.16,r'$\sum_{t=0}^{4}\gamma^t F_t = -\Phi(s_0)+\gamma^5\Phi(s_5)=6$',fontsize=14,fontfamily='DejaVu Serif')
 footer(fig,'Each matrix row contains the two terms contributed by one transition after discounting. Only the initial boundary survives.\nThis algebraic example is not a training curve. Policy-invariance claims still require consistent task, discount, and terminal assumptions.')
 save(fig,'reward-telescoping','Potential-based shaping and telescoping cancellation','Analytical example with explicitly declared potentials and discount, not a measured reinforcement-learning result.')

# 6. The retained benchmark, validated against a fresh run by extract-data.ts.
def evaluation_plate():
 rows=D['benchmark']['rows'];algs=['BFS','Dijkstra','A*'];by={(r['case'],r['algorithm']):r for r in rows};solved=[i for i in range(1,25) if by[i,'A*']['solved']];cost=np.array([[by[i,a]['cost'] if by[i,a]['solved'] else np.nan for i in range(1,25)] for a in algs]);fig=plt.figure(figsize=(12,7.45));header(fig,'A benchmark is a distribution, not one favorable run','Measured static-grid-v1 results · 24 paired cases · seeds 2026–2049 · 10 × 8 grids · fixed generator and tie-break')
 ax=fig.add_axes([.075,.58,.86,.23]);cmap=HEAT.copy();cmap.set_bad('#eceff2');im=ax.imshow(cost,cmap=cmap,vmin=16,vmax=44,aspect='auto');ax.set_yticks(range(3),algs);ax.set_xticks(range(24),range(1,25));ax.tick_params(length=0,labelsize=8.5);ax.set_xlabel('Case index (seed = 2025 + index)',fontsize=9);panel(ax,'a','Returned weighted cost on every case')
 for y in range(3):
  for x in range(24):
   v=cost[y,x];ax.text(x,y,'×' if np.isnan(v) else f'{v:.0f}',ha='center',va='center',fontsize=8.5,color=MUTED if np.isnan(v) else label_color(cmap((v-16)/28)))
 ax.set_xticks(np.arange(-.5,24,1),minor=True);ax.set_yticks(np.arange(-.5,3,1),minor=True);ax.grid(which='minor',color='white',lw=1);ax.tick_params(which='minor',bottom=False,left=False)
 ax2=fig.add_axes([.075,.145,.39,.29]);x=[by[i,'Dijkstra']['expanded'] for i in solved];y=[by[i,'A*']['expanded'] for i in solved];ax2.plot([0,80],[0,80],ls='--',lw=1,color='#a6aeb5',zorder=0);ax2.scatter(x,y,color=HEAD,s=30,alpha=.8,edgecolor='white',lw=.6,zorder=4);ax2.set_xlim(0,80);ax2.set_ylim(0,80);ax2.set_xticks([0,20,40,60,80]);ax2.set_yticks([0,20,40,60,80]);ax2.set_xlabel('Dijkstra expanded cells',fontsize=9);ax2.set_ylabel('A* expanded cells',fontsize=9);ax2.grid(color=GRID,lw=.5);panel(ax2,'b','Paired search effort on solved cases');ax2.text(4,69,'below diagonal:\nfewer expansions with A*',fontsize=8.5,color=HEAD,va='top');ax2.annotate('case 6',xy=(by[6,'Dijkstra']['expanded'],by[6,'A*']['expanded']),xytext=(44,14),fontsize=8.5,arrowprops={'arrowstyle':'-','color':MUTED,'lw':.8})
 ax3=fig.add_axes([.56,.145,.375,.29]);ax3.axis('off');panel(ax3,'c','Summary with the denominator visible');col=[0,.40,.64,.88];heads=['Algorithm','Solved','Mean cost','Mean expanded'];
 for xx,h in zip(col,heads):ax3.text(xx,.93,h,fontsize=8.5,color=MUTED,ha='left' if xx==0 else 'center',transform=ax3.transAxes)
 for j,a in enumerate(algs):
  ar=[r for r in rows if r['algorithm']==a and r['solved']];mc=np.mean([r['cost'] for r in ar]);me=np.mean([r['expanded'] for r in ar]);yy=.71-j*.19
  vals=[a,f'{len(ar)}/24',f'{mc:.1f}',f'{me:.1f}']
  for xx,val in zip(col,vals):ax3.text(xx,yy,val,fontsize=11,color=HEAD if a=='A*' else INK,weight='bold' if a=='A*' else 'normal',ha='left' if xx==0 else 'center',transform=ax3.transAxes)
  ax3.plot([0,1],[yy-.07,yy-.07],transform=ax3.transAxes,color=GRID,lw=.7)
 ax3.text(0,.02,'Means include the 20 solved cases.\n× marks four disconnected instances.\nNo timing or trained-policy results are shown.',fontsize=8.8,color=MUTED,transform=ax3.transAxes,va='bottom',linespacing=1.55)
 footer(fig,'Generated from the committed 72-row baseline and checked against a fresh execution. Cost optimality and expansion count are distinct metrics.\nThis small, fixed instance set is an engineering check; it is not a claim of general algorithm superiority or a full-game Snake benchmark.')
 save(fig,'benchmark-results','Measured static-grid benchmark results','Exact 24-case benchmark cost heatmap, paired expansion scatter, and aggregate summaries. Unsolved cases are explicit.')


# Compact graphics re-render one meaningful panel; never shrink the full plate.
def thumbnails(kinds=None):
 for kind in (kinds or ['state','search','cycle','connectivity','reward','evaluation']):
  fig=plt.figure(figsize=(2.4,1.8));ax=fig.add_axes([.025,.025,.95,.95]);ax.axis('off')
  if kind=='state':
   st=D['state']['tailEntry'];board(ax,6,4);ax.set_xlim(1.6,3.4);ax.set_ylim(3.4,1.6)
   pts=np.array([xy(p) for p in st['body']]);ax.plot(pts[:,0],pts[:,1],color=BODY,lw=23,solid_capstyle='round',solid_joinstyle='round',zorder=3)
   for i,(x,y) in enumerate(pts):
    ax.add_patch(Circle((x,y),.265,fc=HEAD if i==0 else BODY,ec='white',lw=1.1,zorder=4))
    ax.text(x,y,str(i),ha='center',va='center',fontsize=14,color='white',weight='bold',zorder=5)
   ax.annotate('',xy=(3,2.29),xytext=(3,2.72),arrowprops={'arrowstyle':'-|>','color':'white','lw':1.7},zorder=10)
  elif kind=='search':
   q=D['search'];tr=q['traces']['A*'];vals={f"{f['current']['x']},{f['current']['y']}":j+1 for j,f in enumerate(tr['frames'])};board(ax,10,8,q['walls'],vals,vmin=1,vmax=66)
   pts=np.array([xy(p) for p in tr['path']]);ax.plot(pts[:,0],pts[:,1],color='white',lw=3.1,zorder=4);ax.plot(pts[:,0],pts[:,1],color=RED,lw=1.3,zorder=5)
   for k in q['terrain']:
    x,y=map(int,k.split(','));ax.plot(x+.25,y-.25,marker='^',ms=2,color=GOLD,zorder=6)
   marker(ax,q['start'],'S',HEAD);marker(ax,q['goal'],'G',RED)
  elif kind=='cycle':
   c=D['cycle'];idx={f"{p['x']},{p['y']}":i for i,p in enumerate(c['path'])};board(ax,10,6,values=idx,vmin=0,vmax=59,cmap=HEAT);pts=np.array([xy(p) for p in c['path']+[c['path'][0]]]);ax.plot(pts[:,0],pts[:,1],color='#64874b',lw=.8);body(ax,c['states'][0]['body'],order=False);marker(ax,c['path'][15],'H',HEAD)
  elif kind=='connectivity':
   q=D['connection'];vals={f"{p['x']},{p['y']}":1 for p in q['closed']['reachable']};board(ax,10,7,q['closed']['walls'],vals,cmap=LinearSegmentedColormap.from_list('reach',['white','#c1dfa4']),vmax=1)
   for p in q['closed']['right']:
    x,y=xy(p);ax.add_patch(Rectangle((x-.5,y-.5),1,1,fc='#e5e3ee',ec='white',lw=.6,zorder=1))
   marker(ax,q['start'],'S',HEAD);ax.add_patch(Rectangle((4.56,2.56),.88,.88,fill=False,ec=RED,lw=1.5,zorder=5))
  elif kind=='reward':
   phi=np.array([-6.,-5.,-4.,-3.,-2.,0.]);terms=np.zeros((5,6))
   for t in range(5):terms[t,t]=-.9**t*phi[t];terms[t,t+1]=.9**(t+1)*phi[t+1]
   ax.imshow(terms,cmap=DIV,vmin=-6,vmax=6,aspect='equal')
   for y in range(5):
    for x in range(6):
     if abs(terms[y,x])>1e-9:ax.text(x,y,'+' if terms[y,x]>0 else '−',ha='center',va='center',fontsize=11,color=label_color(DIV((terms[y,x]+6)/12)))
  else:
   rows=D['benchmark']['rows'];by={(r['case'],r['algorithm']):r for r in rows};solved=[i for i in range(1,25) if by[i,'A*']['solved']];ax.plot([0,80],[0,80],ls='--',lw=1,color='#b1bbc3');ax.scatter([by[i,'Dijkstra']['expanded'] for i in solved],[by[i,'A*']['expanded'] for i in solved],s=18,color=HEAD,edgecolor='white',lw=.4,zorder=3);ax.set_xlim(0,80);ax.set_ylim(0,80);ax.plot([0,0,80],[80,0,0],color='#9caab6',lw=.8);ax.text(5,66,'A*',fontsize=9,color=HEAD);ax.text(45,5,'Dijkstra',fontsize=8,color=MUTED)
  ax.axis('off');fig.savefig(ROOT/f'{kind}-thumb.svg',format='svg',metadata={'Title':f'{kind.capitalize()} scientific diagram detail','Description':'Single-panel detail generated from the same exact data as the full scientific plate.'})
  if PREVIEW is not None: fig.savefig(PREVIEW/f'{kind}-thumb.png',dpi=115)
  plt.close(fig)

thumbnails()

for f in [state_plate,search_plate,cycle_plate,connectivity_plate,reward_plate,evaluation_plate]:f()
print('Generated six SVG plates in',ROOT)
