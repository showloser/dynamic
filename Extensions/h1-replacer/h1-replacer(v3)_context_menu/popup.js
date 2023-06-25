// Remove the context menu item if it already exists
chrome.contextMenus.remove("myContextMenu", () => {
    // Create the context menu item
    chrome.contextMenus.create({
      id: "myContextMenu",
      title: "My Context Menu",
      contexts: ["page", "selection"],
    });
  });
  
  // Add a listener for when the menu item is clicked
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "myContextMenu") {
      // Do something when the menu item is clicked
      console.log("Context menu item clicked!");
      console.log("Page URL:", info.pageUrl);
      console.log("Selected text:", info.selectionText);
    }
  });
  