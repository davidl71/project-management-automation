"use strict";
!function(){try{var e="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},n=(new Error).stack;n&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[n]="2dcdc32d-7f16-57aa-b21e-05ef2a2f44d2")}catch(e){}}();

(() => {
chrome.runtime.onMessage.addListener((e,a,t)=>{e.name==="health-check-request"&&(console.info("HealthCheck: received request from tab "+a.tab?.id),t({name:"health-check-response",data:"alive"}))});
})();

//# debugId=2dcdc32d-7f16-57aa-b21e-05ef2a2f44d2
