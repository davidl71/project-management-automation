import {
    ApplicationInsights
} from '@microsoft/applicationinsights-web'
import global from './global';
import firebaseManager from './FirebaseManager';

class ApplicationInsightsManager {
    constructor() {
        if (!ApplicationInsightsManager.instance) {
            this.appInsights = new ApplicationInsights({
                config: {
                    instrumentationKey: "6edb1032-d98e-4326-91d6-dac3bf27ed41",
                    maxBatchSizeInBytes: 10240,
                        maxBatchInterval: 15e3,
                        enableDebug: !1,
                        disableTelemetry: !1,
                        disableAjaxTracking: !0,
                        isCookieUseDisabled: !0,
                        isBrowserLinkTrackingEnabled: !0
                }
            })
            
            this.appInsights.loadAppInsights()
            this.appInsights.addTelemetryInitializer(t => {
                // Update criteria as per your need.
                if (t.baseType != 'EventData') {
                    return false;
                } 
                // disable
                return true; // enable everything else
            });
            ApplicationInsightsManager.instance = this
        }
        return ApplicationInsightsManager.instance
    }

    trackEvent(event, customProperties = {}) {
        if (!global.ACCEPT_GDPR) { 
            return
        }
        this.appInsights.trackEvent({
            name: event
        }, customProperties)
        this.appInsights.flush()

        // Firebase event
        firebaseManager.logEvent(event, customProperties)
    }
}

const AppInsightInstance = new ApplicationInsightsManager()
Object.freeze(AppInsightInstance)

const AppInsightEvent = {
    newInstall: "AdBlock.NewInstall",
    // uninstall: "AdBlock.Uninstall", //not this version
    popupShow: "Popup.Show",
    extensionActive: "Extension.Active", //once per 24 hours
    clickPause: "Paused.Click",
    clickMainResume: "Resume.Click.Main", //resume by clicking button beyond domain
    clickPauseResume: "Resume.Click.Pause", //resume by clicking paused button small
    protectionEnable: "Protection.Enable",
    protectionDisable: "Protection.Disable",
    siteBrokenYes: "SiteBroken.Yes",
    siteBrokenNo: "SiteBroken.No",
    reportBrokenSiteClick: "Main.Report.Click",
    feedbackCLick: "Main.Feedback.Click",
    reportBrokenSiteBack: "Report.Back",
    reportBrokenSiteSend: "Report.Send",
    reportBrokenSiteOK: "Report.OK",
    // notificationCancel: "Notification.Cancel",
    // notificationProceed: "Notification.Proceed",
    gdprAcceptPopup: "Popup.GDPR.Accept",
    gdprShowPopup: "Popup.GDPR.Show",
    gdprAcceptWelcome: "Welcome.GDPR.Accept"
}

export {
    AppInsightEvent,
    AppInsightInstance
}