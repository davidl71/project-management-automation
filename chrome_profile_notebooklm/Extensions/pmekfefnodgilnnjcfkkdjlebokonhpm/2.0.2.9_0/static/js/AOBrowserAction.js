/**
 * AOBrowserAction.js
 *
 * Trend Micro Ad Blocker For Chrome 
 *
 * Created on 2022/02/22
 * Copyright 2022 Trend Micro, Inc. All rights reserved.
 *
 */
import AOLog from "./AOLog";
import { tabs, action, declarativeNetRequest } from 'webextension-polyfill'
import global from "./global";
import { parse } from 'tldts-experimental';

class AOBrowserAction { 
    constructor() { 
        this.displayCountAsBadgeText(true); 
    }
    
    displayCountAsBadgeText(trigger) { 
        declarativeNetRequest.setExtensionActionOptions({
            displayActionCountAsBadgeText: trigger
        })
    }

    _setBadgeColor() { 
        action.setBadgeBackgroundColor({
            color: "rgba(85, 85, 85, 1)"
        });
    }

    update(tabId) { 
        if (tabId) { 
            this._setIcon(!global.PAUSED_BLOCKING, tabId) 
        }
    }

    async _setIcon(active, tabId) { 
        if (tabId < 0) {
            return;
        }
        var iconPath = "./static/images/icon/toolbar-icon-19.png"
        let tabHostInfo = await this._getHostInfo(tabId);
        let currentHost = tabHostInfo.hostname
        let isHttp = tabHostInfo.isHttp
        if (!active) {
            iconPath = "./static/images/icon/gray-toolbar-icon-19.png"
        } else { 
            
            if (currentHost && isHttp) {
                AOLog.debug(`${currentHost} setIcon`)
                if (global.CUSTOMWHITELIST.includes(currentHost)) { 
                    iconPath = "./static/images/icon/disable-toolbar-icon-19.png"
                }else if (currentHost !== "new-tab-page") { 
                    iconPath = "./static/images/icon/check-toolbar-icon-19.png"
                }
            }
        }

        AOLog.debug(`${iconPath}/${tabId} setIcon`)
        action.setIcon({
            path: {
                '19': iconPath
            },
            tabId: tabId
        }).catch((error) => { 
            AOLog.error(`set icon error, ${error}`)
        })

    }

    async _getHostInfo(tabId) { 
        let tab = await tabs.get(tabId)
        let url = tab.url
        let hostname = parse(url).hostname
        let isHttp = url.includes("http://") || url.includes("https://")

        return {
            hostname: hostname,
            isHttp: isHttp
        }
    }
}

export default new AOBrowserAction()