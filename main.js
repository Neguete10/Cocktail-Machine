const { app, BrowserWindow } = require('electron');
require('electron-reload')(__dirname, {
    electron: require(`${__dirname}/node_modules/electron`)
  });

let win;

function createWindow() {
    win = new BrowserWindow({        
        width: 1024,
        height: 600,
        show: false,
    });

    win.loadFile('html/home.html');

    win.once('ready-to-show', () => {
        win.minimize();
        win.webContents.openDevTools();
    });

    win.setMenu(null);

    // Handle window close
    win.on('closed', () => {
        // Dereference the window object
        win = null;
    });
}

// When Electron has finished initialization, create the window
app.whenReady().then(createWindow);

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    if (win && !win.isDestroyed()) {
        if (win.webContents.isDevToolsOpened()) {
            win.webContents.closeDevTools();
        }
    }
});
// On macOS, re-create the window when the dock icon is clicked and no other windows are open
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});