/**
 * global.js
 *
 * Trend Micro Ad Blocker For Chrome 
 *
 * Created on 2022/01/14
 * Copyright 2019 Trend Micro, Inc. All rights reserved.
 *
 */

import { storage } from 'webextension-polyfill';
import { FiltersEngine } from '@cliqz/adblocker';
import AOLog from './AOLog';

class Global { 
    constructor() { 
        //constant
        this.ONE_DAY = 24 * 60 * 60 * 1000;

        this.EXCULDES = [
            '@@||trendmicro.com',
            "@@||ads.google.com^$document",
            "@@||analytics.google.com$document",
            "@@||google.com/analytics/*$document"
        ];

        this.CUSTOMWHITELIST = [
        ]

        this.ENGINEINFO = { 
            "easylist": {
                enabled: true,
                url: "https://easylist-downloads.adblockplus.org/easylist.txt",
                category: "ad"
            },
            "easylistprivacy": {
                enabled: true,
                url: "https://easylist-downloads.adblockplus.org/easyprivacy.txt",
                category: "tracker"
            },
            "fanboy-cookie": {
                enabled: true,
                url: "https://secure.fanboy.co.nz/fanboy-cookiemonster.txt",
                category: "tracker"
            },
            "easylist-china": {
                enabled: true,
                url: "https://easylist-downloads.adblockplus.org/easylistchina.txt",
                category: "ad"
            }
        }
        this.ACTIVED_ENGINE = [];
        this.PAUSED_BLOCKING = false;
        this.ENABLED = true;
        
        this.BROWSER_INFO = {
            displayName: "",
            name: "",
            version: "",
            os: "",
        };

        this.TOTAL_DAYS = 0
        this.ACCEPT_GDPR = false
        this.TOTAL_BLOCKED = 0
        this._buildBrowserInfo()
        this._setConfig()
        this.checkTotalInstalledDays()
        
    }

    _buildBrowserInfo() {
        var brand = navigator.userAgentData.brands[2]
        var browser = brand.brand.toLowerCase()
        if (browser.includes("=a?")) {
            brand = navigator.userAgentData.brands[1];
            browser = brand.brand.toLowerCase();
        }
        
        if (browser.includes("chromium")) {
            brand = navigator.userAgentData.brands[0];
            browser = brand.brand.toLowerCase(); 
        }

        const version = brand.version

        const platform = navigator.userAgentData.platform.toLowerCase()

        this.BROWSER_INFO.version = version;

        if (browser.includes('edge')) {
            this.BROWSER_INFO.displayName = "Edge";
            this.BROWSER_INFO.name = "edge";
        } else if (browser.includes('opera')) {
            this.BROWSER_INFO.displayName = 'Opera';
            this.BROWSER_INFO.name = 'opera';
        } else if (browser.includes('chrome')) {
            this.BROWSER_INFO.displayName = 'Chrome';
            this.BROWSER_INFO.name = 'chrome';
        } else if (browser.includes('firefox')) {
            this.BROWSER_INFO.displayName = 'Firefox';
            this.BROWSER_INFO.name = 'firefox';
        } else { 
            this.BROWSER_INFO.displayName = "Other"
            this.BROWSER_INFO.name = 'other'
        } 

        if (platform.includes('mac')) {
			this.BROWSER_INFO.os = 'macOS';
		} else if (platform.includes('win')) {
			this.BROWSER_INFO.os = 'win';
		} else if (platform.includes('linux')) {
			this.BROWSER_INFO.os = 'linux';
		} else if (platform.includes('chromium')) {
			this.BROWSER_INFO.os = 'chromeOS';
		}
    }
    
    checkTotalInstalledDays() { 
        storage.local.get().then(data => { 
            let installedDate = data["kInstalledDate"] 
            let now = Date.now()
            let millis = now - installedDate
            let days = Math.floor(millis / 1000 / 3600 / 24)
            days += 1
            this.TOTAL_DAYS = days
        })
    }

    _setConfig() {
        storage.local.get("kHasAcceptedGDPR").then(accepted => { 
            this.ACCEPT_GDPR = accepted["kHasAcceptedGDPR"] ? accepted["kHasAcceptedGDPR"] : false;
        })

        storage.local.get("kIsPaused").then(paused => { 
            this.PAUSED_BLOCKING = paused["kIsPaused"] ? paused["kIsPaused"] : false;
        })

        storage.local.get("kUnblockedList").then(unblocked => { 
            if (unblocked["kUnblockedList"]) {
                this.CUSTOMWHITELIST = unblocked["kUnblockedList"];
            }
        })

        storage.local.get("kTotalCount").then((count) => { 
            this.TOTAL_BLOCKED = count["kTotalCount"] ? count["kTotalCount"] : 0;
        })
    }

    setLocalEngineInfo() {
        storage.local.get("engineInfo").then(info => { 
            if (info) {
                AOLog.verbose("use database engineinfo")
                this.ENGINEINFO = info
            } else { 
                AOLog.verbose("database engineinfo is null, use default one")
                storage.local.set("engineInfo", this.ENGINEINFO)
            }
        })
    }

    setEngine(engine) { 
        this.ACTIVED_ENGINE.push(engine)
    }

    async getGDPR() { 
        let data = await storage.local.get()
        return data["kHasAcceptedGDPR"]
    }
}


export default new Global();