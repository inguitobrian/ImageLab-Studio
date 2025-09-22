const { contextBridge, ipcRenderer } = require("electron");

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld("electronAPI", {
  // File operations
  onFileSelected: (callback) => ipcRenderer.on("file-selected", callback),
  onSaveImage: (callback) => ipcRenderer.on("save-image", callback),

  // Processing operations
  onOpenBatchModal: (callback) => ipcRenderer.on("open-batch-modal", callback),
  onExportPDF: (callback) => ipcRenderer.on("export-pdf", callback),

  // Utility functions
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),

  // Send messages to main process (if needed for future features)
  sendToMain: (channel, data) => {
    // Whitelist of allowed channels
    const validChannels = [
      "image-processed",
      "batch-complete",
      "pdf-exported",
      "processing-error",
    ];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },

  // Request operations from main process
  requestFileOpen: () => ipcRenderer.invoke("request-file-open"),
  requestFileSave: (data) => ipcRenderer.invoke("request-file-save", data),

  // Platform information
  platform: process.platform,

  // Version information
  versions: {
    node: process.versions.node,
    chrome: process.versions.chrome,
    electron: process.versions.electron,
  },
});

// Log when preload script is loaded (for debugging)
console.log("Preload script loaded successfully");
