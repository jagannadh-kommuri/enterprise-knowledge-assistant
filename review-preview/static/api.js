// Browser-only review adapter. This is not the Python API or a security boundary.
const STORE='atlas-review-v1';
const SESSION='atlas-review-role';
const makeId=()=>globalThis.crypto?.randomUUID?.() || 'review-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
const STOP=new Set('the a an is are was were what how do does to of in on for and or with it i can my our we'.split(' '));
const words=t=>(t.toLowerCase().match(/[a-z0-9]+/g)||[]).filter(t=>!STOP.has(t));
const chunks=t=>{const w=t.trim().split(/\s+/),out=[];for(let i=0;i<w.length;i+=140)out.push(w.slice(i,i+170).join(' '));return out;};
const seed=[{id:'incident-demo',title:'Incident response handbook',visibility:'team',content:'For a severity one incident, the on-call engineer acknowledges the alert within five minutes and opens an incident channel. The incident commander coordinates investigation and publishes updates every fifteen minutes. The first priority is restoring service safely.\n\nA rollback requires the last known healthy release, a recorded incident identifier, and approval from the incident commander. After rollback, verify API error rates, request latency, and database connection health for ten minutes before closing the incident.\n\nA blameless postmortem is completed within three business days. Include the timeline, customer impact, root cause, contributing factors, and action items with owners and due dates.'},{id:'access-demo',title:'Access & document policy',visibility:'team',content:'New employees request application access through the service desk. Their manager approves the business need, and the platform team grants the least privileged role. Production access expires after thirty days unless renewed.\n\nTeam documents are searchable by readers and administrators. Administrator-only documents are visible only to administrators. Readers cannot upload or delete documents. An administrator must review document classification before upload.\n\nRotate service credentials after suspected exposure. Revoke the old credential, provision the replacement through the secret manager, update the service configuration, and verify the application before closing the security ticket.'},{id:'restricted-demo',title:'Launch planning · restricted demo',visibility:'admin',content:'The fictional launch codename is Violet Monsoon. Only administrators can retrieve this demonstration document in the role preview. Executive review is required before release.'}];
function initial(){return{documents:seed.map(d=>({...d,created:Date.now()/1000})),events:[],feedback:[]};}
function read(){try{const raw=localStorage.getItem(STORE);return raw?JSON.parse(raw):initial();}catch{throw Error('Browser storage is unavailable. Allow site storage to use this review.');}}
function save(state){try{localStorage.setItem(STORE,JSON.stringify(state));}catch{throw Error('Browser storage is full or disabled. Delete unused documents or allow site storage.');}}
function check(role){if(!role)throw Error('Select a review role to continue.');}
function admin(role){check(role);if(role!=='admin')throw Error('Administrator role required in this preview.');}
export async function api(path,options={}){
 const start=performance.now(),role=sessionStorage.getItem(SESSION),body=options.body?JSON.parse(options.body):{},method=options.method||'GET';
 if(path==='/login'){if(!['admin','reader'].includes(body.password))throw Error('Choose an administrator or reader preview.');sessionStorage.setItem(SESSION,body.password);return{role:body.password};}
 if(path==='/logout'){sessionStorage.removeItem(SESSION);return{ok:true};}
 check(role);
 if(path==='/me')return{role,mode:'preview',prompt_version:'browser-review-v1'};
 const state=read();
 if(path==='/documents'&&method==='GET')return state.documents.filter(d=>role==='admin'||d.visibility==='team').map(({content,...d})=>({...d,chunks:chunks(content).length}));
 if(path==='/documents'&&method==='POST'){
  admin(role);if(!body.title?.trim()||body.title.length>120||body.content?.trim().length<10||body.content.length>100000||!['team','admin'].includes(body.visibility))throw Error('Use a title and 10–100,000 characters of document content.');
  if(state.documents.length>=100)throw Error('Review limit: 100 documents. Delete unused documents.');
  const d={id:makeId(),title:body.title.trim(),content:body.content,visibility:body.visibility,created:Date.now()/1000};state.documents.push(d);save(state);return{id:d.id,chunks:chunks(d.content).length,embedding_tokens:0};
 }
 if(path.startsWith('/documents/')&&method==='DELETE'){admin(role);const id=path.split('/').at(-1);state.documents=state.documents.filter(d=>d.id!==id);save(state);return{ok:true};}
 if(path==='/ask'){
  const q=words(body.question||'');if(!q.length||body.question.length>1500)throw Error('Enter a specific question, up to 1,500 characters.');
  const counts=t=>{const m=new Map();for(const w of words(t))m.set(w,(m.get(w)||0)+1);return m;};
  const cosine=(a,b)=>{let dot=0;for(const[k,v]of a)dot+=v*(b.get(k)||0);const norm=m=>Math.sqrt([...m.values()].reduce((s,v)=>s+v*v,0));return dot/(norm(a)*norm(b)||1);};
  const query=counts(body.question);const sources=state.documents.filter(d=>role==='admin'||d.visibility==='team').flatMap(d=>chunks(d.content).map((text,i)=>({title:d.title,document_id:d.id,chunk:i+1,text,score:Number(cosine(query,counts(text)).toFixed(4))}))).filter(s=>s.score>=.12).sort((a,b)=>b.score-a.score).slice(0,4);
  const latency_ms=Math.round((performance.now()-start)*10)/10;
  const result={answer:sources.length?sources.map((s,i)=>`${s.text} [${i+1}]`).join('\n\n'):'I could not find enough evidence in the documents visible to this review role. Add a relevant document or rephrase your question.',sources,mode:'browser preview',tokens:0,latency_ms,request_id:makeId()};
  state.events.push({latency_ms});state.events=state.events.slice(-1000);save(state);return result;
 }
 if(path==='/metrics'){admin(role);return{requests:state.events.length,tokens:0,avg_latency_ms:state.events.length?Number((state.events.reduce((a,b)=>a+b.latency_ms,0)/state.events.length).toFixed(1)):0,failures:0};}
 throw Error('This action is not available in the browser review.');
}
