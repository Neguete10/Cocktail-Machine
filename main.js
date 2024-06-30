const { app, BrowserWindow, ipcMain } = require('electron');
//const { exec } = require('child_process');
require('electron-reload')(__dirname, {
    electron: require(`${__dirname}/node_modules/electron`)
});

// ipcMain.on('shutdown-command', (event) => {
//     exec('sudo shutdown -h now', (error, stdout, stderr) => {
//         if (error) {
//             console.error(`exec error: ${error}`);
//             return;
//         }
//         console.log(`stdout: ${stdout}`);
//         console.error(`stderr: ${stderr}`);
//     });
// });

// ipcMain.on('reboot-command', (event) => {
//     exec('sudo reboot', (error, stdout, stderr) => {
//         if (error) {
//             console.error(`exec error: ${error}`);
//             return;
//         }
//         console.log(`stdout: ${stdout}`);
//         console.error(`stderr: ${stderr}`);
//     });
// });

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