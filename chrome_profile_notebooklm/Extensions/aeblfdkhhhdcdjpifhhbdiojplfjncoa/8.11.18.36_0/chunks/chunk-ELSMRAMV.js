
!function(){try{var e="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:{},n=(new Error).stack;n&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[n]="4a57b5f2-21bb-518c-b0d4-2629045539fb")}catch(e){}}();
var s=class{_prependMessage;constructor(i=""){this._prependMessage=i}log=(i,...e)=>{this.isPermitted()&&(this.message(i),[...e])};debug=(i,...e)=>{this.isPermitted()&&(this.message(i),[...e])};info=(i,...e)=>{this.isPermitted()&&console.info(this.message(i),...e)};warn=(i,...e)=>{this.isPermitted()&&console.warn(this.message(i),...e)};error=(i,...e)=>{this.isPermitted()&&console.error(this.message(i),...e)};isPermitted=()=>!1;message=i=>this._prependMessage?`${this._prependMessage}: ${i}`:i};export{s as a};

//# debugId=4a57b5f2-21bb-518c-b0d4-2629045539fb
