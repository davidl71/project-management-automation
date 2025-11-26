/**
 * UnblockedList.js
 *
 * Trend Micro Ad Blocker For Chrome 
 *
 * Created on 2022/11/121
 * Copyright 2022 Trend Micro, Inc. All rights reserved.
 *
 */
import { storage,declarativeNetRequest } from 'webextension-polyfill';
 
class AOUnblockedList { 
    constructor() {

    }

    getAllSites() { 
        return storage.local.get("kUnblockedList")
    }

    async initUnblockedList() {
        let unblockedList = await this.getAllSites()
        this.updateRules(unblockedList["kUnblockedList"])
    }

    updateRules(unblockedList) {
        declarativeNetRequest.getDynamicRules().then(rules => { 
            let length = rules.length;
            if (length > 0) {
                let ids = Array.from({ length: length }, (_, i) => i + 1) 
                declarativeNetRequest.updateDynamicRules(
                    {
                        removeRuleIds: ids
                    }
                )
            }
            
            if (unblockedList && unblockedList.length > 0) { 
                for (let i = 0; i < unblockedList.length; i++) {
                    let domain = unblockedList[i]
                    // if (domain.startsWith("www.")) {
                    //     domain = domain.slice(4)
                    // }
                    domain = "||" + domain + "^"
                    declarativeNetRequest.updateDynamicRules(
                        {
                            addRules: [
                                {
                                    action: {
                                        type: "allowAllRequests"
                                    },
                                    condition: {
                                        resourceTypes: [
                                            "main_frame",
                                            "sub_frame"
                                        ],
                                        urlFilter: domain
                                    },
                                    priority: 2001,
                                    id: i + 1
                                }
                            ]
                        }
                    )
                }
            }
        })
    }
}

export default new AOUnblockedList();