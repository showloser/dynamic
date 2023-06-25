// do i need to make the background.js file if there is no code there?

// ChatGPT
// In a Manifest V3 Chrome extension, the background.js file is not strictly necessary if there is no code to be executed in the background script.

// However, the background.js file can still be included in the extension's directory structure even if it's empty. This is because the background key is required in the manifest.json file for Manifest V3 extensions, and it expects a valid JavaScript file path for the background script.

// So, even if the background.js file is empty, you can include it in the extension's directory structure with no code inside. It will fulfill the requirement of having a background script file for Manifest V3.