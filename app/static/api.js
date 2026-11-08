export async function api(path, options={}) {
 const response=await fetch('/api'+path,{credentials:'same-origin',...options,headers:{'Content-Type':'application/json',...options.headers}});
 let data;try{data=await response.json();}catch{throw Error('The server returned an unexpected response. Please try again.');}
 if(!response.ok){const error=Error(typeof data.detail==='string'?data.detail:'Check the input and try again.');error.status=response.status;throw error;}
 return data;
}
