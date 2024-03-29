import re

# Sample JavaScript code
javascript_code = '''
window.addEventListener('message', function(event) {
    var data = event.data;
    
    var string1 = data.test1;
    var modifiedData = preprocess(test2);
    var string2 = modifiedData.test3;
    var string3 = data.test4;
    var string4 = event.data.test5
    var string5 = event.data.test6
    var string6 = event.data['test7']
    var string = event.data["test8"]

    var string6 = event.data[fake]
});
'''

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

  // PAYLOAD: 
  // postMessage({ message: "<img src=x onerror=alert(1)>" }, "*")
'''


# Extract the unique strings using regex with multiline flag, excluding blacklist matches
def extract_unique_strings(javascript_code):
  # Regular expression patterns to match event.data.(string)
  patterns = [
      r'event\.data\["(\w+)"\]',  # Matches event.data["field"]
      r"event\.data\['(\w+)'\]",  # Matches event.data['field']
      r'event\.data\.(\w+)',       # Matches event.data.field
      r'event\.data(?:[^.]|\.(?!\w))*\.(\w+)', # Matches nested
      r"(?<=\.)\w+" # matches all fields after a .
  ]

  blacklist = [
      'addEventListener',
      'appendChild',
      'after',
      'animate',
      'append',
      'attributes',
      'before',
      'blur',
      'childElementCount',
      'childNodes',
      'children',
      'classList',
      'className',
      'click',
      'cloneNode',
      'closest',
      'compareDocumentPosition',
      'contains',
      'contentEditable',
      'dataset',
      'dir',
      'dispatchEvent',
      'draggable',
      'firstChild',
      'firstElementChild',
      'focus',
      'getAttribute',
      'getAttributeNS',
      'getBoundingClientRect',
      'getClientRects',
      'getElementsByClassName',
      'getElementsByTagName',
      'getElementsByTagNameNS',
      'hasAttribute',
      'hasAttributeNS',
      'hasAttributes',
      'hasChildNodes',
      'id',
      'innerHTML',
      'insertAdjacentElement',
      'insertAdjacentHTML',
      'insertAdjacentText',
      'insertBefore',
      'isConnected',
      'isContentEditable',
      'isEqualNode',
      'isSameNode',
      'lastChild',
      'lastElementChild',
      'localName',
      'matches',
      'namespaceURI',
      'nextElementSibling',
      'nextSibling',
      'nodeName',
      'nodeType',
      'nodeValue',
      'normalize',
      'offsetHeight',
      'offsetLeft',
      'offsetParent',
      'offsetTop',
      'offsetWidth',
      'onabort',
      'onauxclick',
      'onblur',
      'oncancel',
      'oncanplay',
      'oncanplaythrough',
      'onchange',
      'onclick',
      'onclose',
      'oncontextmenu',
      'oncopy',
      'oncuechange',
      'oncut',
      'ondblclick',
      'ondrag',
      'ondragend',
      'ondragenter',
      'ondragleave',
      'ondragover',
      'ondragstart',
      'ondrop',
      'ondurationchange',
      'onemptied',
      'onended',
      'onerror',
      'onfocus',
      'ongotpointercapture',
      'oninput',
      'oninvalid',
      'onkeydown',
      'onkeypress',
      'onkeyup',
      'onload',
      'onloadeddata',
      'onloadedmetadata',
      'onloadend',
      'onloadstart',
      'onlostpointercapture',
      'onmousedown',
      'onmouseenter',
      'onmouseleave',
      'onmousemove',
      'onmouseout',
      'onmouseover',
      'onmouseup',
      'onmousewheel',
      'onpaste',
      'onpause',
      'onplay',
      'onplaying',
      'onpointercancel',
      'onpointerdown',
      'onpointerenter',
      'onpointerleave',
      'onpointermove',
      'onpointerout',
      'onpointerover',
      'onpointerup',
      'onprogress',
      'onratechange',
      'onreset',
      'onresize',
      'onscroll',
      'onseeked',
      'onseeking',
      'onselect',
      'onselectstart',
      'onstalled',
      'onsubmit',
      'onsuspend',
      'ontimeupdate',
      'ontoggle',
      'onvolumechange',
      'onwaiting',
      'onwebkitfullscreenchange',
      'onwebkitfullscreenerror',
      'onwheel',
      'outerHTML',
      'ownerDocument',
      'parentElement',
      'parentNode',
      'prefix',
      'prepend',
      'previousElementSibling',
      'previousSibling',
      'querySelector',
      'querySelectorAll',
      'releasePointerCapture',
      'remove',
      'removeAttribute',
      'removeAttributeNS',
      'removeChild',
      'removeEventListener',
      'replaceChild',
      'replaceWith',
      'requestFullscreen',
      'scroll',
      'scrollBy',
      'scrollHeight',
      'scrollIntoView',
      'scrollIntoViewIfNeeded',
      'scrollLeft',
      'scrollLeftMax',
      'scrollTop',
      'scrollTopMax',
      'scrollTo',
      'setAttribute',
      'setAttributeNS',
      'shadowRoot',
      'slot',
      'spellcheck',
      'style',
      'tabIndex',
      'tagName',
      'textContent',
      'title',
      'toggleAttribute',
      'webkitMatchesSelector',
      'webkitRequestFullscreen',
      'willValidate',
      'wrap',
      'browserAction',
      'contextMenus',
      'cookies',
      'extension',
      'i18n',
      'management',
      'notifications',
      'runtime',
      'scripting',
      'tabs',
      'windows',
      'getBackgroundPage',
      'getURL',
      'getViews',
      'isAllowedFileSchemeAccess',
      'isAllowedIncognitoAccess',
      'sendMessage',
      'sendRequest',
      'getExtensionTabs',
      'getMessage',
      'getUILanguage',
      'detectLanguage',
      'getAcceptLanguages',
      'getLanguage',
      'getAvailableLanguages',
      'getISOLanguageCode',
      'getSelf',
      'getPermissionWarningsById',
      'getPermissionWarningsByManifest',
      'launchApp',
      'setLaunchType',
      'create',
      'update',
      'clear',
      'getAll',
      'getPermissionLevel',
      'connect',
      'getBackgroundPage',
      'getManifest',
      'getPackageDirectoryEntry',
      'getPlatformInfo',
      'getURL',
      'openOptionsPage',
      'reload',
      'onInstalled',
      'onStartup',
      'onSuspend',
      'onSuspendCanceled',
      'onUpdateAvailable',
      'executeScript',
      'insertCSS',
      'registerContentScript',
      'unregisterContentScript',
      'executeScript',
      'insertCSS',
      'create',
      'executeScript',
      'insertCSS',
      'update',
      'remove',
      'query',
      'move',
      'reload',
      'detectLanguage',
      'captureVisibleTab',
      'get',
      'getAllInWindow',
      'getCurrent',
      'onActivated',
      'onUpdated',
      'onMoved',
      'onRemoved',
      'onReplaced',
      'onSelectionChanged',
      'onHighlighted',
      'onDetached',
      'onAttached',
      'onCreated',
      'onZoomChange',
      'duplicate',
      'highlight',
      'move',
      'reload',
      'sendMessage',
      'sendRequest',
      'zoom',
      'setZoomSettings',
      'connect',
      'captureVisibleTab',
      'print',
      'getZoom',
      'setZoom',
      'create',
      'get',
      'getAll',
      'getCurrent',
      'getLastFocused',
      'remove',
      'update'
  ]

  matches = set()
  for pattern in patterns:
      extracted_strings = re.findall(pattern, javascript_code, re.MULTILINE)
      filtered_strings = [string for string in extracted_strings if string not in blacklist]
      matches.update(filtered_strings)
  return list(matches)


path = 'Extensions/h1-replacer/h1-replacer(v3)_window.addEventListernerMessage/popup.js'
start_line = 2
end_line = 6


def extract_codes_postMessage(path,start_line,end_line):
  with open(path, 'r') as file:
    lines = file.readlines()

    # Adjust line numbers to Python's zero-based indexing
    start_line -= 1
    end_line -= 1

    # Trim the lines within the specified range
    code_lines = lines[start_line:end_line+1]

    # Join the trimmed lines to form the code string
    code = ''.join(code_lines)
  return code




code = extract_codes_postMessage(path,start_line,end_line)
