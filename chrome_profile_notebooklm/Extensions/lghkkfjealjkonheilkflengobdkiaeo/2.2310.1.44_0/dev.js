const toggleDevLogs = async (e) => {
    let checked = e.target.checked;
    await chrome.storage.local.set({ devLogsToggleStatus: checked });
    window.location.reload();
}

const devLogInit = async () => {
    let res = await chrome.storage.local.get(['devLogsToggleStatus']);
    if (res.devLogsToggleStatus) {
        document.querySelector("#devLogsToggleCheckbox").checked = true;
    }
}

const flushCache = async () => {
    if (confirm("Are you sure you want to flush the cache?")) {
        await chrome.storage.local.clear();
        window.location.reload();
    }
}

const cacheInit = async () => {
    let res = await chrome.storage.local.get();
    console.log('FULL STORAGE', res);
    document.querySelector("#cacheContent").innerHTML = JSON.stringify(res, null, 2);
}

devLogInit();
cacheInit();
document.querySelector("#devLogsToggleCheckbox").addEventListener("change", toggleDevLogs);
document.querySelector("#flushCacheBtn").addEventListener("click", flushCache);