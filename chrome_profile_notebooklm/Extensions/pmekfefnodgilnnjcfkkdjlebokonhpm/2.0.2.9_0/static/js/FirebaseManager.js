class FirebaseManager {
  constructor() {
    const gaEndpoint = "https://www.google-analytics.com/mp/collect"
    const measurementID = "G-CNPSFD8C9B"
    const apiSecret = "Xbb6cV-bQge5T3n6MM9YsA"
    this.gaUrl = `${gaEndpoint}?measurement_id=${measurementID}&api_secret=${apiSecret}`
    this.clientId = ""
  }

  async getClientID() {
    if (this.clientId) {
      // alread read
      return this.clientId
    }

    // read client id from storage
    const result = await chrome.storage.local.get('clientId')
    this.clientId = result.clientId
    if (!this.clientId) {
      // create new client id
      this.clientId = this.generateClientID()
      await chrome.storage.local.set({clientId: this.clientId})
    }
    return this.clientId
  }

  generateClientID () {
    let time = new Date().getTime()
    let id = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      let rand = (time + Math.random() * 16) % 16 | 0
      time = Math.floor(time / 16)
      return (c === 'x' ? rand : (rand & 0x3 | 0x8)).toString(16)
    })
    return id
  }

  async logEvent(event, customProperties = {}) {
    let eventName = event.replaceAll(".", "_")
    let body = {
      client_id: await this.getClientID(),
      events: [
        {
          name: eventName,
          params: customProperties
        }
      ]
    }
    // since our rule will block firebase analystics url,
    // have to add our ga url to allow list,
    // which is in ruleset_2.json, id: 206129
    fetch(this.gaUrl,{ method: 'POST', body: JSON.stringify(body) })
  }
}

const firebaseManager = new FirebaseManager()
export default firebaseManager