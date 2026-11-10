/** Exact inputs for the scientific plates. Run from the project root with tsx. */
import {writeFileSync,readFileSync} from 'node:fs';
import {cycle,initialGame,move,type Game} from '../../../lib/engine';
import {traceSearch,connected} from '../../../lib/explore';
import {makeCase,runBenchmark,protocol,defaultConfig} from '../../../lib/benchmark';
const body=[{x:3,y:3},{x:2,y:3},{x:2,y:2},{x:3,y:2}];
const before={...initialGame(),body,dir:{x:1,y:0},food:{x:6,y:2}};
const growthBefore={...before,food:{x:4,y:3}};
const state={before,tailEntry:move(before,{x:0,y:-1},8,6),growthBefore,growth:move(growthBefore,{x:1,y:0},8,6)};
const fixture=makeCase(2031,true);
const search={seed:2031,w:10,h:8,start:protocol.start,goal:protocol.goal,walls:[...fixture.walls],terrain:[...fixture.terrain],traces:Object.fromEntries(['BFS','Dijkstra','A*'].map(algorithm=>[algorithm,traceSearch(10,8,protocol.start,protocol.goal,fixture.walls,algorithm as 'BFS'|'Dijkstra'|'A*',fixture.terrain)]))};
const cyc=cycle(10,6),headIndex=15,cycleBody=Array.from({length:10},(_,i)=>cyc[(headIndex-i+cyc.length)%cyc.length]);
let cg:Game={...initialGame(),body:cycleBody,food:cyc[40],dir:{x:0,y:1}};
const cycleStates=[cg];
for(let i=0;i<8;i++){const target=cyc[(headIndex+i+1)%60];cg=move(cg,{x:target.x-cg.body[0].x,y:target.y-cg.body[0].y},10,6);if(cg.status!=='playing')throw new Error('Cycle illustration failed');cycleStates.push(cg)}
const openWalls=new Set(Array.from({length:7},(_,y)=>`5,${y}`).filter(x=>x!=='5,3'));
const closedWalls=new Set(Array.from({length:7},(_,y)=>`5,${y}`));
const connection={w:10,h:7,start:{x:2,y:3},passage:{x:5,y:3},open:{walls:[...openWalls],reachable:connected(10,7,{x:2,y:3},openWalls)},closed:{walls:[...closedWalls],reachable:connected(10,7,{x:2,y:3},closedWalls),right:connected(10,7,{x:7,y:3},closedWalls)}};
const baseline=JSON.parse(readFileSync('lib/benchmark-baseline.json','utf8'));
const actual=runBenchmark(defaultConfig);
if(JSON.stringify(actual)!==JSON.stringify(baseline))throw new Error('Current benchmark differs from recorded baseline; inspect before publishing figure');
const result={schema:'snakeguide-plates-v1',engineFiles:['lib/engine.ts','lib/explore.ts','lib/benchmark.ts'],state,search,cycle:{w:10,h:6,path:cyc,headIndex,states:cycleStates},connection,benchmark:{protocol,config:defaultConfig,rows:actual}};
writeFileSync('public/research/figures/plate-data.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({search:Object.fromEntries(Object.entries(search.traces).map(([k,t])=>[k,{cost:t.cost,steps:t.steps,expanded:t.frames.length}])),reachable:[connection.open.reachable.length,connection.closed.reachable.length],benchmark:actual.filter(r=>r.algorithm==='A*').map(r=>[r.seed,r.cost,r.expanded])}));
