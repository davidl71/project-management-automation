import { r } from './chunks/jquery-e1fc36eb.js';

chrome.runtime.sendMessage({cmd:"getCosmeticsFilters"}).then((t=>{if("false"===t)return;var n=0;t.styles.forEach((t=>{if(!t)return;(t=t.replaceAll(" ","")).includes("display:none")&&(t=t.replace("{display:none!important;}",""));let l=t.split(",")[0];r(l).length>0&&(n+=r(l).length);})),chrome.runtime.sendMessage({cmd:"setBlockedCountFromContent",count:n});let l=t.styleString;var r$1=document.createElement("style");r$1.innerText=l,document.head.appendChild(r$1);})).catch((e=>{console.log(e);}));
