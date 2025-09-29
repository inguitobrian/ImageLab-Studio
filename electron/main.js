const { app, BrowserWindow, Menu, shell, dialog } = require("electron");
const path = require("path");
const isDev = process.env.NODE_ENV === "development";

// Keep a global reference of the window object
let mainWindow;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      webSecurity: true,
    },
    titleBarStyle: process.platform === "darwin" ? "hiddenInset" : "default",
    show: false, // Don't show until ready
    icon: path.join(__dirname, "assets", "icon.png"),
  });

  // Load the app
  if (isDev) {
    mainWindow.loadURL("http://localhost:5173");
    // keep DevTools in dev
    mainWindow.webContents.openDevTools({ mode: "detach" });
  } else {
    mainWindow
      .loadFile(path.join(__dirname, "../dist/index.html"))
      .catch((err) => {
        // If loading fails, show an error page so the window is not blank
        console.error("Failed to load dist/index.html", err);
        mainWindow.loadURL(
          "data:text/html,<h1>Failed to load app</h1><p>Check console for errors.</p>"
        );
      })
      .finally(() => {
        // Open DevTools in production too (detached)
        mainWindow.webContents.openDevTools({ mode: "detach" });
      });
  }

  // Show window when ready to prevent visual flash
  mainWindow.once("ready-to-show", () => {
    mainWindow.show();

    // ensure DevTools are visible (redundant but helpful)
    mainWindow.webContents.openDevTools({ mode: "detach" });
  });

  // Handle window closed
  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });
}

// Create application menu
function createMenu() {
  const template = [
    {
      label: "File",
      submenu: [
        {
          label: "Open Image",
          accelerator: "CmdOrCtrl+O",
          click: async () => {
            const result = await dialog.showOpenDialog(mainWindow, {
              properties: ["openFile"],
              filters: [
                {
                  name: "Images",
                  extensions: ["jpg", "jpeg", "png", "bmp", "tiff", "tif"],
                },
              ],
            });

            if (!result.canceled) {
              // Send file path to renderer process
              mainWindow.webContents.send("file-selected", result.filePaths[0]);
            }
          },
        },
        {
          label: "Save Processed Image",
          accelerator: "CmdOrCtrl+S",
          click: () => {
            mainWindow.webContents.send("save-image");
          },
        },
        { type: "separator" },
        {
          label: "Exit",
          accelerator: process.platform === "darwin" ? "Cmd+Q" : "Ctrl+Q",
          click: () => {
            app.quit();
          },
        },
      ],
    },
    {
      label: "Edit",
      submenu: [
        { role: "undo" },
        { role: "redo" },
        { type: "separator" },
        { role: "cut" },
        { role: "copy" },
        { role: "paste" },
      ],
    },
    {
      label: "View",
      submenu: [
        { role: "reload" },
        { role: "forceReload" },
        { role: "toggleDevTools" },
        { type: "separator" },
        { role: "resetZoom" },
        { role: "zoomIn" },
        { role: "zoomOut" },
        { type: "separator" },
        { role: "togglefullscreen" },
      ],
    },
    {
      label: "Processing",
      submenu: [
        {
          label: "Batch Process",
          accelerator: "CmdOrCtrl+B",
          click: () => {
            mainWindow.webContents.send("open-batch-modal");
          },
        },
        {
          label: "Export PDF Report",
          accelerator: "CmdOrCtrl+P",
          click: () => {
            mainWindow.webContents.send("export-pdf");
          },
        },
      ],
    },
    {
      label: "Help",
      submenu: [
        {
          label: "About OpenCV Studio",
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: "info",
              title: "About OpenCV Studio",
              message: "OpenCV Image Processing Studio",
              detail:
                "A professional image processing application built with Vue.js, Electron, and FastAPI.\n\nVersion: 1.0.0",
            });
          },
        },
        {
          label: "Learn More",
          click: () => {
            shell.openExternal("https://opencv.org/");
          },
        },
      ],
    },
  ];

  // macOS specific menu adjustments
  if (process.platform === "darwin") {
    template.unshift({
      label: app.getName(),
      submenu: [
        { role: "about" },
        { type: "separator" },
        { role: "services" },
        { type: "separator" },
        { role: "hide" },
        { role: "hideOthers" },
        { role: "unhide" },
        { type: "separator" },
        { role: "quit" },
      ],
    });

    // Edit menu
    template[2].submenu.push(
      { type: "separator" },
      {
        label: "Speech",
        submenu: [{ role: "startSpeaking" }, { role: "stopSpeaking" }],
      }
    );

    // Window menu
    template.splice(4, 0, {
      label: "Window",
      submenu: [{ role: "minimize" }, { role: "close" }],
    });
  }

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// This method will be called when Electron has finished initialization
app.whenReady().then(() => {
  createWindow();
  createMenu();

  app.on("activate", () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

// Security: Prevent new window creation
app.on("web-contents-created", (event, contents) => {
  contents.on("new-window", (navigationEvent, navigationURL) => {
    event.preventDefault();
    shell.openExternal(navigationURL);
  });
});

// Handle certificate errors
app.on(
  "certificate-error",
  (event, webContents, url, error, certificate, callback) => {
    if (isDev) {
      // In development, ignore certificate errors
      event.preventDefault();
      callback(true);
    } else {
      // In production, use default behavior
      callback(false);
    }
  }
);
