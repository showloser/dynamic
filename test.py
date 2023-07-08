from postMessageRegex import extract_unique_strings



javascript_code1 = '''
function abc() {
    window.addEventListener("message", (event) => {
      console.log("Event Data: ", event)
      xyz = event.data
      tags = document.getElementsByTagName('h1')
      tags[0].innerHTML = xyz.message + ' abc '
    }) 
  }
  
  chrome.tabs.query({ active: false, currentWindow: true }, function (tabs) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: abc,
      args: []
    })
  });
  
.tabs
  .cocksuker123

  .123skd
  // PAYLOAD: 
  // postMessage({ message: "<img src=x onerror=alert(1)>" }, "*")
'''



print(extract_unique_strings(javascript_code1))