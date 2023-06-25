// Update the extension text with the selected text
function updateExtensionText(selectedText) {
  const textElement = document.getElementById("extensionText");
  textElement.textContent = selectedText;
}

// Create a context menu item with a unique ID
chrome.contextMenus.create({
  id: "myContextMenu",
  title: "My Context Menu",
  contexts: ["page", "selection"],
});

// Add a listener for when the menu item is clicked
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "myContextMenu") {
    // Update the extension text with the selected text
    updateExtensionText(info.selectionText);

    // Inject the content script and send a message to modify the <h1> elements
    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        function: modifyH1Elements,
      },
      () => {
        // Send a message to the content script after the script is injected and ready
        chrome.tabs.sendMessage(tab.id, { text: info.selectionText });
      }
    );
  }
});

// Content script function to modify the <h1> elements
function modifyH1Elements() {
  // Listen for messages from the extension
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.text) {
      // Modify the <h1> elements on the webpage
      const h1Elements = document.getElementsByTagName("h1");

      for (let i = 0; i < h1Elements.length; i++) {
        h1Elements[i].textContent = message.text;
      }
    }
  });
}
