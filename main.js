const { app, BrowserWindow, ipcMain } = require('electron');
require('electron-reload')(__dirname, {
    electron: require(`${__dirname}/node_modules/electron`)
});


function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 1024,
        height: 800,
        fullscreen: true, // Consider setting this dynamically or providing an option for the user to toggle fullscreen mode
        webPreferences: {
            nodeIntegration: true, // Disable nodeIntegration for security
            // contextIsolation: true, // Enable contextIsolation for security
            // preload: `${__dirname}/preload.js` // Use a preload script
        }
    });

    mainWindow.loadFile('html/home.html');

    mainWindow.webContents.session.webRequest.onHeadersReceived((details, callback) => {
        const contentType = details.responseHeaders['Content-Type'] || details.responseHeaders['content-type'];
        if (contentType) {
            const value = Array.isArray(contentType) ? contentType[0] : contentType;
            if (value.startsWith('text/html')) {
                details.responseHeaders['Cache-Control'] = ['max-age=604800']; // 1 week cache for HTML
            } else if (value.startsWith('image/')) {
                details.responseHeaders['Cache-Control'] = ['max-age=2592000']; // 30 days cache for images
            }
        }
        callback({ cancel: false, responseHeaders: details.responseHeaders });
    });

    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
    });

    // Error handling for window creation
    mainWindow.on('error', (error) => {
        console.error(`An error occurred creating the window: ${error}`);
    });
}

app.whenReady().then(createWindow).catch(error => {
    console.error(`Failed to create window: ${error}`);
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});